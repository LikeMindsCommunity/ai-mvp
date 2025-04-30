import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom builder delegate to customize the chatroom screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Added missing parameter
  ) {
    // Use copyWith on the default app bar and customize title and background color
    return appBar.copyWith(
      title: const Text("custom chatroom"), // Custom title
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Custom background color
      ),
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize the LikeMinds Chat SDK with dark theme and custom chatroom config
  await LMChatCore.instance.initialize(
    theme: LMChatThemeData.dark(), // Apply dark theme
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(), // Use the custom builder
      ),
    ),
  );

  // Run the app
  runApp(const MaterialApp(
    home: LMSampleChat(),
    debugShowCheckedModeBanner: false, // Hide debug banner
  ));
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
            // Initiate user session with apiKey, uuid and userName
            // this is required to show the chat
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              // TODO: Replace with YOUR_API_KEY
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
              // TODO: Replace with YOUR_USER_ID
              uuid: "abc",
              // TODO: Replace with YOUR_USER_NAME
              userName: "abc",
            );

            // Check if the context is still mounted before navigating
            if (response.success && context.mounted) {
              // Create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // Navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else if (context.mounted) {
              // Show error if response is not successful
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