---
sidebar_position: 5
title: Create Post Button
slug: /react-native/core/components/universal-feed/create-post-button
---

# LMCreatePostButton

The `LMCreatePostButton` component provides an interface to initiate the creation of a new post in the feed. This button is customizable, supports dynamic styling, and integrates analytics for post creation tracking.

<img
src={require('../../../../../static/img/reactNative/createPostButton.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostButton` includes:

- A customizable button that triggers post creation.
- An icon and text that are styleable and can be modified for personalized community themes.
- An integration with `LMFeedAnalytics` for tracking when the post creation process starts.

## Customization with Props

| Property     | Type     | Description                                                 |
| ------------ | -------- | ----------------------------------------------------------- |
| `customText` | `string` | Custom text displayed on the button (e.g., "Ask Question"). |

## Customization with Styles

| Property             | Type         | Description                                                                       |
| -------------------- | ------------ | --------------------------------------------------------------------------------- |
| `newPostButtonStyle` | `ViewStyle`  | Styles for the button’s background and layout, applied via `universalFeedStyle`.  |
| `newPostButtonText`  | `TextStyle`  | Styles for the text on the button, managed via the theme context.                 |
| `newPostIcon`        | `ImageProps` | Styles for the icon, allowing customization of size, color, and other properties. |

## Integration

To use this component, import it and add it as a child of the `UniversalFeed`.

Here’s how you integrate `LMCreatePostButton` within a screen:

```jsx
import React from "react";
import {
  LMCreatePostButton,
  UniversalFeed,
  STYLES,
} from "@likeminds.community/feed-rn-core";

const FeedScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setUniversalFeedStyles({
      newPostButtonStyle: {
        backgroundColor: "yellow",
      },
    });
  }, []);
  return (
    <UniversalFeed>
      <LMCreatePostButton />
      {/* Other feed components */}
    </UniversalFeed>
  );
};

export default FeedScreen;
```

- Use the `FeedScreen` component with [all other feed components](../../Screens/LMFeedUniversalFeedScreen.md#ui-components) as a child of the `UniversalFeed` component in the relevant screens:
  - [Feed Screen](../../Screens/LMFeedUniversalFeedScreen.md)
