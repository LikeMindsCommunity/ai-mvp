---
sidebar_position: 4
title: Create/Edit Post
slug: /react-native/core/screens/create-or-edit-post-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `CreatePost` screen allows users to create posts by adding text, images, videos, and documents. It provides various UI components and functionalities to facilitate the post creation process.

<img
src={require('../../../../static/img/iOS/screens/createPost.webp').default}
alt="LMFeedCreatePostScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMCreatePostHeader](../Components/CreatePost/LMCreatePostHeader.md)
- [LMCreatePostUIRender](../Components/CreatePost/LMCreatePostUIRender.md)
- [LMUserProfileSection](../Components/CreatePost/LMUserProfileSection.md)
- [LMCreatePostTopics](../Components/CreatePost/LMCreatePostTopics.md)
- [LMCreatePostHeading](../Components/CreatePost/LMCreatePostHeading.md)
- [LMCreatePostTextInput](../Components/CreatePost/LMCreatePostTextInput.md)
- [LMCreatePostUserTagging](../Components/CreatePost/LMCreatePostUserTagging.md)
- [LMCreatePostMedia](../Components/CreatePost/LMCreatePostMedia.md)
- [LMCreatePostAttachmentSelection](../Components/CreatePost/LMCreatePostAttachmentSelection.md)
- [LMCreatePostAnonymousCheckbox](../Components/CreatePost/LMCreatePostAnonymousCheckbox.md)

## Data Variables

- `postToEdit`: Boolean to determine that whether it is creation of a new post or edition of an existing post.
- `memberData`: Data of the logged in member conforming to [`LMUserViewData`](../Models/LMUserViewData.md).

## Callbacks

- `handleGalleryProp`: Triggered when the gallery is accessed, providing the type of gallery as a string.
- `handleDocumentProp`: Triggered when a document is accessed.
- `handlePollProp`: Triggered when a poll is accessed.
- `onPostClickProp`: Triggered when a post is clicked, providing:
  - `allMedia`: An array of media attachments (`LMAttachmentViewData`).
  - `linkData`: An array of link attachments (`LMAttachmentViewData`).
  - `content`: The content of the post as a string.
  - `heading`: The heading of the post as a string.
  - `topics`: An array of topics as strings.
  - `poll`: The poll data.
  - `isAnonymous` (optional): A boolean indicating if the post is anonymous.
- `handleScreenBackPressProp`: Triggered when the back button is pressed on a screen.
- `handleOnAnonymousPostClickedProp`: Triggered when an anonymous post is clicked, with `isAnonymous` as a boolean indicating the anonymity status.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/context/createPostCallbacksContext.tsx).

## Customisation with Props

| Property                 | Type      | Description                                            | Required           |
| ------------------------ | --------- | ------------------------------------------------------ | ------------------ |
| `isHeadingEnabled`       | `boolean` | Enables or disables the heading.                       | :heavy_check_mark: |
| `hideTopicsViewCreate`   | `boolean` | Hides the topics view on the create post screen.       |                    |
| `hideTopicsViewEdit`     | `boolean` | Hides the topics view on the edit post screen.         |                    |
| `isAnonymousPostAllowed` | `boolean` | Allows the creation of anonymous posts if set to true. |                    |
| `hintTextForAnonymous`   | `string`  | Provides a hint text specifically for anonymous posts. |                    |

## Customisation with Styles

