<file path="pubspec.yaml">
name: temp
description: "A new Flutter project."
# The following line prevents the package from being accidentally published to
# pub.dev using `flutter pub publish`. This is preferred for private packages.
publish_to: 'none' # Remove this line if you wish to publish to pub.dev

# The following defines the version and build number for your application.
# A version number is three numbers separated by dots, like 1.2.43
# followed by an optional build number separated by a +.
# Both the version and the builder number may be overridden in flutter
# build by specifying --build-name and --build-number, respectively.
# In Android, build-name is used as versionName while build-number used as versionCode.
# Read more about Android versioning at https://developer.android.com/studio/build/application-id.html
# In iOS, build-name is used as CFBundleShortVersionString while build-number is used as CFBundleVersion.
# Read more about iOS versioning at
# https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/CoreFoundationKeys.html
# In Windows, build-name is used as the major, minor, and patch parts
# of the product and file versions while build-number is used as the build suffix.
version: 1.0.0+1

environment:
  sdk: '>=3.7.2 <4.0.0'

# Dependencies specify other packages that your package needs in order to work.
# To automatically upgrade your package dependencies to the latest versions
# consider running `flutter pub upgrade --major-versions`. Alternatively,
# dependencies can be manually updated by changing the version numbers below to
# the latest version available on pub.dev. To see which dependencies have newer
# versions available, run `flutter pub outdated`.
dependencies:
  flutter:
    sdk: flutter

  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.8
  
  # Add the LikeMinds Chat SDK dependency
  likeminds_chat_flutter_core: ^0.15.0

dev_dependencies:
  flutter_test:
    sdk: flutter

  # The "flutter_lints" package below contains a set of recommended lints to
  # encourage good coding practices. The lint set provided by the package is
  # activated in the `analysis_options.yaml` file located at the root of your
  # package. See that file for information about deactivating specific lint
  # rules and activating additional ones.
  flutter_lints: ^5.0.0

# For information on the generic Dart part of this file, see the
# following page: https://dart.dev/tools/pub/pubspec

# The following section is specific to Flutter packages.
flutter:

  # The following line ensures that the Material Icons font is
  # included with your application, so that you can use the icons in
  # the material Icons class.
  uses-material-design: true

  # To add assets to your application, add an assets section, like this:
  # assets:
  #   - images/a_dot_burr.jpeg
  #   - images/a_dot_ham.jpeg

  # An image asset can refer to one or more resolution-specific "variants", see
  # https://flutter.dev/to/resolution-aware-images

  # For details regarding adding assets from package dependencies, see
  # https://flutter.dev/to/asset-from-package

  # To add custom fonts to your application, add a fonts section here,
  # in this "flutter" section. Each entry in this list should have a
  # "family" key with the font family name, and a "fonts" key with a
  # list giving the asset and other descriptors for the font. For
  # example:
  # fonts:
  #   - family: Schyler
  #     fonts:
  #       - asset: fonts/Schyler-Regular.ttf
  #       - asset: fonts/Schyler-Italic.ttf
  #         style: italic
  #   - family: Trajan Pro
  #     fonts:
  #       - asset: fonts/TrajanPro.ttf
  #       - asset: fonts/TrajanPro_Bold.ttf
  #         weight: 700
  #
  # For details regarding fonts from package dependencies,
  # see https://flutter.dev/to/font-from-package
</file>

<file path="lib/main.dart">
import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';
import 'package:temp/screens/chat_initiation_screen.dart'; // Import the new initiation screen

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize LikeMinds Chat SDK
  await LMChatCore.instance.initialize();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Flutter Demo',
      // Set the home to the ChatInitiationScreen
      home: ChatInitiationScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
</file>

<file path="lib/screens/chat_initiation_screen.dart">
import 'package:flutter/material.dart';
import 'package:likeminds_chat_flutter_core/likeminds_chat_flutter_core.dart';

class ChatInitiationScreen extends StatefulWidget {
  const ChatInitiationScreen({super.key});

  @override
  State<ChatInitiationScreen> createState() => _ChatInitiationScreenState();
}

class _ChatInitiationScreenState extends State<ChatInitiationScreen> {
  bool _isLoading = false;
  String _errorMessage = '';

  // Function to initiate LikeMinds user and navigate
  Future<void> _initiateAndNavigateToChat() async {
    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });

    // TODO: Replace with YOUR_API_KEY
    const String apiKey = "83c8f0ed-a9e2-4634-9a2e-d9c7a1e39ff8";
    // TODO: Replace with YOUR_USER_ID
    const String userId = "abc";
    // TODO: Replace with YOUR_USER_NAME
    const String userName = "abc";

    // Initiate user session using API Key
    LMResponse<void> response = await LMChatCore.instance.showChatWithApiKey(
      apiKey: apiKey,
      uuid: userId,
      userName: userName,
      // Optional: imageUrl, isGuest
    );

    if (response.success) {
      // Navigate to the main chat screen provided by the SDK
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => const LMChatHomeScreen(),
        ),
      );
    } else {
      // Handle initiation error
      setState(() {
        _isLoading = false;
        _errorMessage = response.errorMessage ?? 'Failed to initiate chat.';
      });
      debugPrint("Error initiating chat: ${response.errorMessage}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat Integration Demo'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: _isLoading
            ? const CircularProgressIndicator()
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text(
                    'Tap the button below to open the chat screen:',
                  ),
                  if (_errorMessage.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        'Error: $_errorMessage',
                        style: const TextStyle(color: Colors.red),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _initiateAndNavigateToChat,
                    child: const Text('Open LikeMinds Chat'),
                  ),
                ],
              ),
      ),
    );
  }
}
</file>