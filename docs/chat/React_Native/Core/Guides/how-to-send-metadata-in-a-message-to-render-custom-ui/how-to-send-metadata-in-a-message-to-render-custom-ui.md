---
sidebar_position: 2
title: How to send metadata in a message to render custom UI?
slug: /react-native/core/guide/how-to-send-metadata-in-a-message-to-render-custom-ui
---

## Overview

The LikeMinds Chat SDK allows developers to send custom JSON data inside a message. This can be useful for implementing additional features or use cases based on the needs of your application.

To send custom JSON data in a message, you need to create a custom Chatroom screen with custom message input component and pass it to the stack screen. This gives you control over how the message is created and lets you attach custom data.

In this guide, we will walk you through how to set up a custom Chatroom screen and send custom JSON data along with the message.

## Prerequisites

Before you begin, ensure the following:

- **LikeMinds Chat React Native SDK**: The SDK must be properly installed and initialized in your React Native project. Refer to the [installation guide](https://docs.likeminds.community/chat/react-native/getting-started) if needed.
- **Basic Understanding of React Native Components**: Familiarity with React Native components concepts.

## Steps To Send Metadata in a Message

### Step 1: Enable Custom Widget Settings

- **Open** your LikeMinds [Admin Dashboard](https://dashboard.likeminds.community).
- **Navigate** to the [Chat Settings Section](https://dashboard.likeminds.community/chat/settings).
- **Enable** Custom Widget in Chat Setting.

### Step 2: Create Custom Message Input Box Component To Send Metadata

To send metadata along with a message, you need to create a custom message input component. This involves modifying the onSend method to include a custom JSON object.

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
} from "@likeminds.community/chat-rn-core";
import RecordSendInputFabView from "@likeminds.community/chat-rn-core/ChatSX/components/RecordSendInputFabView";

const CustomMessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  const onSendMessageProp = (
    message,
    metaData,
    voiceNote,
    isSendWhileVoiceNoteRecorderPlayerRunning
  ) => {
    onSend(
      message, // you can pass your custom message
      {
        text: "custom widget is working",
      }, // you can pass your custom json data
      voiceNote,
      isSendWhileVoiceNoteRecorderPlayerRunning
    );
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
            <AddFilesView />
          </TextInputWrapper>
        </InputWrapperLeftSection>

        {/* Send message and send voice notes UI */}
        <RecordSendInputFabView onSendMessageProp={onSendMessageProp} />
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

export default CustomMessageInputBox;
```

### Step 3: Setup Custom Chatroom and File Upload Screen

- Use the `CustomMessageInputBox` component as a child of the `MessageInput` component in the relevant screens:
  - [Chatroom Screen](../../Screens/LMChatroomScreen.md)
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)

In the [Step 2](#step-2-create-custom-message-input-box-component-to-send-metadata) code, custom JSON data is sent via the `onSend` method inside `onSendMessageProp` method. The custom data object:

```json
{
  "text": "custom widget is working"
}
```

is passed when the user creates the message, allowing you to send any relevant data along with the message.

## Steps to render metadata in a message

### Step 1: Pass Your Custom UI Component as Prop

- Pass the Custom UI Component in the `MessageList` Component present inside your [Custom Chatroom Screen](../../Screens/LMChatroomScreen.md).

:::tip
For more detailed implementation on How to display your Custom UI Component refer to [this](../how-to-render-custom-message-ui/how-to-render-custom-message-ui.md).
:::

```tsx
<MessageList customWidgetMessageView={"<CUSTOM_MESSAGE_VIEW_COMPONENT>"} />
```

### Step 2: Integrating with the Stack Navigator

Once your `ChatroomScreenWrapper` component is set up, you need to integrate it into your stack navigator to render this screen when required. Here’s an example of how to add the `ChatroomScreenWrapper` to your stack:

```jsx
import React from "react";
import { Platform } from "react-native";
import { createStackNavigator } from "@react-navigation/stack";
import { ScreenName } from "@likeminds.community/chat-rn-core";
import ChatroomScreenWrapper from "<path_to_custom_chatroom_screen_wrapper>";
import FileUploadScreenWrapper from "<path_to_custom_file_upload_screen_wrapper>";

const Stack = createStackNavigator();

const StackScreen = () => {
  return (
    <Stack.Navigator>
      {/* Other screens */}
      <Stack.Screen
        name={ScreenName.Chatroom}
        component={ChatroomScreenWrapper}
        options={{
          gestureEnabled: Platform.OS === "ios" ? false : true,
        }}
      />
      <Stack.Screen
        options={{
          gestureEnabled: Platform.OS === "ios" ? false : true,
        }}
        name={ScreenName.FileUpload}
        component={FileUploadScreenWrapper}
        initialParams={{
          backIconPath: "", // add your back icon path here
          imageCropIcon: "", // add your image crop icon path here
        }}
      />
    </Stack.Navigator>
  );
};

export default StackScreen;
```

## Conclusion

By following this guide, you can send and render metadata in a message. This approach provides flexibility to tailor the messaging experience to your application's specific requirements.
