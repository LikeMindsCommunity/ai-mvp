---
sidebar_position: 7
title: File Upload Screen
slug: /react-native/core/screens/file-upload-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `FileUpload` screen facilitates the process of uploading files within the LikeMinds chat application. It provides users with an interface to select files from their device, which can include documents, images, and other media types. The screen likely features options to preview selected files and initiate the upload, ensuring a seamless experience for sharing content in conversations.

<img
src={require('../../../../static/img/reactNative/lmFileUpload.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The FileUpload screen serves as a parent component, allowing you to incorporate as many child components as necessary, including your own custom components. Here are a few components that can be utilized to enhance the File Upload.

- [FileUploadHeader](../Components/FileUpload/FileUploadHeader.md)
- [FileUploadView](../Components/FileUpload/FileUploadView.md)
- [MessageInputBox](../Components/MessageInput/MessageInputBox.md)

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `FileUploadScreenWrapper` file which will wrap the `FileUploadScreen` within the `ChatroomContextProvider` so that the callbacks becomes accessible inside of the `FileUploadScreen`.
- Create `fileUploadStyles` for customisation and call the `setFileUploadStyle` to set the customisation.

<Tabs>
<TabItem value="FileUploadScreen" label="FileUploadScreen">

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

</TabItem>
<TabItem value="FileUploadScreenWrapper" label="FileUploadScreenWrapper">

```tsx
import { FileUploadScreen } from "<<path_to_FileUploadScreen.tsx>>";
import { ChatroomContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context";
import { FileUploadContextProvider } from "@likeminds.community/chat-rn-core/ChatSX/context/FileUploadContext";

function FileUploadScreenWrapper() {
  return (
    <ChatroomContextProvider>
      <FileUploadContextProvider>
        <FileUploadScreen />
      </FileUploadContextProvider>
    </ChatroomContextProvider>
  );
}

export default FileUploadScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `FileUploadScreenWrapper` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import {
  FILE_UPLOAD,
  LMOverlayProvider,
  STYLES,
  Themes
} from "@likeminds.community/feed-rn-core";
import { FileUploadScreenWrapper } from "<<path_to_FileUploadScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">} // // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: Platform.OS === "ios" ? false : true }}
            name={FILE_UPLOAD}
            component={FileUploadScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
