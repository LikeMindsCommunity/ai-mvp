"""
Project creator agent for generating actual Android projects from generated code.
"""

import os
import subprocess
import shutil
from pathlib import Path
import textwrap
from typing import Dict, List, Optional, Callable
from code_generator.config import Settings
from .constants import BUILD_CONFIG_FILES
from document_ingest.ingest import ingest_repo

class ProjectCreator:
    """
    Agent responsible for creating actual Android projects from generated code.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the project creator.
        
        Args:
            settings (Settings): Settings object containing configuration
        """
        self.settings = settings
        # Set up project paths
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), self.settings.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _build_docker_image(self, project_dir: str) -> tuple[bool, str]:
        """
        Build the Docker image for the project.
        
        Args:
            project_dir (str): Path to the project directory
            
        Returns:
            tuple[bool, str]: (success, error_message)
        """
        try:
            # Get project name from directory path
            project_name = os.path.basename(project_dir)
            
            # Convert absolute project_dir to relative path from Dockerfile location
            dockerfile_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            relative_project_dir = os.path.relpath(project_dir, dockerfile_dir)
            
            # Build the Docker image with volume mount
            print(f"\nBuilding Docker image for project: {project_dir}")
            print(f"Using relative project path: {relative_project_dir}")
            copy_cmd = [
                "docker", "build",
                "-t", "likeminds-feed-builder",
                "--build-arg", f"PROJECT_NAME={project_name}",
                "--build-arg", f"PROJECT_DIR={relative_project_dir}",
                "."
            ]
            
            print(f"Running Docker build command to create image likeminds-feed-builder and copy project to container: {' '.join(copy_cmd)}")
            result = subprocess.run(copy_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Docker build failed with error:\n{result.stderr}")
                print(f"Docker build stdout:\n{result.stdout}")
                return False, result.stderr

            # Run Gradle build command
            print("\nBuilding APK...\n\n")
            # First refresh dependencies
            refresh_cmd = [
                "docker", "run", "--rm",
                "-v", f"{project_dir}:/{project_name}",
                "-w", f"/{project_name}",
                "-t", "likeminds-feed-builder",
                "./gradlew", "--refresh-dependencies"
            ]
            
            print(f"Running Docker run command to refresh dependencies: {' '.join(refresh_cmd)}")
            result = subprocess.run(refresh_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Gradle refresh failed with error:\n{result.stderr}")
                print(f"Gradle refresh stdout:\n{result.stdout}")
                return False, result.stderr

            # Compile the project
            compile_cmd = [
                "docker", "run", "--rm",                    # Run a container and remove it after completion
                "-v", f"{project_dir}:/{project_name}",     # Mount the project directory to /[project_name]
                "-w", f"/{project_name}",                   # Set working directory to /[project_name]
                "-t", "likeminds-feed-builder",             # Use the builder image
                "./gradlew", "compileDebugJavaWithJavac"    # Run Gradle compile command
            ]
            
            print(f"Running Docker run command to compile project: {' '.join(compile_cmd)}")
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Gradle compile failed with error:\n{result.stderr}")
                print(f"Gradle compile stdout:\n{result.stdout}")
                return False, result.stderr

            # Then build the APK
            build_cmd = [
                "docker", "run", "--rm",
                "-v", f"{project_dir}:/{project_name}",
                "-w", f"/{project_name}",
                "-t", "likeminds-feed-builder",
                "./gradlew", "assembleDebug"
            ]
            
            print(f"Running Docker run command to build APK: {' '.join(build_cmd)}")
            result = subprocess.run(build_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Gradle build failed with error:\n{result.stderr}")
                print(f"Gradle build stdout:\n{result.stdout}")
                return False, result.stderr
                
            print("Project built successfully!")
            return True, ""
            
        except Exception as e:
            print(f"Unexpected error during build: {str(e)}")
            return False, str(e)
    
    def _copy_template_resources(self, template_dir: str, project_dir: str, llm_generated_files: List[str]) -> None:
        """
        Copy all resource files from template to project directory, except those generated by LLM.
        
        Args:
            template_dir (str): Path to template directory
            project_dir (str): Path to project directory
            llm_generated_files (List[str]): List of file paths generated by LLM
        """
        template_res_dir = os.path.join(template_dir, 'app', 'src', 'main', 'res')
        project_res_dir = os.path.join(project_dir, 'app', 'src', 'main', 'res')
        
        if not os.path.exists(template_res_dir):
            print(f"Warning: Template resources directory not found: {template_res_dir}")
            return
            
        # Create project resources directory
        os.makedirs(project_res_dir, exist_ok=True)
        
        # Convert LLM generated file paths to relative paths within res directory
        llm_res_files = set()
        for file_path in llm_generated_files:
            if file_path.startswith('app/src/main/res/'):
                rel_path = os.path.relpath(file_path, 'app/src/main/res')
                llm_res_files.add(rel_path)
        
        # Copy all files from template res directory
        for root, dirs, files in os.walk(template_res_dir):
            rel_path = os.path.relpath(root, template_res_dir)
            target_dir = os.path.join(project_res_dir, rel_path)
            
            # Create target directory
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy files
            for file in files:
                source_file = os.path.join(root, file)
                rel_file_path = os.path.join(rel_path, file)
                
                # Skip if file was generated by LLM
                if rel_file_path in llm_res_files:
                    print(f"Skipping LLM generated file: {rel_file_path}")
                    continue
                    
                target_file = os.path.join(target_dir, file)
                shutil.copy2(source_file, target_file)
                print(f"Copied resource file: {rel_file_path}")
    def install_app_on_remote_emulator(
        self,
        apk_path: str,
        package_name: str,
        remote_device_ip: str = "98.70.40.83",
        remote_device_port: str = "5555",
        on_chunk: Optional[Callable[[Dict], None]] = None,
    ) -> tuple[bool, str]:
        """
        Runs the original Bash installer inside a *single* Docker container.

        Returns:
            (success, stderr_if_any)
        """
        apk_abspath = os.path.abspath(apk_path)
        apk_dir, apk_file = os.path.split(apk_abspath)

        # The original Bash logic, untouched except for:
        #  • waiting handled with `sleep 2`
        #  • variables read from the environment
        installer_script = textwrap.dedent(
            """
            #!/usr/bin/env bash
            set -euo pipefail

            echo "Starting ADB server…"
            adb start-server

            echo "Checking connection to $REMOTE_DEVICE_IP:$REMOTE_DEVICE_PORT"
            if adb devices | grep -q "$REMOTE_DEVICE_IP:$REMOTE_DEVICE_PORT"; then
                echo "Device already connected."
            else
                adb connect "$REMOTE_DEVICE_IP:$REMOTE_DEVICE_PORT"
            fi

            sleep 2
            echo "Connected devices:"
            adb devices

            if [[ -n "$APK_PATH" ]]; then
                echo "Installing $APK_PATH"
                adb install -r "$APK_PATH"
            else
                echo "No APK specified, skipping install"
            fi

            if [[ -n "$PACKAGE_NAME" ]]; then
                echo "Launching $PACKAGE_NAME"
                adb shell monkey -p "$PACKAGE_NAME" -c android.intent.category.LAUNCHER 1
            else
                echo "No package to launch, done."
            fi
            """
        )

        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "--network", "host",               # So the container can reach 98.70.40.83
            "-v", f"{apk_dir}:/workspace/apk:ro",
            "-e", f"REMOTE_DEVICE_IP={remote_device_ip}",
            "-e", f"REMOTE_DEVICE_PORT={remote_device_port}",
            "-e", f"APK_PATH=/workspace/apk/{apk_file}",
            "-e", f"PACKAGE_NAME={package_name}",
            "-t", "likeminds-feed-builder",
            "bash", "-s",                      # read script from STDIN
        ]

        try:
            proc = subprocess.run(
                docker_cmd,
                input=installer_script,
                text=True,
                capture_output=True,
                check=False,                   # we’ll inspect returncode ourselves
            )
            if proc.returncode != 0:
                # Bubble up full stderr so you can debug quickly
                if on_chunk:
                    on_chunk({"type": "Error", "value": proc.stderr})
                return False, proc.stderr

            if on_chunk:
                on_chunk(
                    {"type": "Result", "value": "APK installed and app launched successfully."}
                )
            return True, ""

        except FileNotFoundError as nf:
            # `docker` or the APK path missing on host
            err_msg = f"Host setup problem: {nf}"
            if on_chunk:
                on_chunk({"type": "Error", "value": err_msg})
            return False, err_msg

        except Exception as e:
            if on_chunk:
                on_chunk({"type": "Error", "value": str(e)})
            return False, str(e)
        
    def create_project(self, project_data: Dict, on_chunk: Optional[Callable[[Dict], None]] = None) -> tuple[bool, str]:
        """
        Create a complete Android project from the generated data.
        
        Args:
            project_data (Dict): Project data containing file structure and content
            on_chunk (Optional[Callable[[Dict], None]]): Optional callback function for progress updates
            
        Returns:
            tuple[bool, str]: (success, error_message)
        """
        try:
            if not project_data:
                return False, "Error: No project data provided"
                
            if "project_name" not in project_data:
                return False, "Error: Project name not found in project data"
                
            if "files" not in project_data:
                return False, "Error: No files found in project data"
                
            if "namespace" not in project_data:
                return False, "Error: Namespace not found in project data"
                
            if "application_id" not in project_data:
                return False, "Error: Application ID not found in project data"
            
            # Create project directory
            project_name = project_data["project_name"]
            project_dir = os.path.join(self.output_dir, project_name)
            print(f"\nCreating project directory: {project_dir}")
            os.makedirs(project_dir, exist_ok=True)
            
            # Get template directory path
            template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "code_generator", "likeminds-feed-android-social-feed-theme")
            
            # Copy all build configuration files from template
            for file in BUILD_CONFIG_FILES:
                src_path = os.path.join(template_dir, file)
                dst_path = os.path.join(project_dir, file)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy file if it exists in template
                if os.path.exists(src_path):
                    if file == 'app/build.gradle':
                        # Read the template build.gradle
                        with open(src_path, 'r') as f:
                            content = f.read()
                        
                        # Replace namespace and applicationId
                        content = content.replace(
                            'namespace \'com.likeminds.feed.social.example\'',
                            f'namespace \'{project_data["namespace"]}\''
                        )
                        content = content.replace(
                            'applicationId "com.likeminds.feed.social.example"',
                            f'applicationId "{project_data["application_id"]}"'
                        )
                        
                        # Write the modified build.gradle
                        with open(dst_path, 'w') as f:
                            f.write(content)
                        print(f"Updated build.gradle with namespace: {project_data['namespace']} and applicationId: {project_data['application_id']}")
                    else:
                        shutil.copy2(src_path, dst_path)
                        print(f"Copied build config file: {file}")
            
            # Create files from generated data
            print("Creating project files...")
            for file_data in project_data["files"]:
                file_path = file_data["path"]
                content = file_data["content"]
                
                full_path = os.path.join(project_dir, file_path)
                print(f"Creating file: {full_path}")
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
                
                # Call on_chunk callback if provided
                if on_chunk:
                    on_chunk({
                        "type": "Result",
                        "value": file_path
                    })
            
            # Build Docker image and get APK
            build_success, error_message = self._build_docker_image(project_dir)
            if not build_success:
                return False, error_message

            # Install APK on remote emulator
            apk_path = os.path.join(project_dir, "app", "build", "outputs", "apk", "debug", "app-debug.apk")
            package_name = project_data.get("application_id", "")
            install_success, install_error = self._install_app_on_remote_emulator(apk_path, package_name, on_chunk)
            if not install_success:
                return False, install_error

            return True, ""
            
        except Exception as e:
            return False, str(e)