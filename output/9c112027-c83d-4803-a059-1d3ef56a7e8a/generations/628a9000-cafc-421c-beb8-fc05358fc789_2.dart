import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom builder delegate to modify the Chatroom screen's AppBar
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Added missing parameter
  ) {
    // Use copyWith on the default AppBar to change specific properties
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

  // Create an instance of the custom chatroom builder
  final customBuilder = CustomChatroomBuilder();

  // Create a dark theme instance
  final darkTheme = LMChatThemeData.dark();

  // Call setup function before the runApp() function
  await LMChatCore.instance.initialize(
    // Pass the custom theme and config during initialization
    theme: darkTheme,
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: customBuilder, // Pass the custom builder here
      ),
    ),
  );
  // run the app
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false, // Hides the debug banner
    home: LMSampleChat(),
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
            if (!context.mounted) return;

            if (response.success) {
              // create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optionally show a snackbar or dialog to the user
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      'Error opening chat: ${response.errorMessage ?? 'Unknown error'}'),
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