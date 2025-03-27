---
sidebar_position: 3
title: Post Upload Indicator
slug: /react-native/core/components/universal-feed/post-upload-indicator
---

# Post Upload Indicator

The `LMPostUploadIndicator` component provides a visual indicator while a post is uploading. It displays a loading spinner, a message, and an optional media preview to inform users about the ongoing upload status along with options to retry a failed attempt when uploading a post. This component is designed to be integrated within the Universal Feed.

<img
src={require('../../../../../static/img/reactNative/postUploadIndicator.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## UI Components

- [LMLoader](../Fundamentals/LMFeedLoader.md)

## Customizations with Styles

| Property             | Type          | Description                            |
| -------------------- | ------------- | -------------------------------------- |
| `uploadingTextStyle` | `TextStyle`   | Style for the uploading text.          |
| `retryButtonStyle`   | `object`      | Styles for the retry button.           |
| ├ `buttonStyle`      | `ViewStyle`   | Style for the retry button container.  |
| ├ `iconStyle`        | `LMIconProps` | Style for the retry button icon.       |
| └ `textStyle`        | `TextStyle`   | Style for the retry button text.       |
| `cancelButtonStyle`  | `object`      | Styles for the cancel button.          |
| ├ `buttonStyle`      | `ViewStyle`   | Style for the cancel button container. |
| └ `textStyle`        | `TextStyle`   | Style for the cancel button text.      |
| `progressBarStyle`   | `object`      | Styles for the progress bar.           |
| ├ `size`             | `number`      | Size of the progress bar.              |
| ├ `width`            | `number`      | Width of the progress bar.             |
| └ `tintColor`        | `string`      | Color of the progress bar.             |

## Integration

To use this component, import it and add it as a child of the `UniversalFeed`.

Here’s how you integrate `LMPostUploadIndicator` within a screen:

```jsx
import React from "react";
import {
  LMPostUploadIndicator,
  UniversalFeed,
} from "@likeminds.community/feed-rn-core";

const FeedScreen = () => {
  return (
    <UniversalFeed>
      {/* Other feed components */}
      <LMPostUploadIndicator />
    </UniversalFeed>
  );
};

export default FeedScreen;
```

- Use the `FeedScreen` component with [all other feed components](../../Screens/LMFeedUniversalFeedScreen.md#ui-components) as a child of the `UniversalFeed` component in the relevant screens:
  - [Feed Screen](../../Screens/LMFeedUniversalFeedScreen.md)
