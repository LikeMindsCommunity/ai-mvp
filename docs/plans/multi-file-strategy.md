# Multi-File Generation Strategy

## Problem Statement

The current Flutter code generation system is designed to work with a single file (main.dart), which significantly limits its ability to create proper Flutter integrations. Real-world Flutter applications require modifications across multiple files for proper architecture, including:

- Multiple Dart files for different screens, widgets, and services
- Modifications to pubspec.yaml for dependencies
- Asset files and resources
- Configuration files

This limitation forces all code to be placed in a single file, leading to poor architecture and maintainability issues.

## Strategic Goals

1. Enable the generation of multiple files in a single request
2. Support updating existing files in a project
3. Maintain awareness of project structure and architecture
4. Ensure proper file organization (following Flutter best practices)
5. Provide reliable analysis and error checking across all generated files
6. Support common operations like adding dependencies, assets, and configurations

## Potential Solutions Combined Approach

We will implement a combined approach leveraging the strengths of several strategies:

### 1. Multi-file Code Generation Format

Modify the LLM prompt and response parsing to handle a structured multi-file output format:

```
<file path="lib/main.dart">
// Complete main file content - include ALL contents of the file
</file>

<file path="lib/screens/home_screen.dart">
// Complete home screen content - include ALL contents of the file
</file>

<file path="pubspec.yaml">
# Complete pubspec.yaml file with all dependencies
name: my_app
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  # Any other dependencies
  
flutter:
  uses-material-design: true
</file>
```

IMPORTANT: ALWAYS include the ENTIRE file content in each file block. Each file should be a complete, standalone file that includes all existing code plus any new code. The system does not apply partial changes or patches.

File operations consist of simply specifying the file path: `<file path="path/to/file">` and including its complete contents.

### 2. Project-wide Code Management

Extend the `FlutterCodeManager` to handle multiple files:

- Track all files in the project (both existing and to be generated)
- Provide analysis across the entire project
- Maintain a consistent directory structure

### 3. Templated Integration Framework

Create a more sophisticated integration framework:

- Standard directory structure templates (screens, widgets, models, services)
- Common integration patterns for different features
- Project scaffolding for different architectures (BLoC, Provider, GetX)

### 4. Patch-based File Modifications

For existing files, implement a patch-based approach:

- Allow specifying sections to modify rather than replacing entire files
- Generate diffs for precise changes to existing files
- Apply patches safely with proper backup and validation

### 5. Componentized Architecture Support

Organize code generation around components:

- Break down features into distinct components (auth, chat, feed)
- Each component can generate its own set of files
- Components can have dependencies on other components

## Implementation Tasks

### Phase 1: Foundation (Weeks 1-2)

1. **Extend Code Extraction Logic**
   - [x] Modify regex patterns to extract multi-file code blocks
   - [x] Create parser for the file path and modification instructions
   - [x] Support "create" and "modify" modes for files

2. **Enhance FlutterCodeManager**
   - [x] Create `FileManager` class to handle multiple file operations
   - [x] Implement methods for saving multiple files
   - [x] Track file dependencies and relationships

3. **Update Generator Prompts**
   - [x] Update system instructions to specify multi-file output format
   - [x] Include examples of proper multi-file generation
   - [x] Add guidance for organizing code across files

### Phase 2: Core Functionality (Weeks 3-4)

4. **Implement File Operations**
   - [x] Create, modify, and delete operations for project files
   - [x] Safe handling of existing files (backup before modification)
   - [ ] Conflict resolution for overlapping changes

5. **Extend Analysis Tools**
   - [x] Project-wide code analysis
   - [x] Individual file analysis with error reporting
   - [x] Dependency validation across files

6. **Update Integration Process**
   - [x] Modify copy_to_integration to handle multiple files
   - [x] Create directory structure as needed
   - [x] Preserve existing files when appropriate

### Phase 3: Advanced Features (Weeks 5-6)

7. **Patch-based Modification System**
   - [ ] Implement diff generation for file modifications
   - [ ] Create patch application system with validation
   - [x] Support for section-based modifications

8. **Dependency Management**
   - [x] Parse and modify pubspec.yaml
   - [ ] Handle versioning conflicts
   - [ ] Run dependency resolution

9. **Asset Management**
   - [ ] Handle asset files and resources
   - [x] Update asset references in pubspec.yaml
   - [ ] Support for different asset types (images, fonts, etc.)

### Phase 4: Project Templates & Components (Weeks 7-8)

10. **Template System**
    - [ ] Create project templates for common architectures
    - [ ] Support for different state management approaches
    - [ ] Customizable templates based on project needs

