import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

// Step 1: Define your custom Participant Builder Delegate
class CustomParticipantBuilder extends LMChatParticipantBuilderDelegate {
  // Step 2: Override the userTileBuilder method
  @override
  Widget userTileBuilder(BuildContext context, LMChatUserViewData user) {
    // You can return any custom widget here based on the user data.
    // For example, customize the default LMChatUserTile or build a completely new one.

    // Example 1: Using the default LMChatUserTile but changing the onTap behavior
    // return LMChatUserTile(
    //   userViewData: user,
    //   onTap: () {
    //     print("Custom tap action for user: ${user.name}");
    //     // Add custom navigation or action here
    //   },
    //   // You could potentially customize the style as well if LMChatTileStyle is available
    //   // style: LMChatTileStyle( ... ), // Requires LMChatTileStyle definition from context
    // );

    // Example 2: Building a completely custom tile using ListTile
    return ListTile(
      leading: LMChatProfilePicture(
        user: user, // Use the user data for the profile picture
        size: 40,
      ),
      title: Text(
        'Participant: ${user.name}', // Customize the title text
        style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue),
      ),
      subtitle: Text(user.customTitle ?? 'No custom title'), // Display custom title if available
      trailing: const Icon(Icons.star, color: Colors.amber), // Add a custom trailing icon
      onTap: () {
        print("Custom ListTile tap for user: ${user.name}");
        // Add custom action
      },
    );
  }

  // You can override other builders like appBarBuilder if needed
  // @override
  // PreferredSizeWidget appBarBuilder(
  //   BuildContext context,
  //   TextEditingController searchController,
  //   VoidCallback onSearch,
  //   LMChatAppBar appBar,
  // ) {
  //   // Example: Customize the AppBar
  //   return appBar.copyWith(
  //     title: const Text("Our Awesome Participants"),
  //     backgroundColor: Colors.purple,
  //   );
  // }
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Step 3: Create an instance of the Participant Config with the custom builder
  final participantConfig = LMChatParticipantConfig(
    builder: CustomParticipantBuilder(),
    // Optionally provide custom style or settings if needed
    // style: LMChatParticipantStyle(),
    // setting: LMChatParticipantSetting(),
  );

  // Step 4: Initialize LMChatCore with the custom Participant Config
  await LMChatCore.instance.initialize(
    config: LMChatConfig(
      participantConfig: participantConfig,
      // Add other configurations if necessary
    ),
    // lmChatCallback: LMChatCallback(
    //   accessToken: () => "YOUR_ACCESS_TOKEN", // TODO: Replace if using Server-Side Auth
    //   refreshToken: () => "YOUR_REFRESH_TOKEN", // TODO: Replace if using Server-Side Auth
    // ),
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LikeMinds Participant Tile Customization Demo',
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LikeMinds Demo'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // Initiate session (replace with your actual initiation logic)
            final response = await LMChatCore.instance.showChatWithApiKey(
              context,
              apiKey: "YOUR_API_KEY", // TODO: Replace with YOUR_API_KEY
              userName: "Test User", // TODO: Replace with the user's name
              uuid: "test-user-unique-id-participant", // TODO: Replace with a unique user ID
            );

            if (!response.isSuccess) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      'Failed to initialize chat: ${response.errorMessage ?? "Unknown error"}'),
                ),
              );
            }
            // On success, the SDK navigates internally.
            // To see the customized participants screen, navigate to a chatroom
            // and then view its participants list.
          },
          child: const Text('Launch Chat & Go to Participants'),
        ),
      ),
    );
  }
}

// Note: To see the customized participant tile, you need to:
// 1. Launch the chat using the button above.
// 2. Navigate into any chatroom from the LMChatHomeScreen.
// 3. Open the participants list for that chatroom (e.g., by tapping the chatroom header/title).
// The user tiles on that screen will now be rendered using your `CustomParticipantBuilder.userTileBuilder`.