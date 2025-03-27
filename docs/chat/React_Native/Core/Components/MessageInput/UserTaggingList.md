---
sidebar_position: 5
title: User Tagging List
slug: /react-native/core/components/user-tagging-list
---

## Overview

The `UserTaggingList` component provides a dynamic, scrollable interface for displaying a list of users or groups that can be tagged in messages. It supports user interaction for tagging functionality, customizable UI, and efficient rendering using `FlashList` from Shopify.

This component is primarily used in conjunction with the input box for tagging users in chat messages or posts.

<img
src={require('../../../../../static/img/reactNative/user-tagging.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The `UserTaggingList` is composed of several elements that enhance its functionality and usability:

- **List of Users/Groups:** A scrollable list of users or groups available for tagging.
- **Pressable Items:** Each user or group is a clickable item, enabling tagging interaction.
- **Customizable Appearance:** Supports dynamic styling based on context (e.g., upload screen, theme).

# Theming Customizations

The UserTaggingList component now supports additional theming through `inputBoxStyles.userTaggingListStyles`. The following properties have been added:

| Property Name | Type | Description |
|---------------|------|-------------|
| containerStyle | ViewStyle | Custom styling for the user tagging list container. |
| mentionItemStyle | ViewStyle | Custom styling for individual mention items in the list. |
| mentionTextStyle | TextStyle | Custom styling for the text inside the mention items. |
| highlightStyle | TextStyle | Custom styling for the highlighted mention. |
| mentionIconStyle | LMChatIconProps | Customize the mention icon, including asset path, height, width, and style. |

These styles can be applied to customize the appearance of the user tagging list in your chat application.

## Props

| Property                   | Type       | Description                                                                                                                                                          | Optional           |
| -------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `onUserTaggingClickedProp` | `Function` | Custom callback function triggered when a user/group is selected for tagging. Accepts an object containing `uuid`, `userName`, `communityId`, and `mentionUsername`. | :heavy_check_mark: |

### Callback Object

The `onUserTaggingClickedProp` callback object includes the following properties:

- **uuid:** Unique identifier for the user or group.
- **userName:** Name of the user or group.
- **communityId:** Identifier for the community to which the user or group belongs.
- **mentionUsername:** Username to be displayed as the mention.

## Features

1. **Dynamic User List:**

   - Combines group tags and user tagging data.
   - Displays a scrollable list using the highly performant `FlashList`.

2. **User Interaction:**

   - Items are clickable, triggering tagging functionality.
   - Supports custom and default callbacks for tagging actions.

3. **Custom Styling:**

   - Adaptable styling for different contexts (e.g., dark mode in upload screens).

4. **Efficient Rendering:**
   - Uses `FlashList` for fast, responsive rendering of long lists.
   - Includes pagination with `onEndReached` and a customizable footer.

## Usage Example

### Applying Callbacks & Styling to `MessageInputBox`

Define custom callbacks and apply custom styles using `STYLES.setUserTaggingListStyles` directly within `MessageInputBox`.

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

const MessageInputBox = () => {
  const { hideDMSentAlert, message, DMSentAlertModalVisible, onSend } =
    useInputBoxContext();

  // To customize the user tagging click method, you can create your own and modify it as needed. Otherwise, simply avoid passing it as a prop to the UserTaggingList component
  const handleUserTaggingClick = ({
    uuid,
    userName,
    communityId,
    mentionUsername,
  }: {
    uuid: string;
    userName: string;
    communityId: string;
    mentionUsername: string;
  }) => {
    console.log("Tagged User:", {
      uuid,
      userName,
      communityId,
      mentionUsername,
    });
  };

  
// Define styles for the UserTaggingList component customization
const userTaggingListStyles = {
  containerStyle: {
    backgroundColor: "white",
    padding: 10,
    borderRadius: 10,
  },
  mentionItemStyle: {
    padding: 5,
    marginVertical: 2,
    backgroundColor: "#F0F0F0",
    borderRadius: 5,
  },
  mentionTextStyle: {
    fontSize: 14,
    color: "#333",
  },
  highlightStyle: {
    fontWeight: "bold",
    color: "#007AFF",
  },
  mentionIconStyle: {
    assetPath: require("Path to Your Image"),
    height: 24,
    width: 24,
    iconStyle: { tintColor: "#007AFF" },
  },
};

// Applying styles using setStyle
STYLES.setUserTaggingListStyles("userTaggingListStyles", userTaggingListStyles);

  return (
    <View>
      <VoiceNoteRecordToast />

      <InputWrapper>
        <InputWrapperLeftSection>
          {/* UserTaggingList with dynamic styles from STYLES and custom callbacks */}
          <UserTaggingList onUserTaggingClickedProp={handleUserTaggingClick} />
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

export default MessageInputBox;
```


- Use the `MessageInputBox` component as a child of the `MessageInput` component in the relevant screens:
  - [Chatroom Screen](../../Screens/LMChatroomScreen.md)
  - [File Upload Screen](../../Screens/LMChatroomFileUploadScreen.md)
