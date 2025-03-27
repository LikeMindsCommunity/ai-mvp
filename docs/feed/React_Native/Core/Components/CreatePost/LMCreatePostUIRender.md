---
sidebar_position: 7
title: Create Post UI Render
slug: /react-native/core/components/universal-feed/create-post-ui-render
---

# LMCreatePostUIRender

`LMCreatePostUIRender` is a React component that renders the UI elements for creating or editing a post. It provides different UI layouts based on whether the post is in edit mode and whether post details are available. The component also displays a loader while waiting for post details.

<img
src={require('../../../../../static/img/reactNative/createPostUiRender.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Usage Example

```jsx
import React from "react";
import { View, Text, TextInput } from "react-native";
import {LMCreatePostUIRender, LMCreatePostAnonymousCheckbox, LMCreatePostTopics, LMCreatePostHeading} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostUIRender>
        {/* Anonymous post checkbox */}
        <LMCreatePostAnonymousCheckbox />

        {/* post topics section */}
        <LMCreatePostTopics />

        {/* post heading section */}
        <LMCreatePostHeading />

        {/* ...other required components*/}
      </LMCreatePostUIRender>
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
