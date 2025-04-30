import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

Future<void> main() async {
  // Ensure Flutter bindings are initialized
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK before running the app
  await LMChatCore.instance.initialize();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LikeMinds Chat Demo', // Updated title
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      // Start with MyHomePage, which will handle navigation to chat
      home: const MyHomePage(title: 'LikeMinds Chat Demo Home Page'),
      debugShowCheckedModeBanner: false, // Add this line
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0; // Keep the counter state for example purposes

  // --- Function to initiate user and navigate ---
  Future<void> _openChat(BuildContext context) async {
    // Use the API Key method from the documentation
    // Using example credentials provided in the context
    // TODO: Replace with YOUR_API_KEY
    const String apiKey = "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8";
    // TODO: Replace with YOUR_USER_UNIQUE_ID
    const String uuid = "abc";
    // TODO: Replace with YOUR_USER_NAME
    const String userName = "abc";

    LMResponse<void> response = await LMChatCore.instance.showChatWithApiKey(
      apiKey: apiKey,
      uuid: uuid,
      userName: userName,
    );

    if (response.success) {
      // If initiation is successful, navigate to the LMChatHomeScreen
      // Ensure context is still valid before navigating
      if (!context.mounted) return;
      Navigator.pushReplacement( // Use pushReplacement to replace the current screen
        context,
        MaterialPageRoute(
          builder: (context) => const LMChatHomeScreen(),
        ),
      );
    } else {
      // Handle errors, e.g., show a Snackbar
      // Ensure context is still valid before showing Snackbar
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
              'Error initiating chat: ${response.errorMessage ?? 'Unknown error'}'),
          backgroundColor: Colors.red,
        ),
      );
      debugPrint("Error opening chat: ${response.errorMessage}");
    }
  }
  // --- End of function ---

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          //
          // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
          // action in the IDE, or press "p" in the console), to see the
          // wireframe for each widget.
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter', // Still showing the counter as an example
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 20), // Add some space
            ElevatedButton( // Added an ElevatedButton as another option
              onPressed: () => _openChat(context),
              child: const Text('Open LikeMinds Chat'),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _openChat(context), // Changed onPressed to call _openChat
        tooltip: 'Open Chat', // Changed tooltip
        child: const Icon(Icons.chat), // Changed icon
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}