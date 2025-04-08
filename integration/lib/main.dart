import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Define a custom builder delegate for the Chatroom screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantCount, // Corrected signature
  ) {
    // Use copyWith to customize the default app bar
    return appBar.copyWith(
      // Customize the style of the app bar
      style: appBar.style?.copyWith(
            backgroundColor: Colors.blue, // Set background color to blue
          ) ??
          const LMChatAppBarStyle(backgroundColor: Colors.blue),
      // Customize the title widget
      title: LMChatText(
        'Custom Chatroom', // Set the title text
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // Set text color to white
            fontSize: 18, // Optional: Set font size
            fontWeight: FontWeight.bold, // Optional: Set font weight
          ),
        ),
      ),
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Call setup function before the runApp() function
  // Initialize LMChatCore with the custom configuration
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(), // Pass the custom builder delegate
      ),
    ),
  );
  // run the app
  runApp(const MaterialApp(home: LMSampleChat()));
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
              // TODO: Replace with YOUR_USERNAME
              userName: "abc",
            );
            if (response.success) {
              if (!context.mounted) return; // Check context validity
              // create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optionally, show a snackbar or dialog for the error
              // if (context.mounted) { // Check context validity
              //   ScaffoldMessenger.of(context).showSnackBar(
              //     SnackBar(content: Text("Error opening chat: ${response.errorMessage}")),
              //   );
              // }
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}