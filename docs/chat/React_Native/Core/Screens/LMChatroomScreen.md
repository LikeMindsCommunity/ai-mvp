---
sidebar_position: 3
title: Chatroom Screen
slug: /react-native/core/screens/chatroom-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `ChatRoom` screen serves as the main interface for users to engage in conversations within a specific chatroom in the LikeMinds chat application. It allows users to send and receive messages, view chatroom details, and interact with various features such as polls, media, and reactions, providing a seamless chat experience.

<img
src={require('../../../../static/img/reactNative/lmMessageList.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The Chatroom screen serves as a parent component, allowing you to incorporate as many child components as necessary, including your own custom components. Here are a few components that can be utilized to enhance the Chatroom.

- [ChatroomHeader](../Components/Chatroom/LMChatroomHeader.md)
- [ChatroomTopic](../Components/Chatroom/LMChatroomTopic.md)
- [MessageList](../Components/Chatroom/LMChatroomMessageList.md)
- [MessageInput](../Components/Chatroom/LMChatroomInputBox.md)
- [MessageInputBox](../Components/MessageInput/MessageInputBox.md)

## Callbacks

- `setChatroomTopic`: Triggered to set or update the chatroom's topic.
- `leaveChatroom`: Triggered when the user opts to leave the chatroom.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/context/ChatroomContext.tsx)

## Props

| Property                                 | Type        | Description                                                    | Optional           |
| ---------------------------------------- | ----------- | -------------------------------------------------------------- | ------------------ |
| `children`                               | `ReactNode` | The child components or content to render within the chatroom. |                    |
| `customReplyBox`                         | `Function`  | Custom function to render the reply box.                       | :heavy_check_mark: |
| `customMessageHeader`                    | `ReactNode` | Custom component for the message header.                       | :heavy_check_mark: |
| `customMessageFooter`                    | `ReactNode` | Custom component for the message footer.                       | :heavy_check_mark: |
| `customVideoImageAttachmentConversation` | `ReactNode` | Custom component for video and image attachments.              | :heavy_check_mark: |

For information about more props, click [here](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/e0b1e9604a34cc14963e3c78f6801cd8275ddad8/likeminds-chat-reactnative-integration/ChatSX/screens/ChatRoom/index.tsx#L20)

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `ChatroomScreenWrapper` file which will wrap the `ChatroomScreen` within the `UniversalFeedContextProvider` and `PostListContextProvider` so that the callbacks becomes accessible inside of the `ChatroomScreen`.
- Now, you can create styles based on the component being utilizied, for example, for chatbubble create `messageListStyles` for customisation and call the `setMessageListStyles` to set it, or `inputBoxStyle` for input box customisation and call `setInputBoxStyle` to set the customisation.

<Tabs>
<TabItem value="ChatroomScreen" label="ChatroomScreen">

```tsx
import {
  ChatRoom,
  ChatroomHeader,
  MessageList,
  MessageInput,
  useChatroomContext,
  useMessageListContext,

  ChatroomTopic,
  STYLES
} from "@likeminds.community/chat-rn-core";
import {InputBoxContextProvider} from '@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext';
import {ChatroomContextValues} from '@likeminds.community/chat-rn-core/ChatSX/context/ChatroomContext';
import MessageInputBox from "@likeminds.community/chat-rn-core/ChatSX/components/InputBox";

export function ChatroomScreen() {
  const showViewParticipants = true;
  const showShareChatroom = true;
  const showChatroomIcon = true;
  const customChatroomUserTitle = "Moderator";

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
    onTapToUndo,
  }: ChatroomContextValues = useChatroomContext();
  const { scrollToBottom } = useMessageListContext();

  const customJoinSecretChatroom = async () => {
    console.log("before custom join secret chatroom");
    const response = await joinSecretChatroom();
    console.log("response after custom join secret chatroom", response);
  };
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

  const inputBoxStyles = {
    placeholderTextColor: "#aaa",
    selectionColor: "#3CA874",
  };

  // custom styling for input box
  if (inputBoxStyles) {
    STYLES.setInputBoxStyle(inputBoxStyles);
  }

  const chatBubbleStyles = {
    borderRadius: 10,
    sentMessageBackgroundColor: 'blue',
  };

  // custom styling for message list
  if (chatBubbleStyles) {
    STYLES.setChatBubbleStyle(chatBubbleStyles);
  }

  return (
    <ChatRoom
      showViewParticipants={showViewParticipants}
      showShareChatroom={showShareChatroom}
    >
      {/* ChatroomHeader */}
      <ChatroomHeader
        showChatroomIcon={showChatroomIcon}
        customChatroomUserTitle={customChatroomUserTitle}
        hideSearchIcon={true}
      />
      {/* ChatroomTopic */}
      <ChatroomTopic />
      
      {/* MessageList */}
      <MessageList
        onTapToUndo={customOnTapToUndo}
        scrollToBottom={customScrollToBottom}
      />
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
        <MessageInput joinSecretChatroomProp={customJoinSecretChatroom}>
          <MessageInputBox />
        </MessageInput>
      </InputBoxContextProvider>
    </ChatRoom>
  );
}
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
import { ScreenName, LMOverlayProvider, Themes } from "@likeminds.community/feed-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ChatroomScreenWrapper } from "<<path_to_ChatroomScreenWrapper.tsx>>";

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
        <Stack.Navigator screenOptions={{ headerShown: true }}>
          <Stack.Screen name={ScreenName.Chatroom} component={ChatroomScreenWrapper} />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
