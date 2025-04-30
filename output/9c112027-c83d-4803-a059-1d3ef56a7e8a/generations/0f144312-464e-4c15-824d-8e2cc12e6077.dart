import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom builder delegate for LMChatroomScreen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount,
  ) {
    // Use copyWith to modify the default AppBar
    return appBar.copyWith(
      title: const LMChatText(
        "custom chatroom", // Set the custom title
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // Adjust title color for visibility
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Set the custom background color
      ),
      // Keep other AppBar elements like actions or leading if needed
      // For example, to keep the default back button:
      // leading: appBar.leading,
      // Or to keep default trailing actions:
      // trailing: appBar.trailing,
    );
  }
}

// Create a custom configuration with the custom builder
final customChatroomConfig = LMChatroomConfig(
  builder: CustomChatroomBuilder(),
);

// Create the main chat configuration using the custom chatroom config
final customChatConfig = LMChatConfig(
  chatRoomConfig: customChatroomConfig,
);

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Call setup function before the runApp() function
  // Initialize LMChatCore with the custom configuration
  await LMChatCore.instance.initialize(
    config: customChatConfig,
  );
  // run the app
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false, // Hide the debug banner
    home: const LMSampleChat(),
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
            // initiate user session with apiKey, uuid and userName
            // this is required to show the chat
            // TODO: Replace with YOUR_API_KEY
            // TODO: Replace with YOUR_UUID
            // TODO: Replace with YOUR_USERNAME
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
              uuid: "abc",
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
              // Optionally show an error message to the user
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      'Error opening chat: ${response.errorMessage ?? "Unknown error"}'),
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