---
sidebar_position: 5
title: Message Input
slug: /react-native/core/screens/input-box
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `MessageInput` component is a Higher-Order Component (HOC) designed to enhance the functionality of a message input box within our chat app. It wraps and customizes the `MessageInputBox` component, which supports features like tagging and media, enhancing user interaction by enabling users to mention others or share multimedia content within the chat.

## UI Components

- [LMChatIcon](../Fundamentals/icon.md)
- [LMChatLoader](../Fundamentals/loader.md)
- [LMChatTextInput](../Fundamentals/text_input.md)
- [LMChatTextView](../Fundamentals/text_view.md)

## Callbacks

- `joinSecretChatroomProp`: Callback method to handle joining a secret chatroom.
- `showJoinAlertProp`: Callback method to display an alert for joining a chatroom.
- `showRejectAlertProp`: Callback method to display an alert for rejecting a chatroom invitation.

## Customisations

| Property                   | Type                                            | Description                                   |
| -------------------------- | ----------------------------------------------- | --------------------------------------------- |
| `placeHolderTextColor`     | `string`                                        | The color of the placeholder text             |
| `selectionColor`           | `string`                                        | The color used for text selection             |
| `partsTextStyle`           | [`Partstextstyle`](#partstextstyle)             | Custom style for the text parts               |
| `plainTextStyle`           | [`Plaintextstyle`](#plaintextstyle)             | Custom style for plain text                   |
| `placeHolderText`          | `string`                                        | The text to display as placeholder            |
| `inputTextStyle`           | [`Inputtextstyle`](#inputtextstyle)             | Custom style for the input text               |
| `sendIconStyles`           | [`Sendiconstyles`](#sendiconstyles)             | Custom style for the send icon                |
| `attachmentIconStyles`     | [`Attachmenticonstyles`](#attachmenticonstyles) | Custom style for the attachment icon          |
| `micIconStyles`            | [`Miciconstyles`](#miciconstyles)               | Custom style for the mic icon                 |
| `cameraIconStyles`         | [`Cameraiconstyles`](#cameraiconstyles)         | Custom style for the camera icon              |
| `galleryIconStyles`        | [`Galleryiconstyles`](#galleryiconstyles)       | Custom style for the gallery icon             |
| `documentIconStyles`       | [`Documenticonstyles`](#documenticonstyles)     | Custom style for the document icon            |
| `pollIconStyles`           | [`Polliconstyles`](#polliconstyles)             | Custom style for the poll icon                |
| `messageInputMarginBottom` | `number`                                        | The margin at the bottom of the message input |

### PartsTextstyle

| Property | Type     | Description           |
| -------- | -------- | --------------------- |
| `color`  | `string` | The color of the text |

### PlainTextstyle

| Property | Type     | Description           |
| -------- | -------- | --------------------- |
| `color`  | `string` | The color of the text |

### InputTextstyle

| Property       | Type     | Description                                |
| -------------- | -------- | ------------------------------------------ |
| `flexgrow`     | `number` | Defines the grow factor for the input text |
| `fontsize`     | `string` | The size of the input text font            |
| `fontfamily`   | `string` | The font family for the input text         |
| `maxheight`    | `number` | The maximum height of the input text       |
| `padding`      | `number` | Padding inside the input text              |
| `marginbottom` | `number` | The margin at the bottom of the input text |
| `overflow`     | `string` | How to handle overflow for the input text  |

### SendIconstyles

| Property     | Type     | Description                         |
| ------------ | -------- | ----------------------------------- |
| `width`      | `number` | The width of the send icon          |
| `height`     | `number` | The height of the send icon         |
| `resizemode` | `string` | Defines how to resize the send icon |
| `marginleft` | `number` | The left margin of the send icon    |
| `tintcolor`  | `string` | The color tint for the send icon    |

### AttachmentIconstyles

| Property     | Type     | Description                               |
| ------------ | -------- | ----------------------------------------- |
| `width`      | `number` | The width of the attachment icon          |
| `height`     | `number` | The height of the attachment icon         |
| `resizemode` | `string` | Defines how to resize the attachment icon |

### MicIconstyles

| Property     | Type     | Description                        |
| ------------ | -------- | ---------------------------------- |
| `width`      | `number` | The width of the mic icon          |
| `height`     | `number` | The height of the mic icon         |
| `resizemode` | `string` | Defines how to resize the mic icon |
| `tintcolor`  | `string` | The color tint for the mic icon    |

### CameraIconstyles

| Property     | Type     | Description                           |
| ------------ | -------- | ------------------------------------- |
| `width`      | `number` | The width of the camera icon          |
| `height`     | `number` | The height of the camera icon         |
| `resizemode` | `string` | Defines how to resize the camera icon |

### GalleryIconstyles

| Property     | Type     | Description                            |
| ------------ | -------- | -------------------------------------- |
| `width`      | `number` | The width of the gallery icon          |
| `height`     | `number` | The height of the gallery icon         |
| `resizemode` | `string` | Defines how to resize the gallery icon |

### DocumentIconstyles

| Property     | Type     | Description                             |
| ------------ | -------- | --------------------------------------- |
| `width`      | `number` | The width of the document icon          |
| `height`     | `number` | The height of the document icon         |
| `resizemode` | `string` | Defines how to resize the document icon |

### PollIconstyles

| Property     | Type     | Description                         |
| ------------ | -------- | ----------------------------------- |
| `width`      | `number` | The width of the poll icon          |
| `height`     | `number` | The height of the poll icon         |
| `resizemode` | `string` | Defines how to resize the poll icon |

## Props

| Property                 | Type                            | Description                                                       | Required           |
| ------------------------ | ------------------------------- | ----------------------------------------------------------------- | ------------------ |
| `joinSecretChatroomProp` | `Function`                      | Function to handle joining a secret chatroom.                     | :heavy_check_mark: |
| `showJoinAlertProp`      | `Function`                      | Function to display an alert for joining a chatroom.              | :heavy_check_mark: |
| `showRejectAlertProp`    | `Function`                      | Function to display an alert for rejecting a chatroom invitation. | :heavy_check_mark: |
| `hintMessages`           | [`HintMessages`](#hintmessages) | Object containing various hint messages.                          |                    |

### HintMessages

| Property                     | Type     | Description                                     |
| ---------------------------- | -------- | ----------------------------------------------- |
| `messageForRightsDisabled`   | `string` | Message shown when rights are disabled.         |
| `messageForMemberCanMessage` | `string` | Message shown to members who can send messages. |
| `messageForAnnouncementRoom` | `string` | Message shown for announcement rooms.           |
| `respondingDisabled`         | `string` | Message shown when responding is disabled.      |

## Usage Example

:::info
The `MessageInput` screen can be used by wrapping it inside the `ChatRoom` screen, and the callbacks are passed as props to `MessageInput`.
:::

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `ChatroomScreenWrapper` file which will wrap the `ChatroomScreen` within the `Chat` so that the callbacks becomes accessible inside of the `ChatroomScreen`.
- Create `inputBoxStyles` for customisation and call the `setInputBoxStyle` to set the customisation.

<Tabs>
<TabItem value="ChatroomScreen" label="ChatroomScreen">

```tsx
import {
  STYLES,
  MessageInput,
  useChatroomContext,
  ChatRoom,
} from '@likeminds.community/chat-rn-core';
import MessageInputBox from '@likeminds.community/chat-rn-core/ChatSX/components/InputBox';
import {ChatroomContextValues} from '@likeminds.community/chat-rn-core/ChatSX/context/ChatroomContext';
import {InputBoxContextProvider} from '@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext';

const ChatroomScreen = () => {
  const {
    chatroomID,
    chatroomWithUser,
    currentChatroomTopic,
    chatroomType,
    replyChatID,
    isEditable,
    chatroomName,
    isSecret,
    refInput,
    chatroomDBDetails,
    chatRequestState,
    setIsEditable,
    handleFileUpload,
    joinSecretChatroom,
    showJoinAlert,
    showRejectAlert,
  }: ChatroomContextValues = useChatroomContext();

  const customJoinSecretChatroom = async () => {
    console.log('before custom join secret chatroom');
    const response = await joinSecretChatroom();
    console.log('response after custom join secret chatroom', response);
  };

  const customShowJoinAlert = async () => {
    console.log('before custom show join alert');
    await showJoinAlert();
    console.log('after custom show join alert');
  };
  const customShowRejectAlert = async () => {
    console.log('before custom show reject alert');
    await showRejectAlert();
    console.log('after custom show reject alert');
  };

  const inputBoxStyles = {
    placeholderTextColor: '#aaa',
    selectionColor: '#3CA874',
    partsTextStyle: {
      color: '#3CA874',
    },
    sendIconStyles: {
      tintColor: 'black',
    },
    micIconStyles: {
      tintColor: 'black',
    },
  };

  // custom styling for input box
  if (inputBoxStyles) {
    STYLES.setInputBoxStyle(inputBoxStyles);
  }

  return (
    <ChatRoom>
      {/* Input Box Flow */}
      <InputBoxContextProvider
        chatroomName={chatroomName}
        chatroomWithUser={chatroomWithUser}
        replyChatID={replyChatID}
        chatroomID={chatroomID}
        isUploadScreen={false}
        myRef={refInput}
        handleFileUpload={handleFileUpload}
        isEditable={isEditable}
        setIsEditable={(value: boolean) => {
          setIsEditable(value);
        }}
        isSecret={isSecret}
        chatroomType={chatroomType}
        currentChatroomTopic={currentChatroomTopic}
        isPrivateMember={chatroomDBDetails.isPrivateMember}
        chatRequestState={chatRequestState}>
        <MessageInput
          joinSecretChatroomProp={customJoinSecretChatroom}
          showJoinAlertProp={customShowJoinAlert}
          showRejectAlertProp={customShowRejectAlert}>
          <MessageInputBox />
        </MessageInput>
      </InputBoxContextProvider>
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
import { ScreenName, LMOverlayProvider } from "@likeminds.community/feed-rn-core";
import { CreatePostScreenWrapper } from "<<path_to_CreatePostScreenWrapper.tsx>>";
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
            name={ScreenName.Chatroom}
            component={ChatroomScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