11. **Componentized Generation**
    - [ ] Define component interfaces and dependencies
    - [ ] Implement component-based code generation
    - [ ] Component composition and integration

12. **Testing Framework**
    - [ ] Unit tests for multi-file generation
    - [ ] Integration tests for complex projects
    - [ ] Validation tools for generated code

## Technical Implementation Details

### File Format Parser

```python
def parse_file_blocks(generated_text):
    """Parse file blocks from generated text."""
    pattern = r'<file path="([^"]+)"(?:\s+mode="([^"]+)")?\s*(?:section="([^"]+)")?\s*>\n(.*?)</file>'
    matches = re.finditer(pattern, generated_text, re.DOTALL)
    
    file_operations = []
    for match in matches:
        path = match.group(1)
        mode = match.group(2) or "create"  # Default to create
        section = match.group(3)  # May be None
        content = match.group(4)
        
        file_operations.append({
            "path": path,
            "mode": mode,
            "section": section,
            "content": content
        })
    
    return file_operations
```

### Enhanced FlutterCodeManager

```python
class FlutterCodeManager:
    def __init__(self, project_id, generation_id=None):
        # Existing initialization
        self.files = {}  # Map of file paths to content
    
    def add_file(self, path, content, mode="create", section=None):
        """Add or modify a file."""
        if mode == "create" or path not in self.files:
            self.files[path] = content
        elif mode == "modify":
            if section:
                # Handle section-based modification
                self._modify_file_section(path, section, content)
            else:
                # Replace entire file
                self.files[path] = content
    
    def save_files(self):
        """Save all files to the project directory."""
        for path, content in self.files.items():
            full_path = os.path.join(self.integration_path, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
    
    def analyze_project(self):
        """Analyze the entire project."""
        # Implement project-wide analysis
```

### Prompt Enhancement

The LLM prompt will need to be updated to specify the multi-file format:

```
When generating Flutter code for the integration, please organize your code into multiple files following best practices.

Use the following format for each file:

<file path="lib/main.dart">
// Main file content
</file>

<file path="lib/screens/home_screen.dart">
// Home screen content
</file>

You can also modify existing files by specifying the mode:

<file path="pubspec.yaml" mode="modify" section="dependencies">
  some_package: ^1.0.0
</file>

Follow these guidelines:
1. Place screens in lib/screens/
2. Place widgets in lib/widgets/
3. Place models in lib/models/
4. Place services in lib/services/
5. Place utilities in lib/utils/
```

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Complexity in parsing multi-file output | High | Strong unit tests for parser, fallback mechanisms |
| Errors in file modification | High | Always backup files before modification, validate changes |
| LLM output format inconsistency | Medium | Strict validation, clear examples in prompt |
| Performance with many files | Medium | Optimize file operations, consider async processing |
| Dependency conflicts | Medium | Implement dependency resolution checking |
| Breaking existing functionality | High | Maintain backward compatibility, extensive testing |

## Success Metrics

1. **Functionality**
   - Successfully generate and update multiple files
   - Handle all required file types (Dart, YAML, JSON, etc.)
   - Properly organize code into appropriate files

2. **Quality**
   - Reduce code duplication across files
   - Improve code organization following Flutter best practices
   - Maintain high success rate in analysis and validation

3. **User Experience**
   - Simplified integration of complex features
   - Better maintainability of generated code
   - More natural code structure

## TODO List

- [x] Define multi-file output format specification
- [x] Implement file block parser
- [x] Update FlutterCodeManager to handle multiple files
- [x] Create file operation handlers (create, modify, delete)
- [x] Implement project-wide analysis tools
- [x] Update LLM prompts to specify multi-file output
- [ ] Create templates for common file structures
- [x] Implement pubspec.yaml modification handling
- [ ] Build component-based generation system
- [ ] Create testing framework for multi-file generation
- [x] Document the new multi-file capabilities
- [x] Create examples of multi-file integrations
- [x] Update file handling to use complete file content rather than patches

## Timeline

- **Weeks 1-2**: Foundation - parser, file manager, prompt updates
- **Weeks 3-4**: Core functionality - file operations, analysis, integration
- **Weeks 5-6**: Advanced features - patch system, dependency management
- **Weeks 7-8**: Templates and components - project templates, componentization

## Conclusion

The multi-file generation capability will significantly enhance the Flutter code generation system, enabling more sophisticated and maintainable integrations. By implementing this strategy in phases, we can incrementally improve the system while maintaining stability and backward compatibility. 