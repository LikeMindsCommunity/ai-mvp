import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// --- Step 1: Define a Custom Chatroom Builder Delegate ---
// Extend LMChatroomBuilderDelegate to override specific builders.
class CustomChatroomBuilder extends LMChatroomBuilderDelegate {
  // Override appBarBuilder to customize the Chatroom Screen's AppBar.
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    LMChatRoomViewData chatroom, // Data for the current chatroom
    LMChatAppBar appBar, // The default AppBar widget provided by the SDK
  ) {
    // Use copyWith to modify the default AppBar.
    // Here, we change the title and add a custom action button.
    return appBar.copyWith(
      title: LMChatText(
        'Custom Title: ${chatroom.header}', // Use chatroom data in the title
        style: LMChatTextStyle(
          textStyle: TextStyle(
            color: Colors.white, // Change title color
            fontSize: 18,
          ),
        ),
      ),
      backgroundColor: Colors.deepPurple, // Change AppBar background color
      actions: [
        IconButton(
          icon: LMChatIcon(
            type: LMChatIconType.icon,
            icon: Icons.settings,
            style: LMChatIconStyle(color: Colors.white),
          ),
          onPressed: () {
            // TODO: Implement your custom settings action
            print('Custom settings button tapped for chatroom: ${chatroom.id}');
            ScaffoldMessenger.of(context).showSnackBar(
              LMChatSnackBar(
                  content: LMChatText('Custom Settings Action!')),
            );
          },
        ),
        // Keep existing actions if needed, or replace them entirely.
        ...?appBar.actions, // Optional: Include default actions
      ],
    );
  }

  // You can override other builders here as needed, e.g., sendButton:
  // @override
  // Widget sendButton(...) { ... }
}

// --- Step 2: Create Custom Configuration Objects ---
// Create an instance of your custom builder.
final customChatroomBuilder = CustomChatroomBuilder();

// Create an LMChatroomConfig with the custom builder.
// You can also provide custom settings and styles if needed.
final customChatroomConfig = LMChatroomConfig(
  builder: customChatroomBuilder,
  // setting: LMChatroomSetting(), // Optional: Add custom settings
  // style: LMChatroomStyle(),    // Optional: Add custom styles
);

// Create an LMChatConfig to hold the chatroom configuration.
final customConfig = LMChatConfig(
  chatroomConfig: customChatroomConfig,
  // Add other screen configs if needed (e.g., homeConfig, exploreConfig)
);


Future<void> main() async {
  // Ensure Flutter bindings are initialized.
  WidgetsFlutterBinding.ensureInitialized();

  // --- Step 3: Initialize LMChatCore with Custom Configuration ---
  // Initialize the LikeMinds Chat SDK, passing the custom configuration.
  await LMChatCore.instance.initialize(
    config: customConfig, // Pass the config with your customizations
    // Optional: Add theme, analytics listener, or callbacks if needed
    // theme: LMChatThemeData.light(),
    // analyticsListener: (event) { print(event.eventName); },
    // lmChatCallback: LMChatCoreCallback(...),
  );

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LikeMinds Chat Demo',
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // --- Step 4: Initiate User Session ---
            // Use showChatWithApiKey for client-side authentication.
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "YOUR_API_KEY", // TODO: Replace with YOUR_API_KEY
              uuid: "YOUR_USER_UNIQUE_ID", // TODO: Replace with user's unique ID
              userName: "YOUR_USER_NAME", // TODO: Replace with user's name
              // Optional parameters:
              // isGuest: false,
              // imageUrl: "USER_IMAGE_URL",
            );

            // --- Step 5: Navigate to Chat Home Screen on Success ---
            if (response.success) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  // Navigate to the SDK's Home Screen.
                  builder: (context) => const LMChatHomeScreen(),
                  // Example: Navigating directly to a specific Chatroom Screen
                  // Make sure the chatroomId exists.
                  // builder: (context) => LMChatroomScreen(
                  //   chatroomId: 0, // TODO: Replace with YOUR_CHATROOM_ID
                  // ),
                ),
              );
            } else {
              // Handle initiation error
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      'Error initiating chat: ${response.errorMessage ?? 'Unknown error'}'),
                ),
              );
            }
          },
          child: Text('Login & Start Chat'),
        ),
      ),
    );
  }
}