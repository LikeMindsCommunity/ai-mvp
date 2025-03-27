---
sidebar_position: 8
title: Chatroom Topic
slug: /react-native/core/components/chatroom-topic
---

## Overview

The `ChatroomTopic` component is used within the LikeMinds chat React Native integration to display and manage topics within a chatroom. It allows users to view and interact with specific chatroom topics, providing an organized structure for discussions. This component manages the rendering of topic details, such as title and description, and facilitates user interaction with the topic.

<img
src={require('../../../../../static/img/reactNative/lmChatroomTopic.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisations with Props

| Property           | Type                                  | Description                                |
| ------------------ | ------------------------------------- | ------------------------------------------ |
| `topicHeader`      | [TopicHeader](#topicheader)           | Style for the topic header                 |
| `topicDescription` | [TopicDescription](#topicdescription) | Style for the topic description            |
| `topicPlaceholder` | string                                | Placeholder text for the topic input field |

## Customisations with Styles

### TopicHeader

| Property     | Type   | Description                      |
| ------------ | ------ | -------------------------------- |
| `fontSize`   | number | Font size of the topic header    |
| `fontFamily` | string | Font family for the topic header |
| `color`      | string | Color of the topic header        |

### TopicDescription

| Property     | Type   | Description                           |
| ------------ | ------ | ------------------------------------- |
| `fontSize`   | number | Font size of the topic description    |
| `fontFamily` | string | Font family for the topic description |
| `color`      | string | Color of the topic description        |

## Usage Example

:::info
The `ChatroomTopic` component can be used by wrapping it inside the `ChatRoom` component.
:::

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `ChatroomScreenWrapper` file which will wrap the `ChatroomScreen` within the `Chat` so that the callbacks becomes accessible inside of the `ChatroomScreen`.
- Create `chatroomTopicStyles` for customisation and call the `chatroomTopicStyles` to set the customisation.

<Tabs>
<TabItem value="ChatroomScreen" label="ChatroomScreen">

```tsx
import {
  STYLES,
  useChatroomContext,
  ChatRoom,
} from "@likeminds.community/chat-rn-core";

const ChatroomScreen = () => {
  const chatroomTopicStyles = {
    topicHeader: {
      color: "pink",
    },
  };

  // custom styling for chatroom topics
  if (chatroomTopicStyles) {
    STYLES.setChatroomTopicStyle(chatroomTopicStyles);
  }

  return (
    <ChatRoom>
      <ChatroomTopic />
      {/* Other chat components*/}
    </ChatRoom>
  );
};

export default ChatroomScreen;
```

</TabItem>
<TabItem value="ChatroomScreenWrapper" label="ChatroomScreenWrapper">

```tsx
import { Chat } from "@likeminds.community/chat-rn-core";
import { ChatroomScreen } from "<<path_to_ChatroomScreen.tsx>>";

function ChatroomScreenWrapper() {
  return (
    <Chat>
      <ChatroomScreen />
    </Chat>
  );
}

export default ChatroomScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `ChatroomScreenWrapper` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import { CHATROOM, LMOverlayProvider } from "@likeminds.community/feed-rn-core";
import { ChatroomScreenWrapper } from "<<path_to_ChatroomScreenWrapper.tsx>>";
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
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={CHATROOM}
            component={ChatroomScreenWrapper}
            initialParams={{
              chatroomID: chatroomId,
              announcementRoomId: announcementRoomId,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
