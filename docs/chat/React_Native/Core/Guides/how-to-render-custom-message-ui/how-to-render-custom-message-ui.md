---
sidebar_position: 1
title: How to Render Custom Message UI?
slug: /react-native/core/guide/how-to-render-custom-message-ui
---

## Overview

The LikeMinds Chat SDK allows developers to customize the appearance and layout of messages in a chat room to suit specific design requirements or branding. By implementing a custom UI for messages, you can modify elements such as message content, sender information, and timestamps to create a unique chat experience.

In this guide, we will walk through how to create a chat screen with a custom Message UI.

## Prerequisites

Before you begin, ensure the following:

- **LikeMinds Chat React Native SDK**: The SDK must be properly installed and initialized in your React Native project. Refer to the [installation guide](https://docs.likeminds.community/chat/react-native/getting-started) if needed.
- **Basic Understanding of React Native Components**: Familiarity with React Native components concepts.

## Steps

### Step 1: Define a Custom Message View Component

Implement a custom view for messages using the `customWidgetMessageView` prop in the `MessageList` component. This component defines how individual messages will appear in the chat.

Example:

```jsx
import React from "react";
import { Conversation } from "@likeminds.community/chat-rn/dist/shared/responseModels/Conversation";

const CustomMessageView = (message: Conversation) => {
  return <></>;
};
```

### Step 2: Create a `<CustomChatroomScreen/>` Component

In this step, you will design and implement the `<CustomChatroomScreen/>` component, which will serve as the main interface for users to interact within a chatroom. This component will provide the foundation for features such as displaying messages, sending new messages, and handling user interactions within the chatroom.

```jsx
import React from "react";
import {
  ChatRoom,
  ChatroomHeader,
  MessageList,
  MessageInput,
  MessageInputBox,
  ChatroomTopic,
  useChatroomContext,
} from "@likeminds.community/chat-rn-core";
import CustomMessageView from "./CustomMessageView";
import { InputBoxContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext";

export function CustomChatroomScreen() {
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
    setIsEditable,
    handleFileUpload,
  }: ChatroomContextValues = useChatroomContext();
  return (
    <ChatRoom>
      {/* Chatroom Header */}
      <ChatroomHeader
        showThreeDotsOnHeader={true}
        showThreeDotsOnSelectedHeader={true}
      />

      {/* Chatroom Topic */}
      <ChatroomTopic />

      {/* Message List with Custom Message View */}
      <MessageList customWidgetMessageView={CustomMessageView} />

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
        chatRequestState={chatRequestState}
      >
        <MessageInput>
          <MessageInputBox />
        </MessageInput>
      </InputBoxContextProvider>
    </ChatRoom>
  );
}
```

### Step 3: Wrap your `<CustomChatroomScreen/>` Component with the wrappers imported from the LM Chat SDK

```jsx
import { Chat } from "@likeminds.community/chat-rn-core";
import React from "react";
import { CustomChatroomScreen } from "<path_to_custom_chatroom_screen>";

function CustomChatroomScreenWrapper() {
  return (
    <Chat>
      <CustomChatroomScreen />
    </Chat>
  );
}

export default CustomChatroomScreenWrapper;
```

### Step 4: Add the Wrapped Components to the Stack Navigator

```jsx
<LMOverlayProvider
  myClient={myClient}
  apiKey={apiKey}
  userName={userName}
  userUniqueId={userUniqueID}
  lmChatInterface={lmChatInterface}
>
  <NavigationContainer>
    <Stack.Navigator>
      {/*
        ...other screens
        */}
      <Stack.Screen name="Chatroom" component={CustomChatroomScreenWrapper} />
    </Stack.Navigator>
  </NavigationContainer>
</LMOverlayProvider>
```
