import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Define a custom builder delegate for the Chatroom screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    // Add the missing participantsCount parameter
    int participantsCount,
  ) {
    // Return a customized AppBar using copyWith
    return appBar.copyWith(
      title: const Text("custom chatroom"), // Set custom title
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Set custom background color
      ),
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LMChatCore with the custom Chatroom configuration and a dark theme
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(), // Pass the custom builder
      ),
    ),
    theme: LMChatThemeData.dark(), // Apply the dark theme
  );

  // run the app
  runApp(const MaterialApp(
      debugShowCheckedModeBanner: false, home: LMSampleChat()));
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
            // Define the route before the async call
            final route = MaterialPageRoute(
              builder: (context) => const LMChatHomeScreen(),
            );
            // initiate user session with apiKey, uuid and userName
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

            // Check if the widget is still mounted before using context
            if (!context.mounted) return;

            if (response.success) {
              // navigate to LMChatSocialScreen
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optionally show a snackbar or dialog to inform the user
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