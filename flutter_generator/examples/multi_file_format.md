# Multi-File Format Examples

This document provides examples of the correct multi-file format for the Flutter code generator.

## Basic Format

Each file block should contain the **complete** contents of the file, not just changes:

```
<file path="lib/main.dart">
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

// ... rest of file contents ...
</file>
```

## Complete pubspec.yaml Example

Always include the entire pubspec.yaml file with all dependencies:

```
<file path="pubspec.yaml">
name: my_app
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.5
  provider: ^6.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
  # assets:
  #   - images/a_dot_burr.jpeg
</file>
```

## Multiple Files Example

A complete example with multiple files:

```
<file path="lib/main.dart">
import 'package:flutter/material.dart';
import 'package:my_app/screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
</file>

<file path="lib/screens/home_screen.dart">
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: const Center(
        child: Text('Welcome to the Home Screen!'),
      ),
    );
  }
}
</file>

<file path="pubspec.yaml">
name: my_app
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
</file>
```

## Guidelines

1. Always include the entire content of each file
2. Use `<file path="path/to/file">` to specify each file
3. When modifying an existing file, include the complete file with all changes incorporated
4. Follow Flutter's file organization conventions:
   - Place screens in lib/screens/
   - Place widgets in lib/widgets/
   - Place models in lib/models/
   - Place services in lib/services/
   - Place utilities in lib/utils/ 