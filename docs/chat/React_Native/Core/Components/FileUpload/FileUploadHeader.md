---
sidebar_position: 1
title: File Upload Header
slug: /react-native/core/components/file-upload-header
---

### Overview

The `FileUploadHeader` component provides the header section of the file upload screen. It allows users to navigate back to the previous screen and optionally crop the image they are viewing, depending on the file type being uploaded. It also manages state related to file selection and resets the status bar style when navigating back.

<img
src={require('../../../../../static/img/reactNative/file-header.webp').default}
alt="LMChatCustomWidgetScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

### Component Structure

1. **Heading Container**:

   - A wrapper view that displays the header items only if there are files selected for upload.

2. **Back Button**:

   - A button that allows users to navigate back to the previous screen.
   - It dispatches actions to clear the selected files from the state and reset the status bar style.

3. **Image Crop Button**:
   - If the selected attachment type is an image, an additional button is rendered to allow the user to navigate to the image cropping screen.

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
      {/* Add FileUploadHeader component like this */}
      <FileUploadHeader />
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

### Customise `<FileUploadHeader />` UI Component

- Create a new component `CustomFileUploadHeader`, referencing the [`FileUploadHeader`](https://github.com/LikeMindsCommunity/likeminds-chat-reactnative/blob/master/likeminds-chat-reactnative-integration/ChatSX/components/FileUploadHeader/index.tsx) component.
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
import CustomFileUploadHeader from "<path_to_custom_file_upload_header_component>";

const CustomFileUploadScreen = () => {
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
      {/* Add CustomFileUploadHeader component like this */}
      <CustomFileUploadHeader />
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

export default CustomFileUploadScreen;
```

- Use the `CustomFileUploadHeader` component as a child of the `FileUploadScreen` component:
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)
