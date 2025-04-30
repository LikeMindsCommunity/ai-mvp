import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom builder delegate for the Chatroom screen
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    int participantsCount, // Added missing parameter
  ) {
    // Return the original app bar but customize its style
    return appBar.copyWith(
      // Apply custom styling to the AppBar
      style: appBar.style?.copyWith(
        backgroundColor: Colors.purple, // Set AppBar background color to purple
      ),
      // Customize the title of the AppBar
      title: const LMChatText(
        'Custom Chatroom', // Set the custom title
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // Set title text color to white
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}

// Custom dark theme data
LMChatThemeData darkTheme = LMChatThemeData.dark(
  primaryColor: Colors.deepPurple, // Example dark theme primary color
  backgroundColor: Colors.grey[900], // Example dark theme background
  // Add other dark theme customizations as needed
);

// Custom light theme data
LMChatThemeData lightTheme = LMChatThemeData.light(
  primaryColor: Colors.purple, // Keep purple for light theme
  // Add other light theme customizations as needed
);

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK with custom configurations
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      // Provide the custom Chatroom builder delegate
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(),
      ),
    ),
    // Set the initial theme (e.g., light theme)
    theme: lightTheme,
  );

  // Determine initial theme mode (optional, could be based on system settings)
  // For demonstration, starting with light theme.
  // LMChatTheme.setTheme(lightTheme);

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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () async {
                // Store BuildContext before async call
                final navContext = context;
                // initiate user session with apiKey, uuid and userName
                // this is required to show the chat
                // TODO: Replace with YOUR_API_KEY, YOUR_UUID, YOUR_USERNAME
                LMResponse<void> response =
                    await LMChatCore.instance.showChatWithApiKey(
                  apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
                  uuid: "abc",
                  userName: "abc",
                );
                if (response.success) {
                  // Check if the context is still mounted before navigating
                  if (navContext.mounted) {
                    // create route with LMChatHomeScreen
                    MaterialPageRoute route = MaterialPageRoute(
                      builder: (context) => const LMChatHomeScreen(),
                    );
                    // navigate to LMChatHomeScreen
                    Navigator.pushReplacement(navContext, route);
                  }
                } else {
                  debugPrint("Error opening chat: ${response.errorMessage}");
                }
              },
              child: const Text('Open Chat'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Toggle theme by setting the dark theme
                LMChatTheme.setTheme(darkTheme);
                // You might need to trigger a rebuild of the MaterialApp
                // if the theme change should affect the whole app immediately.
                // This typically requires state management (like Provider, BLoC, etc.)
                // at a higher level to rebuild the MaterialApp.
                // For simplicity here, we just set the theme.
                // The chat screens will use the new theme when opened/rebuilt.
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Switched to Dark Theme')),
                );
              },
              child: const Text('Switch to Dark Theme'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Toggle theme by setting the light theme
                LMChatTheme.setTheme(lightTheme);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Switched to Light Theme')),
                );
              },
              child: const Text('Switch to Light Theme'),
            ),
          ],
        ),
      ),
    );
  }
}