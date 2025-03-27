---
sidebar_position: 8
title: Input Box View
slug: /react-native/core/components/input-box-view
---

## Overview

The `InputBoxView` component provides an input area for messages in a chat application. It includes features for text input, voice recording, and GIF selection, making it a versatile and interactive chat input component. The component integrates with `InputBoxContext` for managing state and utilizes Redux for dispatching actions related to message input.

<img
src={require('../../../../../static/img/reactNative/input-box-view.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The `InputBoxView` includes the following elements:

- **Text Input:** Supports multiline input, mentions, and dynamic placeholders.
- **Voice Notes:** Enables recording, playback, and clearing of voice notes.
- **GIF Picker:** Optional GIF selection button integrated with GiphyDialog.
- **Dynamic States:** Manages animations and states like deleting recordings, voice playback, and recording lock.

## Theming Customizations

The `InputBoxView` component supports theming through `inputBoxStyles.inputBoxViewStyles`. These styles are dynamically applied using `STYLES.setInputBoxViewStyles`. The following properties are available:

| Property Name         | Type              | Description |
|-----------------------|-------------------|-------------|
| voiceNotesInputParent | ViewStyle         | Custom styling for the parent container of voice notes input. |
| recordTitle           | TextStyle         | Custom styling for the title of the voice recording. |
| emoji                 | LMChatIconProps   | Customization of emoji icons, including assetPath, iconStyle, height, and width. |
| input                 | Object            | Customization of input box styles such as border, padding, and background color. |
| chevron               | LMChatIconProps   | Customization of the chevron icon, including assetPath, iconStyle, height, and width. |

### Customization of Icons

You can customize asset paths and styles of the icons used in the `InputBoxView` component:

| Icon Name             | Property Name      | Description |
|-----------------------|--------------------|-------------|
| Record Icon           | `emoji`            | Customize the record button icon. |
| Stop Recording Icon   | `emoji`            | Customize the stop recording button icon. |
| Cross Icon            | `emoji`            | Customize the close button icon. |
| Left Chevron Icon     | `chevron`          | Customize the left chevron icon. |
| Play Icon             | `emoji`            | Customize the play icon for voice notes. |
| Pause Icon            | `emoji`            | Customize the pause icon for voice notes. |

## Props

| Property               | Type       | Description                                                                                               | Optional           |
| ---------------------- | ---------- | --------------------------------------------------------------------------------------------------------- | ------------------ |
| `handleStopRecordProp` | `Function` | Custom callback triggered when stopping voice recording. Defaults to context's `handleStopRecord`.        | :heavy_check_mark: |
| `clearVoiceRecordProp` | `Function` | Custom callback triggered to clear the current voice recording. Defaults to context's `clearVoiceRecord`. | :heavy_check_mark: |
| `onPausePlayProp`      | `Function` | Custom callback triggered to pause voice playback. Defaults to context's `onPausePlay`.                   | :heavy_check_mark: |
| `onResumePlayProp`     | `Function` | Custom callback triggered to resume voice playback. Defaults to context's `onResumePlay`.                 | :heavy_check_mark: |
| `handleGifProp`        | `Function` | Custom callback triggered when selecting a GIF. Defaults to `GiphyDialog.show`.                           | :heavy_check_mark: |

## Features

1. **Voice Recording:**
   - Start, stop, and clear voice recordings.
   - Lock recordings with a slide-to-cancel feature.
   - Supports playback with pause and resume functionality.

2. **GIF Selection:**
   - Integrated GIF picker with customizable callback.

3. **Dynamic Input Styles:**
   - Adapts placeholder text, text color, and styles based on the chatroom type and upload screen state.

4. **Mentions and Styling:**
   - Supports mentions using "@" with configurable styles.

5. **Animations:**
   - Includes Lottie animations for delete actions.

## Usage Example

### Customizing Callbacks and Styling

Define custom callbacks and apply styles dynamically using `STYLES.setInputBoxViewStyles` directly within `MessageInputBox`.

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
    // Customize gif selection behavior
  const handleGifSelection = () => {
    console.log("GIF Picker activated");
  };

  // Customize stop recording behavior
  const handleStopRecording = () => {
    console.log("Recording stopped");
  };

  // Customize clear recording behavior
  const clearRecording = () => {
    console.log("Recording cleared");
  };

  // Define custom styles
  const inputBoxStyles = {
    voiceNotesInputParent: {
      padding: 10,
      backgroundColor: "lightgray",
    },
    recordTitle: {
      fontSize: 16,
      color: "#333",
    },
    emoji: {
      assetPath: "path to your image", // Replace with your image path
      height: 25,
      width: 25,
    },
    chevron: {
      assetPath: "path to your image", // Replace with your image path
      height: 20,
      width: 20,
    },
    input: {
      borderWidth: 1,
      borderColor: "#ccc",
      borderRadius: 8,
      padding: 10,
      backgroundColor: "#f9f9f9",
    },
    stopRecordingIcon: {
      assetPath: "path to your image", // Replace with your image path
      height: 25,
      width: 25,
    },
    crossIcon: {
      assetPath: "path to your image", // Replace with your image path
      height: 20,
      width: 20,
    },
    leftChevronIcon: {
      assetPath: "path to your image", // Replace with your image path
      height: 20,
      width: 20,
    },
    playIcon: {
      assetPath: "path to your image", // Replace with your image path
      height: 25,
      width: 25,
    },
    pauseIcon: {
      assetPath: "path to your image", // Replace with your image path
      height: 25,
      width: 25,
    },
  };
  STYLES.setInputBoxViewStyles(inputBoxStyles);

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
            {/* InputBoxView with dynamic styles from STYLES and custom callbacks */}
            <InputBoxView 
            handleStopRecordProp={handleStopRecording}
            clearVoiceRecordProp={clearRecording}
            handleGifProp={handleGifSelection}/>
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

- Use `MessageInputBox` inside the `MessageInput` component in:
  - [Chatroom Screen](../../Screens/LMChatroomScreen.md)
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)

