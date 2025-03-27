---
sidebar_position: 1
title: Universal Feed Header
slug: /react-native/core/components/universal-feed/universal-feed-header
---

# Universal Feed Header

The `LMUniversalFeedHeader` component is designed to serve as the header of the Universal Feed screen. It displays the app's title and a notification bell icon, indicating any unread notifications with a badge. This component leverages contextual styling and behavior, enabling it to adapt to different themes and respond to user interactions.

<img
src={require('../../../../../static/img/reactNative/universalFeedHeader.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMUniversalFeedHeader` is a reusable component that offers:

- A customizable header with a title.
- A notification bell icon, which changes color based on the theme.
- An optional notification badge displaying the count of unread notifications.

## UI Components

- [LMFeedHeader](../Fundamentals/LMFeedHeader.md)

## Integration

To use this component, import it and add it as a child of the `UniversalFeed`.

Here’s how you integrate `LMUniversalFeedHeader` within a screen:

```jsx
import React, { useEffect } from "react";
import {
  LMUniversalFeedHeader,
  UniversalFeed,
  STYLES,
} from "@likeminds.community/feed-rn-core";

const FeedScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setUniversalFeedStyles({
      screenHeader: {
        headingTextStyle: {
          color: "blue",
        },
      },
    });
  }, []);
  return (
    <UniversalFeed>
      <LMUniversalFeedHeader />
      {/* Other feed components */}
    </UniversalFeed>
  );
};

export default FeedScreen;
```

- Use the `FeedScreen` component with [all other feed components](../../Screens/LMFeedUniversalFeedScreen.md#ui-components) as a child of the `UniversalFeed` component in the relevant screens:
  - [Feed Screen](../../Screens/LMFeedUniversalFeedScreen.md)
