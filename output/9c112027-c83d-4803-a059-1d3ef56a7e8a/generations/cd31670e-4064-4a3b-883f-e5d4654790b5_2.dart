import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Custom Builder Delegate to override the default AppBar
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom,
    LMChatAppBar appBar,
    // Add the missing participantsCount parameter
    int participantsCount,
  ) {
    // Use copyWith on the default AppBar to modify title and background color
    return appBar.copyWith(
      title: const Text(
        "custom chatroom",
        style: TextStyle(
          color: Colors.white, // Set title color to white for better contrast
        ),
      ),
      style: (appBar.style ?? const LMChatAppBarStyle()).copyWith(
        backgroundColor: Colors.purple, // Set AppBar background to purple
      ),
    );
  }
}

// Custom Chat Theme Data for Dark Mode
LMChatThemeData darkTheme = LMChatThemeData.dark(
    // You can further customize dark theme colors and styles here if needed
    // For example:
    // primaryColor: Colors.deepPurple,
    // backgroundColor: Colors.black,
    );

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK with the custom builder and dark theme
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      chatRoomConfig: LMChatroomConfig(
        builder: CustomChatroomBuilder(), // Inject the custom builder
      ),
    ),
    theme: darkTheme, // Apply the dark theme
  );

  // Run the app
  runApp(const MaterialApp(
    debugShowCheckedModeBanner: false, // Hide debug banner
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
            // Initiate user session with apiKey, uuid and userName
            // this is required to show the chat
            // TODO: Replace with YOUR_API_KEY
            // TODO: Replace with YOUR_UUID
            // TODO: Replace with YOUR_USERNAME
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8", // API Key
              uuid: "abc", // User Unique ID
              userName: "abc", // User Name
            );

            // Check if the context is still mounted before navigating
            if (!context.mounted) return;

            if (response.success) {
              // Create route with LMChatHomeScreen
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              // Navigate to LMChatHomeScreen
              Navigator.pushReplacement(context, route);
            } else {
              // Handle error, e.g., show a snackbar or log the error
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      "Error opening chat: ${response.errorMessage ?? 'Unknown error'}"),
                ),
              );
              debugPrint("Error opening chat: ${response.errorMessage}");
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}