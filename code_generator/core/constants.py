"""
Common constants used across the code generator.
"""

# List of build configuration files that should be excluded from code generation
# and handled separately in the project creation process
BUILD_CONFIG_FILES = [
    'build.gradle',
    'gradle.properties',
    'gradlew',
    'gradlew.bat',
    'settings.gradle',
    'app/build.gradle',
    'gradle/wrapper/gradle-wrapper.properties',
    'gradle/wrapper/gradle-wrapper.jar',
    'gradle/libs.versions.toml'
] 