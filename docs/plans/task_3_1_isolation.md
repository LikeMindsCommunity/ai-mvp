# Task 3.1: Isolate Integration Environment

## Overview

This task involved updating the Flutter code generation system to use isolated environments for each generation. Previously, all Flutter code generations shared the same integration directory, which could lead to conflicts when multiple generations were running concurrently.

The goal was to create a per-generation directory structure, where each code generation gets its own isolated environment. This prevents conflicts between different generations and allows for better resource management and cleanup.

## Implementation Details

### 1. Directory Structure

Each code generation uses its database ID (from the `code_generations` table) as its unique identifier and gets its own directory structure:

```
output/
  ├── {generation_id}/
  │   ├── flutter_code_1.dart
  │   ├── flutter_code_2.dart (if fixes were applied)
  │   └── integration/
  │       ├── lib/
  │       │   └── main.dart
  │       ├── pubspec.yaml
  │       └── ... (other Flutter project files)
```

The root `integration/` directory now serves as a template that gets copied to each generation-specific directory.

### 2. Components Updated

#### FlutterCodeManager

- Added support for generation-specific directories
- Implemented directory creation and management methods
- Updated code saving and analysis to use the isolated directories
- Added cleanup method to remove generation directories when no longer needed

#### FlutterIntegrationManager

- Updated to work with isolated integration directories
- Modified command execution to handle working directory correctly
- Improved process tracking and termination
- Added better logging with per-generation log files

#### FlutterGeneratorServiceImpl

- Implemented generation tracking using dictionaries
- Created helper methods to get or create managers for specific generations
- Added generation cleanup functionality
- Updated service methods to use the isolated environments
- Uses database-generated IDs for synchronization with the code_generations table

#### WebSocketHandler

- Added tracking of active generation IDs per WebSocket connection
- Implemented cleanup on WebSocket disconnect
- Added support for client-initiated cleanup
- Enhanced error handling to ensure proper cleanup in all scenarios
- Passes database-generated IDs to the FlutterGeneratorServiceImpl to maintain synchronization

### 3. Configuration

Added a new environment variable to control automatic cleanup:

- `AUTO_CLEANUP`: When set to true, automatically cleans up generation directories when they're no longer needed

### 4. Cleanup Script

Created a utility script `tools/cleanup_old_generations.py` to clean up old generation directories:

```bash
# Basic usage (removes generations older than 24 hours)
python tools/cleanup_old_generations.py

# Specify a different age threshold
python tools/cleanup_old_generations.py --age-hours 48

# Perform a dry run (no files are actually deleted)
python tools/cleanup_old_generations.py --dry-run

# Verbose output
python tools/cleanup_old_generations.py -v
```

## Benefits

1. **Isolation**: Each generation runs in its own environment, preventing conflicts between concurrent generations.
2. **Resource Management**: Resources are properly tracked and cleaned up when no longer needed.
3. **Scalability**: The system can now handle multiple concurrent generations without interference.
4. **Reliability**: Failures in one generation don't affect others, improving overall system stability.

## Usage

The client API remains the same, but the response now includes a `generation_id` field that can be used to reference the specific generation:

```json
{
  "success": true,
  "web_url": "http://localhost:8080",
  "code_path": "/output/12345678-1234-5678-1234-567812345678/flutter_code_1.dart",
  "generation_id": "12345678-1234-5678-1234-567812345678"
}
```

When fixing code, the client should include the `generation_id` to ensure the fix is applied to the correct environment:

```json
{
  "type": "FixCode",
  "user_query": "Fix the errors in my Flutter app",
  "error_message": "Error details...",
  "generation_id": "12345678-1234-5678-1234-567812345678"
}
```

To clean up a specific generation, clients can send:

```json
{
  "type": "CleanupGeneration",
  "generation_id": "12345678-1234-5678-1234-567812345678"
}
```

## Environment Variables

```
# Isolation and Cleanup Configuration
AUTO_CLEANUP=false  # Set to true to automatically clean up generation directories
OUTPUT_PATH=output
INTEGRATION_PATH=integration
``` 