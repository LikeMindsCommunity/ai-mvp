import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Import UI package for LMChatText and styles

// Custom Builder Delegate for Chatroom Screen
class CustomChatroomAppBarBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Updated parameter list as per LMChatroomBuilderDelegate
  ) {
    // Use copyWith on the default LMChatAppBar
    return appBar.copyWith(
      // Customize the style of the LMChatAppBar
      style: appBar.style?.copyWith(
            backgroundColor: Colors.blue.shade900, // Deep blue background
          ) ??
          LMChatAppBarStyle(
            backgroundColor: Colors.blue.shade900,
          ),
      // Set a custom title widget
      title: const LMChatText(
        "Custom ChatRoom", // Custom title text
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // White text color
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      // Customize the leading back button icon color
      leading: LMChatButton(
        onTap: () => Navigator.of(context).pop(),
        style: LMChatButtonStyle(
          icon: LMChatIcon(
            type: LMChatIconType.icon,
            icon: Icons.arrow_back,
            style: LMChatIconStyle(
              color: Colors.white, // White icon color
            ),
          ),
        ),
      ),
      // Customize trailing icons if needed (example: make them white)
      trailing: [
        // Add your existing trailing icons here, customizing their style
        // Example:
        // LMChatButton(
        //   onTap: () { /* Action */ },
        //   style: LMChatButtonStyle(
        //     icon: LMChatIcon(
        //       type: LMChatIconType.icon,
        //       icon: Icons.more_vert,
        //       style: LMChatIconStyle(
        //         color: Colors.white, // White icon color
        //       ),
        //     ),
        //   ),
        // ),
      ],
    );
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Call setup function before the runApp() function
  await LMChatCore.instance.initialize(
    // Configure the SDK with the custom builder delegate
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomAppBarBuilder(),
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
            // TODO: Replace with YOUR_API_KEY, YOUR_UUID, YOUR_USERNAME
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "YOUR_API_KEY",
              uuid: "YOUR_UUID",
              userName: "YOUR_USERNAME",
            );
            if (response.success) {
              // Navigate to the chatroom screen after successful login
              // TODO: Replace with YOUR_CHATROOM_ID
              int chatroomId = 0; // Replace with the actual chatroom ID
              if (chatroomId != 0) {
                MaterialPageRoute route = MaterialPageRoute(
                  builder: (context) => LMChatroomScreen(
                    chatroomId: chatroomId,
                  ),
                );
                Navigator.push(context, route);
              } else {
                // Or navigate to Home Screen if no specific chatroom ID
                MaterialPageRoute route = MaterialPageRoute(
                  builder: (context) => const LMChatHomeScreen(),
                );
                Navigator.pushReplacement(context, route);
              }
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optionally show a snackbar or dialog with the error
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                    content: Text(
                        'Error opening chat: ${response.errorMessage ?? 'Unknown error'}')),
              );
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}