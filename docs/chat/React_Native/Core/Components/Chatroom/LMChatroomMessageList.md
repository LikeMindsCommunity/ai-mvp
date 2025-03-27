---
sidebar_position: 4
title: Message List
slug: /react-native/core/components/chatroom/message-list
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `MessageList` component is responsible for rendering a list of messages in a chat interface. It manages the display of individual messages, handling any necessary UI elements like timestamps and sender information. The component also includes functionality for displaying loading indicators and empty states when no messages are available.

<img
src={require('../../../../../static/img/reactNative/lmMessageList.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMChatroomMessage](../Message/LMChatroomMessage.md)

## Customisations

The `MessageList` customisations can be done using [`chatBubbleStyles`](../Message/LMChatroomMessage.md#customisations)

## Props

| Property            | Type       | Description                                         | Default | Required |
| ------------------- | ---------- | --------------------------------------------------- | ------- | -------- |
| `onTapToUndo`       | `Function` | Triggered when the user taps to undo an action.     |         |          |
| `scrollToBottom`    | `Function` | Triggered to scroll the message list to the bottom. |         |          |
| `showChatroomTopic` | `boolean`  | Determines if the chatroom topic should be shown.   |         |          |

## Usage Example

:::info
The `MessageList` component can be used by wrapping it inside the `ChatRoom` component, and the callbacks are passed as props to `MessageList`.
:::

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `ChatroomScreenWrapper` file which will wrap the `MessageListScreen` within the `Chat` so that the callbacks becomes accessible inside of the `ChatroomScreen`.
- Create `messageListStyles` for customisation and call the `setMessageListStyles` to set the customisation.

<Tabs>
<TabItem value="ChatroomScreen" label="ChatroomScreen">

```tsx
import {
  STYLES,
  MessageList,
  useChatroomContext,
  ChatRoom,
} from "@likeminds.community/chat-rn-core";

const ChatroomScreen = () => {
  const { onTapToUndo, scrollToBottom } = useChatroomContext();

  const customOnTapToUndo = async () => {
    console.log("before custom on tap to undo");
    const response = await onTapToUndo();
    console.log("response after custom on tap to undo", response);
  };

  const customScrollToBottom = async () => {
    console.log("before custom scroll to bottom");
    await scrollToBottom();
    console.log("after custom scroll to bottom");
  };

  return (
    <ChatRoom>
      <MessageList
        onTapToUndo={customOnTapToUndo}
        scrollToBottom={customScrollToBottom}
        showChatroomTopic={false}
      />
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
import { CHATROOM, LMOverlayProvider } from "@likeminds.community/chat-rn-core";
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
