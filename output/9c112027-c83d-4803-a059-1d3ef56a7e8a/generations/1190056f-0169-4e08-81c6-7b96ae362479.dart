import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Required for LMChatText

class CustomChatroomBuilderDelegate extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount,
  ) {
    // Use copyWith to modify the existing AppBar style
    return appBar.copyWith(
      title: const LMChatText(
        "custom chatroom", // Set the custom title
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // Set title text color if needed
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      style: appBar.style?.copyWith(
            backgroundColor: Colors.purple, // Set the custom background color
          ) ??
          LMChatAppBarStyle.basic(Colors.purple), // Use basic if style is null
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LMChatCore with the custom builder delegate
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilderDelegate(),
      ),
    ),
  );

  runApp(const MaterialApp(
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