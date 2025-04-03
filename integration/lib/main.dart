import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:likeminds_chat_flutter_ui/likeminds_chat_flutter_ui.dart'; // Import UI package for LMChatUserTile if needed

// Custom Builder Delegate for Participants Screen
class CustomParticipantBuilder extends LMChatParticipantBuilderDelegate {
  @override
  Widget userTileBuilder(
    BuildContext context,
    LMChatUserViewData user,
    LMChatUserTile tile,
  ) {
    // Example: Return a customized ListTile for each participant
    // You can use the provided 'user' data (LMChatUserViewData)
    // to build your custom tile.
    // You can also instantiate and customize the default LMChatUserTile if needed:
    // return LMChatUserTile(
    //   userViewData: user,
    //   style: LMChatTileStyle(
    //     backgroundColor: Colors.lightBlue[50],
    //     // Add other style customizations
    //   ),
    //   onTap: () {
    //     // Handle tap if needed
    //     debugPrint("Tapped on user: ${user.name}");
    //   },
    // );

    // Or return a completely custom widget:
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 4.0, horizontal: 8.0),
      child: ListTile(
        leading: CircleAvatar(
          // Use user.imageUrl or a placeholder
          backgroundImage:
              user.imageUrl != null && user.imageUrl!.isNotEmpty
                  ? NetworkImage(user.imageUrl!)
                  : null,
          child:
              user.imageUrl == null || user.imageUrl!.isEmpty
                  ? Text(
                    user.name.isNotEmpty ? user.name[0].toUpperCase() : '?',
                  )
                  : null,
        ),
        title: Text(
          'Custom: ${user.name}', // Example: Add "Custom: " prefix
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.purple,
          ),
        ),
        subtitle: Text(user.customTitle ?? 'Community Member'),
        trailing: const Icon(Icons.star, color: Colors.amber),
        onTap: () {
          debugPrint("Custom tap on user: ${user.name}");
          // Default tap action (like opening profile) might be overridden
          // unless you specifically call the default behavior if accessible.
        },
      ),
    );
  }

  // You can override other builders as well, like appBarBuilder
  @override
  PreferredSizeWidget appBarBuilder(
    BuildContext context,
    TextEditingController searchController,
    VoidCallback onSearch,
    LMChatAppBar appBar,
  ) {
    // Example: Customize the AppBar title
    return appBar.copyWith(title: const Text('Our Awesome Participants'));
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // --- Configuration Steps ---
  // 1. Create an instance of your custom builder delegate
  final customParticipantBuilder = CustomParticipantBuilder();

  // 2. Create the config object for the participants screen
  final participantConfig = LMChatParticipantConfig(
    builder: customParticipantBuilder,
    // You can also provide custom Style and Setting objects here if needed
    // style: LMChatParticipantStyle(),
    // setting: LMChatParticipantSetting(),
  );

  // 3. Create the main config and inject the participant config
  final lmChatConfig = LMChatConfig(participantConfig: participantConfig);

  // 4. Initialize the SDK with the custom configuration
  await LMChatCore.instance.initialize(
    config: lmChatConfig,
    // Add lmChatCallback if needed for token handling
  );
  // --- End Configuration Steps ---

  runApp(const MaterialApp(home: LMSampleChat()));
}

class LMSampleChat extends StatelessWidget {
  const LMSampleChat({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('LM Sample Chat')),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // initiate user session with apiKey, uuid and userName
            LMResponse<void>
            response = await LMChatCore.instance.showChatWithApiKey(
              apiKey: "YOUR_API_KEY", // TODO: Replace with YOUR_API_KEY
              uuid: "YOUR_USER_UNIQUE_ID", // TODO: Replace with YOUR_USER_ID
              userName:
                  "YOUR_USER_DISPLAY_NAME", // TODO: Replace with user's name
            );
            if (response.success) {
              // Navigate to LMChatHomeScreen upon successful session initiation
              // From LMChatHomeScreen, the user can navigate to a specific chatroom
              // and then access the Participants Screen via the chatroom menu.
              MaterialPageRoute route = MaterialPageRoute(
                builder: (context) => const LMChatHomeScreen(),
              );
              Navigator.pushReplacement(context, route);
            } else {
              debugPrint("Error opening chat: ${response.errorMessage}");
              // Handle error, e.g., show a SnackBar
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                    'Error initiating chat: ${response.errorMessage ?? 'Unknown error'}',
                  ),
                ),
              );
            }
          },
          child: const Text('Open Chat Home'),
        ),
      ),
    );
  }
}

// Note: To see the customized Participants Screen, you need to:
// 1. Run this app.
// 2. Click 'Open Chat Home'.
// 3. Navigate into a chatroom from the home screen.
// 4. Open the chatroom details/menu (usually via an AppBar icon).
// 5. Select the option to view participants.
// You should then see the participants list rendered using your custom `userTileBuilder`.
