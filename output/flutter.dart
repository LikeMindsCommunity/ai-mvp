import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

void main() async {
  // Ensure Flutter bindings are initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize the LikeMinds Chat SDK
  // [cite: chat/Flutter/getting-started.md]
  await LMChatCore.instance.initialize();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LikeMinds Chat Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  void _initiateChat() async {
    // Initiate user session using API Key (Client Side Authentication)
    // [cite: chat/Flutter/getting-started.md]
    LMResponse<void> response = await LMChatCore.instance.showChatWithApiKey(
      apiKey: "YOUR_API_KEY", // TODO: Replace with YOUR_API_KEY
      uuid: "USER_ID", // TODO: Replace with YOUR_USER_ID
      userName: "USER_NAME", // TODO: Replace with YOUR_USER_NAME
    );

    // Check if the initiation was successful
    if (response.success) {
      // Navigate to the LMChatHomeScreen
      // [cite: chat/Flutter/getting-started.md]
      if (mounted) { // Ensure the widget is still in the tree
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => const LMChatHomeScreen(),
          ),
        );
      }
    } else {
      // Handle initiation error
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error initiating chat: ${response.errorMessage}'),
          ),
        );
      }
      print('Error initiating chat: ${response.errorMessage}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LikeMinds Chat Demo'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: _initiateChat,
          child: const Text('Start Chat'),
        ),
      ),
    );
  }
}