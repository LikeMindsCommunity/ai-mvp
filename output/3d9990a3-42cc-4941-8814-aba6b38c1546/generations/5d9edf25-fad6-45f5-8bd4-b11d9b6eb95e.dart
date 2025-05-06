import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Call setup function before the runApp() function
  await LMChatCore.instance.initialize();
  // run the app
  runApp(const MaterialApp(
    home: LMSampleChat(),
    debugShowCheckedModeBanner: false, // Add this line
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
            // TODO: Replace with YOUR_API_KEY
            // TODO: Replace with YOUR_UUID
            // TODO: Replace with YOUR_USERNAME
            LMResponse<void> response =
                await LMChatCore.instance.showChatWithApiKey(
              apiKey: "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8",
              uuid: "abc",
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
              // Optionally, show an error message to the user
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                      'Error opening chat: ${response.errorMessage ?? "Unknown error"}'),
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