import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Call setup function before the runApp() function
  await LMChatCore.instance.initialize();
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
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "YOUR_API_KEY", // TODO: Replace with YOUR_API_KEY
              uuid: "YOUR_USER_ID", // TODO: Replace with YOUR_USER_ID
              userName:
                  "YOUR_USER_NAME", // TODO: Replace with YOUR_USER_NAME
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
            }
          },
          child: const Text('Open Chat'),
        ),
      ),
    );
  }
}