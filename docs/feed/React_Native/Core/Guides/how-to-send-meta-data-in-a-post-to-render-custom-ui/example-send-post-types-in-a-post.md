---
sidebar_position: 3
title: Example implementation of sending post types in a post
slug: /react-native/core/guide/example-sending-post-types-in-a-post
---

## Overview

In this example, we will extend the functionality of the custom create post screen to allow users to enter post types when creating a post. The post types will be sent as part of the custom JSON data in the post metadata.

## Steps

### Step 1: Create a Custom Create Post Screene

We will modify the custom `CreatePost` screen to include a `TextInput` component where users can enter their post types. And will be stored in the state and sent in the custom JSON when the post is created.

Here’s the modified code:

```tsx
import React, { useState } from "react";
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
import { TextInput, View, Text } from "react-native";

const CustomCreatePostScreen = ({ navigation, route }) => {
  const { onPostClick } = useCreatePostContext();
  const [postTypes, setPostTypes] = useState(""); // State for post types

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
        "post_types": postTypes, // Add the post types to the custom JSON data
      }
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

            {/* post types input section */}
            <View style={{ marginVertical: 10 }}>
              <Text>Enter Post Types:</Text>
              <TextInput
                style={{ borderColor: 'gray', borderWidth: 1, padding: 8 }}
                placeholder="Type Post Typed"
                value={postTypes}
                onChangeText={setPostTypes}
              />
            </View>

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

### Step 2: Capturing the Post Types

In the above code:

- We use the `useState` hook to create a state variable `postTypes` that holds the value entered by the user.
- A `TextInput` component is added below the `LMCreatePostTopics` component to allow users to type in their post types.
- The `onChangeText` prop of the `TextInput` updates the `postTypes` state as the user types.

### Step 3: Sending the Post Types as Custom JSON Data

The `customHandleCreatePost` function handles the post creation. Inside this function, we pass the `postTypes` value as part of the `metaData` object when `onPostClick` is called.

For example, the custom JSON data could look like this:

```json
{
  "postTypes": "Question"
}
```

### Step 4: Test the Custom Create Post Screen

Once the changes are made, navigate to the custom `CREATE_POST` screen in your app’s stack. When a user writes in their post types and creates a post, the post types will be sent along with the post metadata.

### Conclusion

By following these steps, you’ve successfully added a `TextInput` field to capture the post types and send it as part of the custom JSON data when creating a post. This feature can be extended to send any other kind of custom data as needed.

Once you’ve successfully sent custom JSON data, you will also need to implement a custom Post UI component to receive and display the custom JSON data. For details on how to receive and handle the custom JSON data in your app, refer to the [documentation on handling custom JSON data in the UI](../how-to-render-custom-post-ui/example-add-a-custom-post-type-tag-in-post.md).
