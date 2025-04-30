import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Import the UI package for LMChatAppBar

// Custom Builder Delegate for Chatroom Screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantCount, // Added participantCount parameter as per LMChatroomScreen.md context
  ) {
    // Use copyWith on the default LMChatAppBar to customize it
    return appBar.copyWith(
      title: const Text(
        "custom chatroom", // Set the custom title
        style: TextStyle(color: Colors.white), // Optional: Set title text color
      ),
      style: (appBar.style ?? const LMChatAppBarStyle()).copyWith(
        backgroundColor: Colors.purple, // Set the custom background color
      ),
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LMChatCore with the custom chatroom configuration
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(), // Pass the custom builder delegate
      ),
    ),
  );

  // Run the app
  runApp(const MaterialApp(
    debugShowCheckedModeBanner: false, // Hide debug banner
    home: LMSampleChat(),
  ));
}

// A blank scaffold with a button that opens the LM Chat when clicked
class LMSampleChat extends StatelessWidget {
  const LMSampleChat({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LM Sample Chat'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // TODO: Replace with your API Key
            const String apiKey = "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8";
            // TODO: Replace with your User ID
            const String uuid = "abc";
            // TODO: Replace with your User Name
            const String userName = "abc";

            // Initiate user session with apiKey, uuid, and userName
            // This is required to show the chat
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: apiKey,
              uuid: uuid,
              userName: userName,
            );
            if (response.success) {
              // Create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // Navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optional: Show an error message to the user
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      "Error opening chat: ${response.errorMessage ?? 'Unknown error'}"),
                ),
              );
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}