---
sidebar_position: 1
title: Network Chat Screen
slug: /react-native/core/screens/network-chat-screen
---

## Overview

The `NetworkChat` screen is the central hub for users in the LikeMinds chat application, displaying a dynamic feed of messages, posts, and updates from connections in your network.

<img
src={require('../../../../static/img/reactNative/networking_chat.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [ChatroomItem](../Components/LMChatroomHomeFeedItem.md)

## Data Variables

- `user`: It stores the logged-in user data.
- `tokens`: This screen does all the initialisation API calls, and store tokens received in response.
- `chatrooms`: It holds the chatrooms data which is then rendered as list of chatrooms.

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add the `LMChatNetworkChatroomsScreen` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import { Themes, NetworkChatScreen, ScreenName } from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={Themes.NETWORK} // // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name={ScreenName.NetworkChatScreen} component={NetworkChatScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```