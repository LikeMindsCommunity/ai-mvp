import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Ensure UI package is imported for LMChatAppBar

// Custom Builder Delegate for Chatroom Screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount,
  ) {
    // Use copyWith on the default AppBar to customize
    return appBar.copyWith(
      title: const Text("custom chatroom"), // Set custom title
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Set custom background color
      ),
    );
  }
}

// Configuration for the Chatroom Screen
final LMChatroomConfig customChatroomConfig = LMChatroomConfig(
  builder: CustomChatroomBuilder(),
);

// Main Application Setup
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK with custom configuration
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: customChatroomConfig,
    ),
  );

  // Run the app
  runApp(const MaterialApp(
    debugShowCheckedModeBanner: false, // Hides the debug banner
    home: LMSampleChat(),
  ));
}

// Sample App Widget
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
            // TODO: Replace with YOUR_API_KEY, YOUR_USER_ID, YOUR_USER_NAME
            const String apiKey = "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8";
            // TODO: Replace with YOUR_USER_ID
            const String uuid = "abc";
            // TODO: Replace with YOUR_USER_NAME
            const String userName = "abc";

            // Initiate user session with apiKey, uuid and userName
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: apiKey,
              uuid: uuid,
              userName: userName,
            );

            if (response.success) {
              // Navigate to LMChatHomeScreen after successful session initiation
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              Navigator.pushReplacement(context, route);
            } else {
              // Handle error opening chat
              debugPrint("Error opening chat: ${response.errorMessage}");
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