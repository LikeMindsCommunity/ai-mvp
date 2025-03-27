---
sidebar_position: 9
title: Add Files View
slug: /react-native/core/components/add-files-view
---

## Overview

The `AddFilesView` component provides a button for accessing additional file attachment options in a chat interface. It integrates with the input box context and supports customizable behavior for file selection.

<img
src={require('../../../../../static/img/reactNative/add-files.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '20%'}}
/>

## UI Components

The `AddFilesView` includes the following elements:

- **Attachment Button:** A touchable button that triggers a modal for file selection or executes a custom action when pressed.
- **Icon Display:** Dynamically displays an icon based on whether the user is interacting with a chatbot or standard chat.

## Props

| Property              | Type       | Description                                                                                                            | Optional           |
| --------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `handleFilesViewProp` | `Function` | Custom callback function triggered when the attachment button is pressed. Defaults to opening a modal if not provided. | :heavy_check_mark: |

## Features

1. **Dynamic Visibility:**

   - The component is only visible when specific conditions are met (e.g., not in upload mode, not recording voice notes, etc.).

2. **Chatbot-Specific Customization:**
   - Displays a chatbot-specific attachment button when interacting with chatbots.

## Usage Example

### To Customise Callbacks

Define a custom method like `handleFilesView` and pass it to the `handleFilesViewProp` of the `<AddFilesView/>` component.

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

const CustomMessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  // Define a custom action for the file attachment button
  const handleFilesView = () => {
    console.log("Opening file selection modal...");
  };

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
            {/* Add CustomAddFilesView component like this */}
            <AddFilesView handleFilesViewProp={handleFilesView} />
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

### Customise `<AddFilesView />` UI Component

- Create a new component `CustomAddFilesView`, referencing the [`AddFilesView`](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/AddFilesView/index.tsx) component.
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
  RecordSendInputFabView,
} from "@likeminds.community/chat-rn-core";
import CustomAddFilesView from "<path_to_custom_add_files_view_component>";

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
            {/* Add CustomAddFilesView component like this */}
            <CustomAddFilesView />
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