| Property                   | Type                                                    | Description                                              | Required           |
| -------------------------- | ------------------------------------------------------- | -------------------------------------------------------- | ------------------ |
| `userNameTextStyle`        | `TextStyle`                                             | Represents the style of the username text.               |                    |
| `createPostScreenHeader`   | [`CreatePostScreenHeader`](#createpostscreenheader)     | Contains properties for the create post screen header.   |                    |
| `attachmentOptionsStyle`   | [`AttachmentOptionsStyle`](#attachmentoptionsstyle)     | Contains styles for attachment options.                  | :heavy_check_mark: |
| `createPostTextInputStyle` | [`CreatePostTextInputStyle`](#createposttextinputstyle) | Contains styles for the create post text input.          | :heavy_check_mark: |
| `addMoreAttachmentsButton` | [`AddMoreAttachmentsButton`](#addmoreattachmentsbutton) | Contains properties for the add more attachments button. | :heavy_check_mark: |

### CreatePostScreenHeader

| Property              | Type                                                      | Description                                      |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------ |
| `showBackArrow`       | `boolean`                                                 | Indicates whether to show the back arrow.        |
| `editPostHeading`     | `string`                                                  | The heading text when editing a post.            |
| `createPostHeading`   | `string`                                                  | The heading text when creating a new post.       |
| `rightComponent`      | `React.ReactNode`                                         | The component to be displayed on the right side. |
| `subHeading`          | `string`                                                  | The subheading text to be displayed.             |
| `backIcon`            | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Represents the back icon properties.             |
| `subHeadingTextStyle` | `TextStyle`                                               | Represents the style of the subheading text.     |
| `headingTextStyle`    | `TextStyle`                                               | Represents the style of the heading text.        |
| `headingViewStyle`    | `ViewStyle`                                               | Represents the style of the heading view.        |

### AttachmentOptionsStyle

| Property                   | Type                                                      | Description                               |
| -------------------------- | --------------------------------------------------------- | ----------------------------------------- |
| `attachmentOptionsView`    | `ViewStyle`                                               | Style for the attachment options view.    |
| `photoAttachmentView`      | `ViewStyle`                                               | Style for the photo attachment view.      |
| `photoAttachmentIcon`      | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Properties for the photo attachment icon. |
| `photoAttachmentTextStyle` | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Style for the photo attachment text.      |
| `videoAttachmentView`      | `ViewStyle`                                               | Style for the video attachment view.      |
| `videoAttachmentIcon`      | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Properties for the video attachment icon. |
| `videoAttachmentTextStyle` | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Style for the video attachment text.      |
| `filesAttachmentView`      | `ViewStyle`                                               | Style for the files attachment view.      |
| `filesAttachmentIcon`      | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Properties for the files attachment icon. |
| `filesAttachmentTextStyle` | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Style for the files attachment text.      |

### CreatePostTextInputStyle

| Property               | Type        | Description                                   |
| ---------------------- | ----------- | --------------------------------------------- |
| `inputTextStyle`       | `TextStyle` | Style for the input text.                     |
| `placeholderText`      | `string`    | Text to be displayed when the input is empty. |
| `placeholderTextColor` | `string`    | Color of the placeholder text.                |
| `rightIcon`            | `Object`    | Properties for the right icon of the input.   |
| `textValueStyle`       | `TextStyle` | Style for the text value.                     |
| `mentionTextStyle`     | `TextStyle` | Style for the mention text.                   |
| `multilineField`       | `boolean`   | Indicates if the input should be multiline.   |

### AddMoreAttachmentsButton

| Property      | Type                                                      | Description                            | Required           |
| ------------- | --------------------------------------------------------- | -------------------------------------- | ------------------ |
| `text`        | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Properties for the text on the button. | :heavy_check_mark: |
| `icon`        | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Properties for the icon on the button. | :heavy_check_mark: |
| `onTap`       | `Function`                                                | Function to execute on button tap.     | :heavy_check_mark: |
| `placement`   | `"start"` or `"end"`                                      | Placement of the icon on the button.   | :heavy_check_mark: |
| `buttonStyle` | `ViewStyle`                                               | Style for the button.                  | :heavy_check_mark: |
| `isClickable` | `boolean`                                                 | Indicates if the button is clickable.  | :heavy_check_mark: |

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `CreatePostScreenWrapper` file which will wrap the `CreatePostScreen` within the `CreatePostContextProvider` along with `UniversalFeedContextProvider` so that the callbacks becomes accessible inside of the `CreatePostScreen`.
- Create `createPostStyles` for customisation and call the `setCreatePostStyles` to set the customisation.

<Tabs>
<TabItem value="createPostScreen" label="CreatePostScreen">

```tsx
import React from "react";
import {
  CreatePost,
  useCreatePostContext,
} from "@likeminds.community/feed-rn-core";
import {
  LMCreatePostAttachmentSelection,
  LMCreatePostHeader,
  LMCreatePostHeading,
  LMCreatePostMedia,
  LMCreatePostTextInput,
  LMCreatePostTopics,
  LMCreatePostUIRender,
  LMCreatePostUserTagging,
  LMUserProfileSection,
  LMCreatePostAnonymousCheckbox
} from "@likeminds.community/feed-rn-core";
import STYLES from "@likeminds.community/feed-rn-core/constants/Styles";

const CreatePostScreen = () => {
  const {
    handleDocument,
    handleGallery,
    onPostClick,
    handleScreenBackPress,
    removePollAttachment,
    editPollAttachment,
  } = useCreatePostContext();

  const customHandleDocumentProp = () => {
    console.log("before document handle");
    handleDocument();
    console.log("after document handle");
  };
  const customHandleGalleryProp = (type) => {
    console.log("before gallery handle");
    handleGallery(type);
    console.log("after gallery handle");
  };
  const customHandleCreatePost = (
    allAttachment,
    formattedLinkAttachments,
    postContentText,
    heading,
    topics,
    poll,
    isAnonymous
  ) => {
    console.log("before post click");
    onPostClick(
      allAttachment,
      formattedLinkAttachments,
      postContentText,
      heading,
      topics,
      poll,
      isAnonymous
    );
    console.log("after post click");
  };
  const customBackHandler = () => {
    console.log("before back click");
    handleScreenBackPress();
    console.log("after back click");
  };
  const customPollEditClicked = () => {
    console.log("before edit poll click");
    editPollAttachment();
    console.log("after edit poll  click");
  };
  const customPollClearClicked = () => {
    console.log("before clear poll  click");
    removePollAttachment();
    console.log("after clear poll  click");
  };

  const createPostStyles = {
    userNameTextStyle: {
      color: "green",
    },
    createPostScreenHeader: {
      subHeading: "LikeMinds",
    },
  };

  // hide create poll button to disable poll creation
  const pollStyles = {
    hidePoll: true
  }

  if (pollStyles) {
    STYLES.setPollStyle(pollStyles)
  }
  
  // customisation with styles
  if (createPostStyles) {
    // create post screen customisation
    STYLES.setCreatePostStyles(createPostStyles);
  }

  return (
    <CreatePost
      // callbacks
      handleDocumentProp={() => customHandleDocumentProp()}
      handleGalleryProp={(type) => customHandleGalleryProp(type)}
      onPostClickProp={(
        allAttachment,
        formattedLinkAttachments,
        postContentText,
        heading,
        topics,
        poll,
        isAnonymous
      ) =>
        customHandleCreatePost(
          allAttachment,
          formattedLinkAttachments,
          postContentText,
          heading,
          topics,
          poll,
          isAnonymous
        )
      }
      handleScreenBackPressProp={() => customBackHandler()}
      onPollEditClicked={customPollEditClicked}
      onPollClearClicked={customPollClearClicked}

      // customisation with props
      isHeadingEnabled={true}
      isAnonymousPostAllowed
    >
      {/* screen header section*/}
      <LMCreatePostHeader />

      {/* handles the UI to be rendered for edit post and create post */}
      <LMCreatePostUIRender>
        {/* user profile section */}
        <LMUserProfileSection />

        {/* Anonymous post checkbox */}
        <LMCreatePostAnonymousCheckbox/>

        {/* post topics section */}
        <LMCreatePostTopics />

        {/* post heading section */}
        <LMCreatePostHeading />

        {/* text input field */}
        <LMCreatePostTextInput />

        {/* users tagging list */}
        <LMCreatePostUserTagging />

        {/* selected media section */}
        <LMCreatePostMedia />
        
        {/* selection options section */}
        <LMCreatePostAttachmentSelection />
      </LMCreatePostUIRender>

    </CreatePost>
  );
};

export default CreatePostScreen;
```

</TabItem>
<TabItem value="createPostScreenWrapper" label="CreatePostScreenWrapper">

```tsx
import {
  CreatePostContextProvider,
  UniversalFeedContextProvider,
} from "@likeminds.community/feed-rn-core";
import CreatePostScreen from "<<path_to_CreatePostScreen.tsx>>";

const CreatePostScreenWrapper = ({ navigation, route }) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <CreatePostContextProvider navigation={navigation} route={route}>
        <CreatePostScreen />
      </CreatePostContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default CreatePostScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `CreatePostScreenWrapper` as a Stack screen in your `NavigationContainer`.

```tsx
import {
  CREATE_POST,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import { CreatePostScreenWrapper } from "<<path_to_CreatePostScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={CREATE_POST}
            component={CreatePostScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
