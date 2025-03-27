---
sidebar_position: 1
title: Message Input
slug: /react-native/core/components/message-input-box
---

# Overview

The `MessageInputBox` component is a core UI element for enabling users to create and send messages in the chat interface. It integrates various features, including text input, file attachments, user tagging, voice notes, and modals for advanced functionality like direct message requests and file selection.

<img
src={require('../../../../../static/img/reactNative/lmSimpleInputBox.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

---

## Component Breakdown

- [VoiceNoteRecordToast](./VoiceNoteRecordToast.md) :
  This component displays a toast notification for ongoing voice note recordings. It is rendered at the top of the `MessageInputBox`.

- [InputWrapper](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/InputWrapper/index.tsx):
  The main container for the input box functionality. It contains:

  - [InputWrapperLeftSection](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/InputWrapperLeftSection/index.tsx):
    This section houses the primary input features:

    - [UserTaggingList](./UserTaggingList.md): Displays a list of users for tagging within the message.
    - [ReplyBoxView](./ReplyBoxView.md): Shows the message being replied to, if applicable.
    - [LinkPreviewInputView](./LinkPreviewInputView.md): Displays link previews when a URL is entered.
    - [EditBox](./EditBox.md): Enables editing of previously sent messages.
    - TextInputWrapper:
      This nested container includes:

      - [AddMoreFilesView](./AddMoreFilesView.md): UI for adding additional files to the message.
      - [InputBoxView](./InputBoxView.md): The main text input field for composing messages.
      - [AddFilesView](./AddFilesView.md): UI for attaching files (e.g., images, documents).

  - [RecordSendInputFabView](./RecordSendInputFabView.md): This component provides UI elements for sending messages and recording voice notes. It handles both text and audio message sending seamlessly.

- [SelectFilesModal](./SelectFilesModal.md): Enables users to select files such as images and documents for attachment.
- [SendDMRequestModal](./SendDMRequestModal.md): Displays a modal for sending direct message (DM) requests.

:::note
The order of components would be same.
:::

---

## Context Integration

The `MessageInputBox` utilizes the `useInputBoxContext` hook for managing the input box state and actions.

---

## Example Usage

### Step 1: Create MessageInputBox Component

```tsx
import {
  AddFilesView,
  AddMoreFilesView,
  EditBox,
  InputBoxView,
  InputWrapper,
  InputWrapperLeftSection,
  LinkPreviewInputView,
  ReplyBoxView,
  SelectFilesModal,
  SendDMRequestModal,
  TextInputWrapper,
  useInputBoxContext,
  UserTaggingList,
  VoiceNoteRecordToast,
  RecordSendInputFabView,
} from "@likeminds.community/chat-rn-core";

const MessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  return (
    <View>
      <VoiceNoteRecordToast />

      <InputWrapper>
        <InputWrapperLeftSection>
          <UserTaggingList />
          <ReplyBoxView />
          <LinkPreviewInputView />
          <EditBox />

          <TextInputWrapper>
            <AddMoreFilesView />
            <InputBoxView />
            <AddFilesView />
          </TextInputWrapper>
        </InputWrapperLeftSection>

        {/* Send message and send voice notes UI */}
        <RecordSendInputFabView />
      </InputWrapper>

      {/* More features modal like select Images, Docs etc. */}
      <SelectFilesModal />
      {/* SEND DM request Modal */}
      <SendDMRequestModal
        hideDMSentAlert={hideDMSentAlert}
        DMSentAlertModalVisible={DMSentAlertModalVisible}
        onSend={onSend}
        message={message}
      />
    </View>
  );
};

export default MessageInputBox;
```

### Step 2: Add MessageInputBox Component to ChatroomScreen

```tsx
import { View } from "react-native";
import { ChatroomContextValues } from "@likeminds.community/chat-rn-core/ChatSX/context/ChatroomContext";
import { InputBoxContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext";
import {
  MessageInputBox,
  MessageInput,
} from "@likeminds.community/chat-rn-core";

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

  return (
    <View style={{ flex: 1 }}>
      {/* Other chat components */}

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
    </View>
  );
};

export default ChatroomScreen;
```

- To customize the UI of the `<MessageInputBox />` component, modify the appearance of a specific element detailed in the [component breakdown](#component-breakdown).
