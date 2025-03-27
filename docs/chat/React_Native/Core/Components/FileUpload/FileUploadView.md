---
sidebar_position: 2
title: File Upload View
slug: /react-native/core/components/file-upload-view
---

### Overview

The `FileUploadView` component is responsible for displaying the selected file based on its type (Image, Video, Pdf, or Gif) within the file upload flow. It handles different file types by rendering appropriate views such as an image viewer, a video player, or a PDF thumbnail.

<img
src={require('../../../../../static/img/reactNative/file-view.webp').default}
alt="LMChatCustomWidgetScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

### Component Structure

1. **File Display**:
   - The component checks the file type and displays the selected file accordingly.
   - It supports the following types:
     - **Image**: Displays the image using the `Image` component.
     - **Video**: Displays the video using the `react-native-media-console` video player.
     - **PDF**: Displays a PDF thumbnail using an image.
     - **GIF**: Displays the GIF.

## Usage Example

```tsx
import { View } from "react-native";
import React from "react";
import { useChatroomContext } from "@likeminds.community/chat-rn-core";
import { useFileUploadContext } from "@likeminds.community/chat-rn-core/ChatSX/context/FileUploadContext";
import styles from "@likeminds.community/chat-rn-core/ChatSX/screens/FIleUpload/styles";
import FileUploadHeader from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadHeader";
import FileUploadView from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadView";
import FileUploadMessageInput from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadMessageInput";
import { InputBoxContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext";
import { PDF_TEXT } from "@likeminds.community/chat-rn-core/ChatSX/constants/Strings";
import MessageInputBox from "@likeminds.community/chat-rn-core/ChatSX/components/InputBox";
import FileUploadBottomScrollView from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadBottomScrollView";

const FileUploadScreen = () => {
  const { chatroomType } = useChatroomContext();
  const {
    docItemType,
    chatroomID,
    previousMessage,
    handleFileUpload,
    isGif,
    chatroomDBDetails,
  } = useFileUploadContext();
  return (
    <View style={styles.page}>
      <FileUploadHeader />
      {/* Add FileUploadView component like this */}
      <FileUploadView />
      <FileUploadMessageInput>
        <InputBoxContextProvider
          isUploadScreen={true}
          isDoc={docItemType === PDF_TEXT ? true : false}
          chatroomID={chatroomID}
          previousMessage={previousMessage}
          handleFileUpload={handleFileUpload}
          isGif={isGif}
          chatroomType={chatroomType}
          isPrivateMember={chatroomDBDetails.isPrivateMember}
          chatRequestState={chatroomDBDetails.chatRequestState}
        >
          <MessageInputBox />
        </InputBoxContextProvider>
      </FileUploadMessageInput>
      <FileUploadBottomScrollView />
    </View>
  );
};

export default FileUploadScreen;
```

### Customise `<FileUploadView />` UI Component

- Create a new component `CustomFileUploadView`, referencing the [`FileUploadView`](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/FileUploadView/index.tsx) component.
- Perform your UI customizations in the new component.

```tsx
import { View } from "react-native";
import React from "react";
import { useChatroomContext } from "@likeminds.community/chat-rn-core";
import { useFileUploadContext } from "@likeminds.community/chat-rn-core/ChatSX/context/FileUploadContext";
import styles from "@likeminds.community/chat-rn-core/ChatSX/screens/FIleUpload/styles";
import FileUploadHeader from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadHeader";
import FileUploadView from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadView";
import FileUploadMessageInput from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadMessageInput";
import { InputBoxContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context/InputBoxContext";
import { PDF_TEXT } from "@likeminds.community/chat-rn-core/ChatSX/constants/Strings";
import MessageInputBox from "@likeminds.community/chat-rn-core/ChatSX/components/InputBox";
import FileUploadBottomScrollView from "@likeminds.community/chat-rn-core/ChatSX/components/FileUploadBottomScrollView";

const CustomFileUploadHeader = () => {
  const { chatroomType } = useChatroomContext();
  const {
    docItemType,
    chatroomID,
    previousMessage,
    handleFileUpload,
    isGif,
    chatroomDBDetails,
  } = useFileUploadContext();
  return (
    <View style={styles.page}>
      <FileUploadHeader />
      {/* Add CustomFileUploadView component like this */}
      <CustomFileUploadView />
      <FileUploadMessageInput>
        <InputBoxContextProvider
          isUploadScreen={true}
          isDoc={docItemType === PDF_TEXT ? true : false}
          chatroomID={chatroomID}
          previousMessage={previousMessage}
          handleFileUpload={handleFileUpload}
          isGif={isGif}
          chatroomType={chatroomType}
          isPrivateMember={chatroomDBDetails.isPrivateMember}
          chatRequestState={chatroomDBDetails.chatRequestState}
        >
          <MessageInputBox />
        </InputBoxContextProvider>
      </FileUploadMessageInput>
      <FileUploadBottomScrollView />
    </View>
  );
};

export default CustomFileUploadHeader;
```

- Use the `CustomFileUploadHeader` component as a child of the `FileUploadScreen` component:
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)
