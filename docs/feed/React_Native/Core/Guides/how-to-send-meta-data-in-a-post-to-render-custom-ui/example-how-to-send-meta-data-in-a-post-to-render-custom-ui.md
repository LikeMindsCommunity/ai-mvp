---
sidebar_position: 2
title: Example implementation of sending location data in a post
slug: /react-native/core/guide/example-implementation-sending-location-data-in-post
---

## Overview

In this example, we will extend the functionality of the custom create post screen to allow users to enter their location when creating a post. The location will be sent as part of the custom JSON data in the post metadata.

By adding a input tag for users to type in their location, we can capture and send that location in the post’s metadata using the LikeMinds Feed SDK.

## Steps

### Step 1: Create a Custom Create Post Screen

We will modify the custom `CreatePost` screen to include a `TextInput` component where users can enter their location. The location will be stored in the state and sent in the custom JSON when the post is created.

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
  const [location, setLocation] = useState(""); // State for location input

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
        "location": location, // Add the location to the custom JSON data
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

            {/* location input section */}
            <View style={{ marginVertical: 10 }}>
              <Text>Enter Location:</Text>
              <TextInput
                style={{ borderColor: 'gray', borderWidth: 1, padding: 8 }}
                placeholder="Type location"
                value={location}
                onChangeText={setLocation}
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

### Step 2: Capturing the Location

In the above code:

- We use the `useState` hook to create a state variable `location` that holds the value entered by the user.
- A `TextInput` component is added below the `LMCreatePostTopics` component to allow users to type in their location.
- The `onChangeText` prop of the `TextInput` updates the `location` state as the user types.

### Step 3: Sending the Location as Custom JSON Data

The `customHandleCreatePost` function handles the post creation. Inside this function, we pass the `location` value as part of the `metaData` object when `onPostClick` is called.

For example, the custom JSON data could look like this:

```json
{
  "location": "New York City"
}
```

### Step 4: Test the Custom Create Post Screen

Once the changes are made, navigate to the custom `CREATE_POST` screen in your app’s stack. When a user types in their location and creates a post, the location will be sent along with the post metadata.

### Conclusion

By following these steps, you’ve successfully added a `TextInput` field to capture the user’s location and send it as part of the custom JSON data when creating a post. This feature can be extended to send any other kind of custom data as needed.

Once you’ve successfully sent custom JSON data, you will also need to implement a custom Post UI component to receive and display the custom JSON data. For details on how to receive and handle the custom JSON data in your app, refer to the [documentation on handling custom JSON data in the UI](../how-to-render-custom-post-ui/example-add-a-custom-post-type-tag-in-post.md).
