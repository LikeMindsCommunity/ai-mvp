---
sidebar_position: 7
title: Add More Files View
slug: /react-native/core/components/add-more-files-view
---

## Overview

The `AddMoreFilesView` component provides a user interface for uploading additional files, such as images or documents, during a chat. It integrates with the `InputBoxContext` to manage states such as file types, upload screens, and restrictions based on chatroom types (e.g., chatbot interactions).

<img
src={require('../../../../../static/img/reactNative/add-more-files.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '20%'}}
/>

## UI Components

The `AddMoreFilesView` includes the following elements:

- **Add Image Button:** A button that allows users to select images from their gallery.
- **Add Document Button:** A button for selecting documents for upload.

## Theming Customizations

The `AddMoreFilesView` component supports additional theming through `STYLES.setAddMoreFilesViewStyles`. Below are the properties that have been added:

## Properties

| **Property Name**   | **Type**          | **Description**                                                                 |
|----------------------|-------------------|---------------------------------------------------------------------------------|
| `containerStyle`     | `ViewStyle`       | Custom styling for the file addition button container.                          |
| `iconStyle`          | `LMChatIconProps` | Customize the icon for adding files, including asset path, height, width, and style. |

## Props

| Property             | Type       | Description                                                                                                                      | Optional           |
| -------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `handleGalleryProp`  | `Function` | Custom callback triggered when the "Add Image" button is pressed. If not provided, the default `selectGallery` function is used. | :heavy_check_mark: |
| `handleDocumentProp` | `Function` | Custom callback triggered when the "Add Document" button is pressed. If not provided, the default `selectDoc` function is used.  | :heavy_check_mark: |

## Features

1. **Dynamic Button Display:**
   - Shows appropriate buttons based on the context (e.g., whether it's an upload screen or a chatbot interaction).

2. **Customizable Actions:**
   - Supports custom callbacks for both gallery and document selection, allowing for tailored upload workflows.

3. **Contextual State Management:**
   - Integrates with `InputBoxContext` to check file types (`isDoc`, `isGif`), screen state (`isUploadScreen`), and chatroom type (`chatroomType`).

## Usage Example

### Applying Callbacks & Styling to `MessageInputBox`

Define custom callbacks and apply custom styles using `STYLES.setAddMoreFilesViewStyles` directly within `MessageInputBox`.

```tsx
import React from "react";
import { View } from "react-native";
import {
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

  // Custom callbacks
  const handleGallerySelection = () => {
    console.log("Gallery button clicked");
  };

  const handleDocumentSelection = () => {
    console.log("Document button clicked");
  };

// Define custom styles using setStyles
const addMoreFilesViewStyles = {
  containerStyle: {
    backgroundColor: "white",
    padding: 10,
    borderRadius: 10,
  },
  iconStyle: {
    assetPath: require("Path to Your Image"),
    height: 24,
    width: 24,
  },
};

// Apply styles globally
STYLES.setAddMoreFilesViewStyles("addMoreFilesViewStyles", addMoreFilesViewStyles);
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
            {/* AddMoreFilesView with dynamic styles from STYLES and custom callbacks */}
            <AddMoreFilesView
              handleGalleryProp={handleGallerySelection}
              handleDocumentProp={handleDocumentSelection}
            />
            <InputBoxView />
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

