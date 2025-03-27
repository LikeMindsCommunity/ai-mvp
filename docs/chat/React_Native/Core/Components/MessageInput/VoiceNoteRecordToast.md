---
sidebar_position: 2
title: VoiceNoteRecordToast
slug: /react-native/core/components/voice-note-record-toast
---

## Overview

The `VoiceNoteRecordToast` component is a UI element that displays a toast message, guiding users to "Tap and Hold" for recording voice notes. It is dynamically positioned based on the keyboard state and platform (iOS/Android) to provide an optimal user experience.

<img
src={require('../../../../../static/img/reactNative/record-toast.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Features

- **Conditional Rendering**: Displays the toast only when the user interacts with the voice note recording feature.

## Context Dependencies

This component uses the `useInputBoxContext` to access key state values:

- `isVoiceNoteIconPress`: Determines if the voice note recording is active.
- `isKeyBoardFocused`: Indicates if the keyboard is currently focused.
- `isIOS`: Boolean to check if the app is running on iOS.

## UI Components

- [`LMChatTextView`](../Fundamentals/text_view.md): Displays the "Tap and Hold" text with custom styles.

## Props

| Property               | Type      | Description                                         | Optional |
| ---------------------- | --------- | --------------------------------------------------- | -------- |
| `isVoiceNoteIconPress` | `boolean` | Active state for voice note icon press.             | No       |
| `isKeyBoardFocused`    | `boolean` | Indicates if the keyboard is focused.               | No       |
| `isIOS`                | `boolean` | Indicates if the app is running on an iOS platform. | No       |

## Usage Example

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
  UserTaggingList,
  VoiceNoteRecordToast,
  RecordSendInputFabView,
} from "@likeminds.community/chat-rn-core";

const CustomMessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  return (
    <View>
      {/* Add VoiceNoteRecordToast component like this*/}
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

        <RecordSendInputFabView />
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

### Customise `<VoiceNoteRecordToast />` UI Component

- Create a new component `CustomVoiceNoteRecordToast`, referencing the [`VoiceNoteRecordToast`](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/VoiceNoteRecordToast/index.tsx) component.
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
  UserTaggingList,
  RecordSendInputFabView,
} from "@likeminds.community/chat-rn-core";
import CustomVoiceNoteRecordToast from "<path_to_custom_edit_box_component>";

const CustomMessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  return (
    <View>
      {/* Add CustomVoiceNoteRecordToast component like this*/}
      <CustomVoiceNoteRecordToast />

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

        <RecordSendInputFabView />
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
