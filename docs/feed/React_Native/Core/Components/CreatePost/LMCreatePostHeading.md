---
sidebar_position: 3
title: Create Post Heading
slug: /react-native/core/components/universal-feed/create-post-heading
---

# LMCreatePostHeading

The `LMCreatePostHeading` component is responsible for the heading section of the post creation screen. It allows users to input a heading for the post, displaying a character count and providing conditional rendering based on the `isHeadingEnabled` context.

<img
src={require('../../../../../static/img/reactNative/createPostHeading.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostHeading` provides the following functionality:

- Displays an input field for the post heading with a character limit.
- Shows a separator line and character counter.
- Supports dark/light theme modes.
- The heading input section is conditionally rendered based on the `isHeadingEnabled` context.

## Props

The component supports callback and properties through context values, which are configured within the `CreatePost` component.

| Property           | Type      | Description                                                                |
| ------------------ | --------- | -------------------------------------------------------------------------- |
| `isHeadingEnabled` | `boolean` | Determines if the heading input section and related UI elements are shown. |

## Example Usage

To use this component, make sure the `CreatePostContext` and `CreatePostCustomisableMethodsContext` are properly set up in the parent component.

```javascript
import React from "react";
import { View } from "react-native";
import { LMCreatePostHeading } from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostHeading />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
