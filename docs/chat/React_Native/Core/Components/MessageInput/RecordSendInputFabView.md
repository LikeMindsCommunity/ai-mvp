---
sidebar_position: 10
title: Record Send Input Fab View
slug: /react-native/core/components/record-send-input-fab-view
---

## Overview

The `RecordSendInputFabView` component provides a dynamic floating action button (FAB) for chat input. It supports multiple functionalities, including sending messages, recording voice notes, and handling direct message (DM) requests. The component is designed to adapt to various chat states and integrates seamlessly with context and state management.

<img
src={require('../../../../../static/img/reactNative/record-send-fab-view.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '20%'}}
/>

## UI Components

The `RecordSendInputFabView` includes the following elements:

- **Send Button:** Displays a button to send messages or attachments.
- **Voice Recording Button:** A button for starting and managing voice recordings.
- **Lock and Chevron Icons:** Visual indicators for locking voice recordings.
- **Gesture Support:** Enables advanced gestures for enhanced user interaction.

## Props

| Property            | Type              | Description                                                                                                         | Optional           |
| ------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `onSendMessageProp` | OnSendMessageProp | Custom callback function for sending messages or voice notes. Defaults to using the `onSend` function from context. | :heavy_check_mark: |

## Features

1. **Dynamic Button States:**

   - Automatically switches between send and voice recording buttons based on the chat input state.

2. **Voice Recording Functionality:**

   - Supports voice note recording with visual feedback for lock and chevron indicators.
   - Allows sending recorded voice notes directly.

3. **DM Support:**

   - Handles direct message requests for private members in DM chatrooms.

4. **Gesture-Based Interaction:**

   - Includes advanced gestures for locking and managing voice recordings.

5. **Customizable Behavior:**
   - Supports a custom `onSendMessageProp` for overriding default message-sending behavior.

## Usage Example

### To Customise Callbacks

Define a custom method like `customSendHandler` and pass it to the `onSendMessageProp` of the `<RecordSendInputFabView/>` component.

```tsx
import React from "react";
import { View } from "react-native";
import {
  RecordSendInputFabView,
  OnSendMessageProp,
} from "@likeminds.community/chat-rn-core";

const MessageInputBox = () => {
  const customSendHandler = ({
    message,
    metaData,
    voiceNote,
    isSendWhileVoiceNoteRecorderPlayerRunning,
  }: OnSendMessageProp) => {
    console.log("Message sent:", message);
    console.log("Metadata:", metaData);
    console.log("Voice Note Details:", voiceNote);
    console.log(
      "Sent while voice note recorder/player running:",
      isSendWhileVoiceNoteRecorderPlayerRunning
    );
  };

  return (
    <View style={{ flex: 1 }}>
      {/* Other chat input components */}
      <RecordSendInputFabView onSendMessageProp={customSendHandler} />
    </View>
  );
};

export default MessageInputBox;
```

```tsx
import React from "react";
import { View } from "react-native";
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
  VoiceNoteRecordToast,
  UserTaggingList,
  RecordSendInputFabView,
} from "@likeminds.community/chat-rn-core";
import { OnSendMessageProp } from "@likeminds.community/chat-rn-core/ChatSX/components/RecordSendInputFabView";

const CustomMessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  const customSendHandler = ({
    message,
    metaData,
    voiceNote,
    isSendWhileVoiceNoteRecorderPlayerRunning,
  }: OnSendMessageProp) => {
    console.log("Message sent:", message);
    console.log("Metadata:", metaData);
    console.log("Voice Note Details:", voiceNote);
    console.log(
      "Sent while voice note recorder/player running:",
      isSendWhileVoiceNoteRecorderPlayerRunning
    );
  };

  return (
    <View>
      <VoiceNoteRecordToast />

      <InputWrapper>
        <InputWrapperLeftSection>
          <UserTaggingList />
          <ReplyBoxView handleReplyBoxCloseProp={handleReplyBoxClose} />
          <LinkPreviewInputView />
          <EditBox />

          <TextInputWrapper>
            <AddMoreFilesView />
            <InputBoxView />
            <AddFilesView />
          </TextInputWrapper>
        </InputWrapperLeftSection>

        {/* Add RecordSendInputFabView component like this*/}
        <RecordSendInputFabView onSendMessageProp={customSendHandler} />
      </InputWrapper>

      <SelectFilesModal />
      <SendDMRequestModal
        hideDMSentAlert={hideDMSentAlert}
        DMSentAlertModalVisible={DMSentAlertModalVisible}
        onSend={onSend}
        message={message}
      />
    </View>
  );
};

export default CustomMessageInputBox;
```

### Customise `<RecordSendInputFabView />` UI Component

- Create a new component `CustomRecordSendInputFabView`, referencing the [`RecordSendInputFabView`](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/RecordSendInputFabView/index.tsx) component.
- Perform your UI customizations in the new component.

```tsx
import React from "react";
import { View } from "react-native";
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
  VoiceNoteRecordToast,
  UserTaggingList,
} from "@likeminds.community/chat-rn-core";
import CustomRecordSendInputFabView from "<path_to_custom_record_send_input_fab_view_component>";

const CustomMessageInputBox = () => {
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
        {/* Add CustomRecordSendInputFabView component like this*/}
        <CustomRecordSendInputFabView />
      </InputWrapper>

      <SelectFilesModal />
      <SendDMRequestModal
        hideDMSentAlert={hideDMSentAlert}
        DMSentAlertModalVisible={DMSentAlertModalVisible}
        onSend={onSend}
        message={message}
      />
    </View>
  );
};

export default CustomMessageInputBox;
```

- Use the `CustomMessageInputBox` component as a child of the `MessageInput` component in the relevant screens:
  - [Chatroom Screen](../../Screens/LMChatroomScreen.md)
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)
