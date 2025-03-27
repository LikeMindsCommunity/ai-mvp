---
sidebar_position: 1
title: How to send metadata in a post to render custom UI?
slug: /react-native/core/guide/how-to-send-meta-data-in-a-post-to-render-custom-ui
---

## Overview

The LikeMinds Feed SDK allows developers to send custom JSON data inside a post. This can be useful for implementing additional features or use cases based on the needs of your application.

To send custom JSON data in a post, you need to create a custom create post screen and pass it to the stack screen. This gives you control over how the post is created and lets you attach custom data.

In this guide, we will walk you through how to set up a custom Create Post screen and send custom JSON data along with the post.

## Prerequisites

Before you begin, ensure the following:

- **LikeMinds Chat React Native SDK**: The SDK must be properly installed and initialized in your React Native project. Refer to the [installation guide](https://docs.likeminds.community/feed/react-native/getting-started) if needed.
- **Basic Understanding of React Native Components**: Familiarity with React Native components concepts.

## Steps To Send Metadata in a Post

### Step 1: Setup Custom Create Post Screen

You can create a custom screen by using the `CreatePost` component from the LikeMinds Feed SDK and overriding some of its default functionality to handle attachments, post creation, and sending custom JSON data.

Below is the code for a custom `CreatePost` screen:

```jsx
import React from "react";
import {
  CreatePost,
  useCreatePostContext,
  CreatePostContextProvider,
  UniversalFeedContextProvider,
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

const CustomCreatePostScreen = ({ navigation, route }) => {
  const { onPostClick } = useCreatePostContext();

  const customHandleCreatePost = (
    allAttachment,
    formattedLinkAttachments,
    postContentText,
    heading,
    topics,
    poll
  ) => {
    // Sending custom JSON data with the post
    onPostClick(
      allAttachment,
      formattedLinkAttachments,
      postContentText,
      heading,
      topics,
      poll,
      metaData: {
        "text": "custom widget is working"
      } // Custom JSON data here
    );
  };

  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <CreatePostContextProvider navigation={navigation} route={route}>
        <CreatePost onPostClickProp={customHandleCreatePost}>
          {/* screen header section */}
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
      </CreatePostContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default CustomCreatePostScreen;
```

In the above code, custom JSON data is sent via the `onPostClick` method. The custom data object:

```json
{
  "text": "custom widget is working"
}
```

is passed when the user creates the post, allowing you to send any relevant data along with the post.

## Steps To Render Metadata in a Post

### Step 1: Create A Custom Universal Feed Screen

1. Create a Custom [Universal Feed Screen](../../Screens/LMFeedUniversalFeedScreen.md) i.e `CustomUniversalFeedScreen`

```tsx
import {
    LMCreatePostButton,
    LMFilterTopics,
    LMPostUploadIndicator,
    LMUniversalFeedHeader,
    PostsList,
    UniversalFeed,
} from "@likeminds.community/feed-rn-core";
import { useAppSelector } from "@likeminds.community/feed-rn-core/store"
import { View } from "react-native"

const CustomUniversalFeedScreen = () => {
 const mappedTopics = useAppSelector((state: any) => state.feed.mappedTopics);
    return (
        {/* @ts-ignore */}
        <View style={{ flex: 1 }}>
            <UniversalFeed isHeadingEnabled={true} isTopResponse={true}>
                <LMUniversalFeedHeader />
                <LMFilterTopics />
                <LMPostUploadIndicator />
                <PostsList
                items={mappedTopics}
                />
                <LMCreatePostButton customText={CUSTOM_TEXT} />
            </UniversalFeed>
        </View>
    );
};
```

2. Create and pass your Custom UI Component as a prop to the `PostsList` Component

```tsx
<PostsList
  items={mappedTopics}
  customWidgetPostView={"<YOUR_CUSTOM_COMPONENT>"}
/>
```

:::tip
For more detailed implementation on How to display your Custom UI Component refer to [this](../how-to-render-custom-post-ui/how-to-render-custom-post-ui.md).
:::

### Step 2: Integrating with the Stack Navigator

Once your `CustomCreatePostScreen` and `CustomUniversalFeedScreen` component is set up, you need to integrate it into your stack navigator to render this screen when required. Here’s an example of how to add the CreateScreen to your stack:

```jsx
import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import CustomCreatePostScreen from "./CustomCreatePostScreen";
import CustomUniversalFeedScreen from "./CustomUniversalFeedScreen";
import { CREATE_POST, UNIVERSAL_FEED } from "@likeminds.community/feed-rn-core";

const Stack = createStackNavigator();

const StackScreen = () => {
  return (
    <Stack.Navigator>
      {/* Other screens */}
      <Stack.Screen
        name={CREATE_POST}
        component={CustomCreatePostScreen} // Reference to your custom CreateScreen
      />
      <Stack.Screen
        name={UNIVERSAL_FEED}
        component={CustomUniversalFeedScreen} // Reference to your custom Universal Feed Screen
      />
    </Stack.Navigator>
  );
};

export default StackScreen;
```

By adding the `CustomCreatePostScreen` to the `Stack.Screen` in the stack navigator, you can navigate to the custom `CREATE_POST` screen from anywhere in your app.
