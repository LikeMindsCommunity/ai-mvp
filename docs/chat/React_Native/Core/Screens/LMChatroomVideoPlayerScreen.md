---
sidebar_position: 8
title: Video Player Screen
slug: /react-native/core/screens/video-player-screen
---

## Overview

The `VideoPlayer` screen allows users to view and interact with video content within the LikeMinds chat application. It provides an intuitive interface for playing, pausing, and seeking through videos, enhancing the overall multimedia experience. This screen likely supports various video formats and offers additional features, such as fullscreen viewing and playback controls, ensuring users can enjoy video content seamlessly.

<img
src={require('../../../../static/img/reactNative/lmVideoPlayer.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Data Variables

- `url`: URL of the video to be rendered.

## Props

| Property | Type     | Description                        | Required           |
| -------- | -------- | ---------------------------------- | ------------------ |
| `url`    | `string` | The URL of the video to be played. | :heavy_check_mark: |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `VideoPlayer` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import { VIDEO_PLAYER, VideoPlayer, Themes } from "@likeminds.community/chat-rn-core";
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
      theme={<"SDK_THEME">} // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={"VideoPlayer"}
            component={VideoPlayer}
            initialParams={{ url: "" }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
