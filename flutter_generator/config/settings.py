"""
Configuration settings for the Flutter code generator.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """
    Configuration settings for the Flutter code generator.
    Provides default values and environment variable loading.
    """
    
    def __init__(self):
        """Initialize settings with default values and load environment variables."""
        # API Configuration
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
        
        # Project paths
        self.integration_path = os.getenv("INTEGRATION_PATH", "integration")
        self.output_path = os.getenv("OUTPUT_PATH", "output")
        
        # Web server settings
        self.web_host = os.getenv("WEB_HOST", "localhost")
        self.web_port = int(os.getenv("WEB_PORT", "8080"))
        
        # Command timeout settings
        self.command_timeout = int(os.getenv("COMMAND_TIMEOUT", "300"))
        self.build_timeout = int(os.getenv("BUILD_TIMEOUT", "6000"))
        
        # Cleanup settings
        self.auto_cleanup = os.getenv("AUTO_CLEANUP", "false").lower() in ("true", "1", "yes")
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that required settings are present."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables or .env file")
        
        # Create required directories if they don't exist
        os.makedirs(self.output_path, exist_ok=True)
        
        # Ensure integration directory exists, create it if it doesn't
        if not os.path.exists(self.integration_path):
            print(f"Integration directory not found at: {self.integration_path}, creating a new one")
            os.makedirs(self.integration_path, exist_ok=True)
            
            # Create basic Flutter structure
            lib_dir = os.path.join(self.integration_path, "lib")
            os.makedirs(lib_dir, exist_ok=True)
            
            # Create a basic pubspec.yaml file
            pubspec_path = os.path.join(self.integration_path, "pubspec.yaml")
            with open(pubspec_path, "w") as f:
                f.write("""name: flutter_integration
description: A new Flutter project for integration testing.
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
""")
            
            # Create a basic main.dart file
            main_dart_path = os.path.join(lib_dir, "main.dart")
            with open(main_dart_path, "w") as f:
                f.write("""import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Integration',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Integration Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: const Text('Ready for integration'),
      ),
    );
  }
}
""")

        # Validate port number
        if not (1024 <= self.web_port <= 65535):
            raise ValueError(f"Invalid web port number: {self.web_port}")
            
        # Validate timeouts
        if self.command_timeout < 1:
            raise ValueError(f"Invalid command timeout: {self.command_timeout}")
        if self.build_timeout < 1:
            raise ValueError(f"Invalid build timeout: {self.build_timeout}") 