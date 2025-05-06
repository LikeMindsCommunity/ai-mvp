import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Import UI package for LMChatAppBar

// Custom Builder Delegate for Chatroom Screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Added missing parameter based on delegate signature
  ) {
    // Use copyWith on the default AppBar to modify specific properties
    return appBar.copyWith(
      title: const Text("custom chatroom"), // Set the custom title
      style: appBar.style?.copyWith(
            backgroundColor: Colors.purple, // Set the custom background color
          ) ??
          const LMChatAppBarStyle(backgroundColor: Colors.purple),
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Define the custom chatroom configuration
  final customChatroomConfig = LMChatroomConfig(
    builder: CustomChatroomBuilder(), // Use the custom builder delegate
  );

  // Initialize LMChatCore with the custom configuration
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: customChatroomConfig,
    ),
  );

  // Run the app
  runApp(const MaterialApp(
      home: LMSampleChat(), debugShowCheckedModeBanner: false));
}

// A blank scaffold with a button that opens
// the LM Social Chat when clicked
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
            // initiate user session with apiKey, uuid and userName
            // this is required to show the chat
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              // TODO: Replace with YOUR_API_KEY
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
              // TODO: Replace with YOUR_UUID
              uuid: "abc",
              // TODO: Replace with YOUR_USER_NAME
              userName: "abc",
            );
            if (response.success) {
              // create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}