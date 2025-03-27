---
sidebar_position: 6
title: Edit Box
slug: /react-native/core/components/edit-box
---

## Overview

The `EditBox` component provides an interface for editing a message in a chat conversation. It allows users to view the message being edited and includes a close button to dismiss the edit box. The component integrates with the `InputBoxContext` for managing the editable state and message content, and uses Redux for dispatching actions related to the edited message.

<img
src={require('../../../../../static/img/reactNative/edit-box.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The `EditBox` includes the following elements:

- **Edit Box:** Displays the message being edited, utilizing the `ReplyBox` component.
- **Close Button:** A clickable button to dismiss the edit box, either by executing a custom close callback or using the default behavior defined in the context.

## Theming Customizations

The `EditBox` component now supports additional theming through `inputBoxStyles.editBoxStyles`. These styles are applied dynamically using `STYLES.setEditBoxStyles`. The following properties have been added:

| Property Name    | Type            | Description                                                                                |
| ---------------- | --------------- | ------------------------------------------------------------------------------------------ |
| containerStyle   | ViewStyle       | Custom styling for the edit box container.                                                 |
| closeButtonStyle | ViewStyle       | Custom styling for the close button container.                                             |
| closeIconStyle   | LMChatIconProps | Allows customization of the close icon, including assetPath, height, width, and iconStyle. |

## Props

| Property                 | Type       | Description                                                                                                                                                     | Optional           |
| ------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `handleEditBoxCloseProp` | `Function` | Custom callback function triggered when the close button is pressed. If not provided, the default behavior resets the edit state and clears the edited message. | :heavy_check_mark: |

## Features

1. **Dynamic Edit Box:**

   - Displays the message being edited, with additional context such as the chatroom name.

2. **Customizable Close Action:**

   - Supports a custom callback for closing the edit box. If not provided, it defaults to resetting the edit state and clearing the message.

3. **State Management Integration:**
   - Uses the `InputBoxContext` to manage the `isEditable` state, indicating whether the edit box is visible, and the `editConversation` state, which holds the message content being edited.
   - Utilizes Redux to dispatch actions (`SET_EDIT_MESSAGE` and `SELECTED_MESSAGES`) to update the edited message and clear any selected messages.

## Usage Example

### Customizing Callbacks and Styling

Define custom callbacks for gallery and document selection, and apply custom styles using `STYLES.setEditBoxStyles`directly within `MessageInputBox`. 

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

const MessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  // Customize the edit box close behavior
  const handleEditBoxClose = () => {
    console.log("Edit box closed");
  };

  // Define custom styles for EditBox component
  const editBoxStyles = {
    containerStyle: {
      backgroundColor: "white",  // Custom background color
      padding: 10,               // Custom padding
      borderRadius: 10,          
    },
    closeButtonStyle: {
      position: "absolute",      
      top: 10,                   
      right: 10,                 
      backgroundColor: "blue",   
      padding: 5,                
      borderRadius: 5,           
    },
    closeIconStyle: {
      assetPath: require("Path to Your Image"),  // Path to the close icon image
      height: 24,                                  // Icon height
      width: 24,                                   // Icon width
    },
  };

  // Apply styles dynamically
  STYLES.setEditBoxStyles(editBoxStyles);

  return (
    <View>
      <VoiceNoteRecordToast />

      <InputWrapper>
        <InputWrapperLeftSection>
          <UserTaggingList />
          <ReplyBoxView />
          <LinkPreviewInputView />
          {/* EditBox with dynamic styles from STYLES and custom callbacks */}
          <EditBox handleEditBoxCloseProp={handleEditBoxClose} />

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

export default MessageInputBox;
```

- Use the `MessageInputBox` component as a child of the `MessageInput` component in the relevant screens:
  - [Chatroom Screen](../../Screens/LMChatroomScreen.md)
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)

