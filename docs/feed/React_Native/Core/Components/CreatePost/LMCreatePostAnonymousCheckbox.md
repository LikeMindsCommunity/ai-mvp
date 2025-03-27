---
sidebar_position: 1
title: Create Post Anonymous Checkbox
slug: /react-native/core/components/universal-feed/create-post-anonymous-checkbox
---

# LMCreatePostAnonymousCheckbox

The `LMCreatePostAnonymousCheckbox` component allows users to choose if they want to create a post anonymously. This checkbox is contextually aware and adapts based on the component's current state, such as post editing status and configuration settings.

<img
src={require('../../../../../static/img/reactNative/createPostAnonymousCheckbox.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostAnonymousCheckbox` includes:

- A customizable checkbox for enabling anonymous posting.
- An optional hint text that provides guidance on anonymous posting.
- Integration with `CreatePostContext` for managing anonymous post settings dynamically.

## Customization Options

The component supports the following customization through context, these values need to be passed through `CreatePost` component.

| Property                           | Type       | Description                                                                                           |
| ---------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------- |
| `hintTextForAnonymous`             | `string`   | Custom hint text displayed alongside the checkbox (e.g., "Post anonymously to protect your privacy"). |
| `isAnonymousPostAllowed`           | `boolean`  | Determines if anonymous posting is enabled for the community.                                         |
| `handleOnAnonymousPostClickedProp` | `function` | Optional custom callback function for handling the anonymous post toggle.                             |

## Example Usage

To use this component, ensure that it's wrapped within a provider that supplies `CreatePostContext` and `CreatePostCustomisableMethodsContext`. Here’s an example of how to include `LMCreatePostAnonymousCheckbox` in a `CreatePost` screen:

```javascript
import React from "react";
import { View } from "react-native";
import {
  LMCreatePostAnonymousCheckbox,
  CreatePostProvider,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  return (
    <View style={{ flex: 1 }}>
      {/* Other create post components */}
      <LMCreatePostAnonymousCheckbox />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
