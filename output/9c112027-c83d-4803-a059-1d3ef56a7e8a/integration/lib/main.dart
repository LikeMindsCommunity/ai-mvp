import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom Builder Delegate extending LMChatroomBuilderDelegate
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Added participantsCount parameter
  ) {
    return appBar.copyWith(
      title: const Text("custom chatroom"), // Updated title
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Updated color
      ),
    );
  }
}

// Create an instance of LMChatThemeData using the dark theme constructor
LMChatThemeData customChatTheme = LMChatThemeData.dark(
  primaryColor: Colors.purple, // Set primary color to purple for dark theme
  backgroundColor: Colors.black, // Example dark background color
  buttonStyle: LMChatButtonStyle.basic().copyWith(
    backgroundColor: Colors.purple,
    textStyle: const TextStyle(color: Colors.white),
  ),
);

// Create a custom configuration with the custom builder
LMChatConfig customConfig = LMChatConfig(
  chatRoomConfig: LMChatroomConfig(
    builder: CustomChatroomBuilder(),
  ),
);

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK with the custom theme and config
  await LMChatCore.instance.initialize(
    theme: customChatTheme,
    config: customConfig,
  );

  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: false, // Hide debug mode banner
      home: const LMSampleChat(),
      theme: ThemeData.dark(), // Apply dark theme to the app
      darkTheme: ThemeData.dark(), // Specify dark theme data
      themeMode: ThemeMode.dark, // Force dark mode
    ),
  );
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
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              // TODO: Replace with YOUR_API_KEY
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
              // TODO: Replace with YOUR_UUID
              uuid: "abc",
              // TODO: Replace with YOUR_USERNAME
              userName: "abc",
            );

            // Check if the widget is still mounted before using the context
            if (!context.mounted) return;

            if (response.success) {
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Optionally show a snackbar or dialog if the context is still valid
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                      content: Text(
                          "Error opening chat: ${response.errorMessage}")),
                );
              }
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}