import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom Builder Delegate to modify the Chatroom AppBar
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
  ) {
    // Return a customized AppBar
    return AppBar(
      title: const Text("custom chatroom"), // Set custom title
      backgroundColor: Colors.purple, // Set custom background color
      leading: appBar.leading, // Use default back button logic
      actions: appBar.trailing, // Use default actions
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Define custom dark theme
  LMChatThemeData darkTheme = LMChatThemeData.dark();

  // Define custom chatroom config with the custom builder
  LMChatroomConfig customChatroomConfig = LMChatroomConfig(
    builder: CustomChatroomBuilder(),
  );

  // Define overall SDK config including the chatroom customization
  LMChatConfig sdkConfig = LMChatConfig(
    chatRoomConfig: customChatroomConfig,
  );

  // Initialize LMChatCore with the dark theme and custom config
  await LMChatCore.instance.initialize(
    theme: darkTheme, // Apply dark theme
    config: sdkConfig, // Apply custom configurations
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
            // TODO: Replace with YOUR_API_KEY
            const String apiKey = "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8";
            // TODO: Replace with YOUR_USER_ID
            const String uuid = "abc";
             // TODO: Replace with YOUR_USER_NAME
            const String userName = "abc";

            // initiate user session with apiKey, uuid and userName
            // this is required to show the chat
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: apiKey,
              uuid: uuid,
              userName: userName,
            );
            if (response.success) {
              // create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              // Handle initialization error
              debugPrint("Error opening chat: ${response.errorMessage}");
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