---
sidebar_position: 1
title: Getting Started
slug: /react-native/getting-started
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Getting started

This Getting started will walk you through the process of setting up a chat application using a two-layer architecture: Core Integration layer and Data layer.

## Prerequisites

Before you begin, make sure you have the following installed:

- Node.js and npm (Node Package Manager)
- React Native CLI
- Xcode (for iOS development)
- Android Studio (for Android development)
- LikeMinds API Key: Sign up on the [LikeMinds dashboard](https://docs.likeminds.community/chat/#generate-api-key) and obtain an API key for your application.

## Step-by-Step Integration Guide

Follow these steps to integrate the LikeMinds Chat SDK into your React Native application using NPM:

### Step 1 - Adding Dependency

LikeMinds Chat SDK has a number of peer dependencies that are required to take advantage of all of the out of the box features. It is suggested you follow the install instructions for each package to ensure it is properly setup. Most if not all of the required packages now support auto-linking so setup should be minimal.

```bash
# Add LikeMinds Chat React Native SDK
npm install @likeminds.community/chat-rn-core@latest @likeminds.community/chat-rn@latest

## Setup up react native firebase for notifications, don't setup if it's already done. Do checkout react native firebase docs
npm install @react-native-firebase/app @react-native-firebase/messaging @notifee/react-native

## Add react navigation dependencies, don't install if already installed
npm install @react-navigation/material-top-tabs @react-navigation/native @react-navigation/native-stack @react-navigation/stack react-native-safe-area-context react-native-screens

# Add the listed dependencies
npm install @react-native-community/datetimepicker @react-native/babel-preset@0.74.0 @shopify/flash-list @types/react-native-video aws-sdk buffer diff@5.1.0 firebase moment react-native-blob-util react-native-compressor react-native-create-thumbnail react-native-device-info react-native-gesture-handler react-native-image-crop-tools react-native-image-picker react-native-linear-gradient react-native-media-console react-native-pager-view react-native-pdf-thumbnail react-native-permissions react-native-reanimated react-native-shimmer-placeholder react-native-swiper-flatlist react-native-tab-view react-native-uuid react-native-video realm@11.10.2 rn-emoji-keyboard react-native-document-picker react-native-svg @react-native-community/netinfo

# Install Pods (iOS only)
npx pod-install
```

#### Add Optional Dependencies

#### Giphy

Enables the full GIPHY experience directly to your app with the GIPHY SDK.

```bash
npm install @giphy/react-native-sdk
```

#### Audio Player

Installing this package allows you to play the voice note attachments in the chat.

```bash
npm install react-native-track-player
```

#### Slider

Installing this package allows you to interact with the slider of voice note attachments in the chat.

```bash
npm install @react-native-community/slider
```

#### Lottie

Installing this package will allow your users to see audio record animation.

```bash
npm install lottie-react-native
```

#### Audio Recorder

Installing this package will allow your users to record voice note.

```bash
npm install react-native-audio-recorder-player
```

#### Copying messages

Adds ability to copy messages to the clipboard.

```bash
npm install @react-native-clipboard/clipboard
```

### Step 2 - Setup LikeMinds Chat

To start using the package, import the `initMyClient()` method in your `App.tsx` or `App.js` file, this methods takes in 3 optional parameters

| Parameter            | Type                                                    | Description                                                       |
| -------------------- | ------------------------------------------------------- | ----------------------------------------------------------------- |
| `filterStateMessage` | ConversationState[]                                     | An optional array of Conversation State to filter state messages. |
| `shareLogsWithLM`    | `boolean`                                               | Determines whether error logs should be shared with LikeMinds.    |
| `onErrorHandler`     | `(exception: string, stackTrace: LMStackTrace) => void` | A callback function executed when an error occurs.                |

```ts
import { initMyClient } from "@likeminds.community/chat-rn-core";

export const lmChatClient = initMyClient();
// To initiate user session, follow step 3
```

:::tip
To check how to filter state Messages, Navigate to this [doc](./Core/Guides/how-to-use-filter-state-message-in-chatroom/how-to-use-filter-state-message-in-chatroom.md)
:::

:::tip
If you are using the AI Chatbot theme, please go to the dashboard and follow these steps

1. **Open** your LikeMinds [Admin Dashboard](https://dashboard.likeminds.community.com).
2. **Navigate** to the AI [Chatbot Section](https://dashboard.likeminds.community/chat/chatbot).
3. **Follow** the steps promoted on the section.

:::

### Step 3 - Initiate User Session

<Tabs>
<TabItem value="all-chat-theme" label="All Chat Theme">

You have successfully initiated `LMChatClient`, now all you need to do is inflate the Chat Screen based on one of the themes below.

| Theme              | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| `COMMUNITY`        | Designed for community-based use cases such as group chats.                 |
| `NETWORKING`       | Tailored for networking scenarios, focusing on direct messages (DMs).       |
| `COMMUNITY_HYBRID` | Combines features of community and networking for both group chats and DMs. |

- Provide the API Key directly to the LikeMinds Chat SDK to initiate a user session.
- Pass the following parameters to `<LMOverlayProvider />` from `@likeminds.community/chat-rn-core`:
  - `apiKey`
  - `userName`
  - `uuid`
  - `theme`

```tsx
import {
  LMOverlayProvider,
  initMyClient,
  Themes
} from "@likeminds.community/chat-rn-core";
import { LMCoreCallbacks } from "@likeminds.community/chat-rn-core/ChatSX/setupChat";
import { GestureHandlerRootView } from "react-native-gesture-handler";

const App = () => {
  const [myClient, setMyClient] = useState<any>();
  const apiKey = "<YOUR_API_KEY>";
  const userName = "<USER_NAME>";
  const uuid = "<USER_ID>";
  const theme = <"SDK_THEME">

  useEffect(() => {
    async function generateClient() {
      // Initiate LMChatClient as described in step 2
      const res: any = initMyClient();
      setMyClient(res);
    }
    generateClient();
  }, []);

  return (
    <GestureHandlerRootView style={{flex: 1}}>
      {userName && uuid && apiKey && myClient ? (
        <LMOverlayProvider
          myClient={myClient}
          apiKey={apiKey}
          userName={userName}
          userUniqueId={uuid}
          theme={theme}
        >
          {/* Follow step 4 to add navigation logic after user is successfully initiated with LM servers */}
        </LMOverlayProvider>
      ) : null}
    </GestureHandlerRootView>
  );
};

export default App;
```

</TabItem>
<TabItem value="ai-chat-theme" label="AI Chatbot Theme">

You have successfully initiated `LMChatClient`. Now before initiating the Chatbot, you need to initiate a user session and navigate to the chatroom with the Chatbot:

1. Provide the necessary user details to the LikeMinds Chat SDK to initiate a user session.
2. Pass the instance of the initiated `LMChatClient` to `<LMChatBotOverlayProvider />` imported from `@likeminds.community/chat-rn-core`:

```tsx
import {
  LMChatBotOverlayProvider,
  initMyClient,
} from "@likeminds.community/chat-rn-core";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { ConversationState } from "@likeminds.community/chat-rn";

const App = () => {
  const [myClient, setMyClient] = useState<any>();

  useEffect(() => {
    async function generateClient() {
      // Initiate LMChatClient as described in step 2
      const res: any = initMyClient();
      setMyClient(res);
    }
    generateClient();
  }, []);

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      {myClient ? (
        <LMChatBotOverlayProvider myClient={myClient}>
          {/* Follow step 4 & 5 to add navigation logic after user is successfully initiated with LM servers */}
        </LMChatBotOverlayProvider>
      ) : null}
    </GestureHandlerRootView>
  );
};

export default App;
```

</TabItem>
</Tabs>

### Step 4 - Configure Navigation

<Tabs>
<TabItem value="CommunityTheme" label="Community Theme">

Set up the navigation for your application using React Navigation. Create a `StackNavigator` in your `App.js` or equivalent file:

```tsx
import React from "react";
import { Platform } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  CarouselScreen,
  CreatePollScreen,
  ImageCropScreen,
  PollResult,
  VideoPlayer,
  ExploreFeed,
  HomeFeed,
  LMOverlayProvider,
  ReportScreen,
  ImageScreen,
  ViewParticipants,
  AddParticipants,
  DmAllMembers,
  SearchInChatroom,
  CommunityChatScreen,
  ScreenName,
  FileUploadScreenWrapper,
  ChatroomScreenWrapper,
} from "@likeminds.community/chat-rn-core";

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator initialRouteName={ScreenName.CommunityChatScreen}>
          <Stack.Screen
            name={ScreenName.CommunityChatScreen}
            component={CommunityChatScreen}
          />
          <Stack.Screen
            name={ScreenName.SearchInChatroom}
            component={SearchInChatroom}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={ScreenName.ExploreFeed}
            component={ExploreFeed}
            initialParams={{
              backIconPath: "",
              filterIconPath: "",
              participantsIconPath: "",
              totalMessagesIconPath: "",
              joinButtonPath: "",
              joinedButtonPath: "",
            }}
          />
          <Stack.Screen
            name={ScreenName.Chatroom}
            component={ChatroomScreenWrapper}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
          />
          <Stack.Screen
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
            name={ScreenName.FileUpload}
            component={FileUploadScreenWrapper}
            initialParams={{
              backIconPath: "", // add your back icon path here
              imageCropIcon: "", // add your image crop icon path here
            }}
          />
          <Stack.Screen name={ScreenName.VideoPlayer} component={VideoPlayer} />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={ScreenName.CarouselScreen}
            component={CarouselScreen}
            initialParams={{
              backIconPath: "", // add your back icon path here
            }}
          />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={ScreenName.PollResult}
            component={PollResult}
          />
          <Stack.Screen
            name={ScreenName.CreatePollScreen}
            component={CreatePollScreen}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name={ScreenName.ImageCropScreen}
            component={ImageCropScreen}
          />
          <Stack.Screen name={ScreenName.Report} component={ReportScreen} />
          <Stack.Screen name={ScreenName.ImageScreen} component={ImageScreen} />
          <Stack.Screen
            name={ScreenName.ViewParticipants}
            component={ViewParticipants}
          />
          <Stack.Screen
            name={ScreenName.AddParticipants}
            component={AddParticipants}
          />
          <Stack.Screen
            name={ScreenName.DmAllMembers}
            component={DmAllMembers}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

</TabItem>
<TabItem value="NetworkingTheme" label="Networking Theme">

Set up the navigation for your application using React Navigation. Create a `StackNavigator` in your `App.js` or equivalent file:

```tsx
import React from "react";
import { Platform } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  CarouselScreen,
  CreatePollScreen,
  ImageCropScreen,
  PollResult,
  VideoPlayer,
  ExploreFeed,
  HomeFeed,
  LMOverlayProvider,
  ReportScreen,
  ImageScreen,
  ViewParticipants,
  AddParticipants,
  DmAllMembers,
  SearchInChatroom,
  NetworkChatScreen,
  ScreenName,
  FileUploadScreenWrapper,
  ChatroomScreenWrapper,
} from "@likeminds.community/chat-rn-core";

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator initialRouteName={ScreenName.NetworkChatScreen}>
          <Stack.Screen
            name={ScreenName.NetworkChatScreen}
            component={NetworkChatScreen}
          />
          <Stack.Screen
            name={ScreenName.SearchInChatroom}
            component={SearchInChatroom}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={ScreenName.Chatroom}
            component={ChatroomScreenWrapper}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
          />
          <Stack.Screen
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
            name={ScreenName.FileUpload}
            component={FileUploadScreenWrapper}
            initialParams={{
              backIconPath: "", // add your back icon path here
              imageCropIcon: "", // add your image crop icon path here
            }}
          />
          <Stack.Screen name={ScreenName.VideoPlayer} component={VideoPlayer} />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={ScreenName.CarouselScreen}
            component={CarouselScreen}
            initialParams={{
              backIconPath: "", // add your back icon path here
            }}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name={ScreenName.ImageCropScreen}
            component={ImageCropScreen}
          />
          <Stack.Screen name={ScreenName.Report} component={ReportScreen} />
          <Stack.Screen name={ScreenName.ImageScreen} component={ImageScreen} />
          <Stack.Screen
            name={ScreenName.DmAllMembers}
            component={DmAllMembers}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

:::info

1. By default, only Members to Community Managers and visa versa direct messages are allowed, to enable direct messages for all Members, Enable **Members can DM other members** from LikeMinds Dashboard's [Chat Setting Section](https://dashboard.likeminds.community/chat/settings).

:::

</TabItem>
<TabItem value="CommunityHybridTheme" label="Community Hybrid Theme">

Set up the navigation for your application using React Navigation. Create a `StackNavigator` in your `App.js` or equivalent file:

```tsx
import React from "react";
import { Platform } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  CarouselScreen,
  CreatePollScreen,
  ImageCropScreen,
  PollResult,
  VideoPlayer,
  ExploreFeed,
  HomeFeed,
  LMOverlayProvider,
  ReportScreen,
  ImageScreen,
  ViewParticipants,
  AddParticipants,
  DmAllMembers,
  SearchInChatroom,
  CommunityHybridChatScreen,
  ScreenName,
  FileUploadScreenWrapper,
  ChatroomScreenWrapper,
} from "@likeminds.community/chat-rn-core";

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator
          initialRouteName={ScreenName.CommunityHybridChatScreen}
        >
          <Stack.Screen
            name={ScreenName.CommunityHybridChatScreen}
            component={CommunityHybridChatScreen}
          />
          <Stack.Screen
            name={ScreenName.SearchInChatroom}
            component={SearchInChatroom}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={ScreenName.ExploreFeed}
            component={ExploreFeed}
            initialParams={{
              backIconPath: "",
              filterIconPath: "",
              participantsIconPath: "",
              totalMessagesIconPath: "",
              joinButtonPath: "",
              joinedButtonPath: "",
            }}
          />
          <Stack.Screen
            name={ScreenName.Chatroom}
            component={ChatroomScreenWrapper}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
          />
          <Stack.Screen
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
            name={ScreenName.FileUpload}
            component={FileUploadScreenWrapper}
            initialParams={{
              backIconPath: "", // add your back icon path here
              imageCropIcon: "", // add your image crop icon path here
            }}
          />
          <Stack.Screen name={ScreenName.VideoPlayer} component={VideoPlayer} />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={ScreenName.CarouselScreen}
            component={CarouselScreen}
            initialParams={{
              backIconPath: "", // add your back icon path here
            }}
          />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={ScreenName.PollResult}
            component={PollResult}
          />
          <Stack.Screen
            name={ScreenName.CreatePollScreen}
            component={CreatePollScreen}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name={ScreenName.ImageCropScreen}
            component={ImageCropScreen}
          />
          <Stack.Screen name={ScreenName.Report} component={ReportScreen} />
          <Stack.Screen name={ScreenName.ImageScreen} component={ImageScreen} />
          <Stack.Screen
            name={ScreenName.ViewParticipants}
            component={ViewParticipants}
          />
          <Stack.Screen
            name={ScreenName.AddParticipants}
            component={AddParticipants}
          />
          <Stack.Screen
            name={ScreenName.DmAllMembers}
            component={DmAllMembers}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

:::info

1. By default, only Members to Community Managers and visa versa direct messages are allowed, to enable direct messages for all Members, Enable **Members can DM other members** from LikeMinds Dashboard's [Chat Setting Section](https://dashboard.likeminds.community/chat/settings).

:::

</TabItem>
<TabItem value="AIChatbotTheme" label="AI Chatbot Theme">

Set up the navigation for your application using React Navigation. Create a `StackNavigator` in your `App.js` or equivalent file:

```tsx title="App.tsx"
import React from "react";
import { Platform } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  LMChatAIBotInitiaitionScreen,
  ImageCropScreen,
  SearchInChatroom,
  FileUploadScreenWrapper,
  ChatroomScreenWrapper,
} from "@likeminds.community/chat-rn-core";

const Stack = createStackNavigator();

enum ScreenName {
  Chatroom = "Chatroom",
  FileUpload = "FileUpload",
  ImageCropScreen = "ImageCropScreen",
  SearchInChatroom = "SearchInChatroom",
  ChatBotInitiateScreen = "ChatBotInitiateScreen",
}

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator>
          <Stack.Screen
            name={ScreenName.ChatBotInitiateScreen}
            component={LMChatAIBotInitiaitionScreen}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={ScreenName.SearchInChatroom}
            component={SearchInChatroom}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={ScreenName.Chatroom}
            component={ChatroomWrapperScreen}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
          />
          <Stack.Screen
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
            name={ScreenName.FileUpload}
            component={FileUploadScreenWrapper}
            initialParams={{
              backIconPath: "", // add your back icon path here
              imageCropIcon: "", // add your image crop icon path here
            }}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name={ScreenName.ImageCropScreen}
            component={ImageCropScreen}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

</TabItem>
</Tabs>

### Step 5 - Add Chatbot Button to your Screen (Optional)

:::note
This step is only required for accessing the AI chatbot via a FAB icon.
:::

#### 1. Set Up Your Screen

- Create a new screen or use an existing one in your application i.e Home Screen.
- Add the `<LMChatAIButton />` component imported from the `@likeminds.community/chat-rn-core` package in that screen.

```tsx title="HomeScreen.tsx"
import {
  LMChatAIButton
} from "@likeminds.community/chat-rn-core";

const HomeScreen = () => {
  return (
    {/* JSX of your app screen i.e Home Screen */}
    .
    .
    .
    {/* Add the LMChatAIButton component */}
    <LMChatAIButton
      apiKey={"<API_KEY>"}
      userName={"<USER_NAME>"}
      uuid={"<USER_ID>"}
    />
  )
}
```

#### 2. Wrap Your Screen

- Wrap the above screen with `<LMChatBotOverlayProvider/>` and pass the `myClient` instance initialized in step 3

```tsx title="app.tsx"
import {
  LMChatBotOverlayProvider
} from "@likeminds.community/chat-rn-core";

<LMChatBotOverlayProvider myClient={myClient}>
  <Stack.Navigator>
    <Stack.Screen
      name={"<HOME_SCREEN_NAME>"}
      component={"<HOME_SCREEN_COMPONENT>"}
    />
    {/* Add this along side other screens set up in step 4 */}
  <Stack.Navigator/>
</LMChatBotOverlayProvider>
```
