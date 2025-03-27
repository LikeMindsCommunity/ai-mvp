---
sidebar_position: 3
title: Create Post Header
slug: /react-native/core/components/universal-feed/create-post-header
---

# LMCreatePostHeader

The `LMCreatePostHeader` component provides the header section for the `CreatePost` screen. It includes a customizable back button, a title, and a "Post" button with conditional logic to handle post creation and editing scenarios.

<img
src={require('../../../../../static/img/reactNative/createPostHeader.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostHeader` offers the following functionality:

- Displays "Create Post" or "Edit Post" based on whether the user is creating or editing a post.

## Callbacks

The component supports callback through context values, which are configured within the `CreatePost` component. It supports the following customizable properties:

| Property                       | Type       | Description                                                                                          |
| ------------------------------ | ---------- | ---------------------------------------------------------------------------------------------------- |
| `onPostClickProp`              | `function` | Custom callback for handling post submission.                                                        |
| `handleScreenBackPressProp`    | `function` | Custom callback for handling back navigation.                                                        |
| `customCreatePostScreenHeader` | `object`   | Style and content customization options for the header section, including the back button and title. |

## Customisations with Styles

| Property              | Type                                                                       | Description                                                                                          |
| --------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `showBackArrow`       | `boolean`                                                                  | Determines whether the back arrow is displayed.                                                      |
| `editPostHeading`     | `string`                                                                   | Text displayed as the heading when editing an existing post.                                         |
| `createPostHeading`   | `string`                                                                   | Text displayed as the heading when creating a new post.                                              |
| `rightComponent`      | `ReactNode`                                                                | Custom component for the right side of the header, typically a button for saving or posting content. |
| `subHeading`          | `string`                                                                   | Optional subheading text displayed below the main heading.                                           |
| `backIcon`            | [`LMIconProps`](../../Components/Fundamentals/LMFeedIcon.md#customisation) | Custom icon for the back arrow, if provided.                                                         |
| `subHeadingTextStyle` | `TextStyle`                                                                | Custom style for the subheading text.                                                                |
| `headingTextStyle`    | `TextStyle`                                                                | Custom style for the main heading text.                                                              |
| `headingViewStyle`    | `ViewStyle`                                                                | Custom style for the container of the heading view.                                                  |

To see all the properties, visit [CreatePostStyleProps.createPostScreenHeader](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L300)

## Example Usage

To use this component, make sure to wrap it within a `CreatePostProvider`. Here’s an example:

```javascript
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  LMCreatePostHeader,
  CreatePostProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setCreatePostStyles({
      createPostScreenHeader: {
        headingTextStyle: { color: "blue" },
      },
    });
  }, []);

  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostHeader />
      {/* Additional CreatePost components */}
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
