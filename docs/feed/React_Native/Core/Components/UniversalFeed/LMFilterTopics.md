---
sidebar_position: 2
title: Filter Topics
slug: /react-native/core/components/universal-feed/filter-topics
---

# Filter Topics

The `LMFilterTopics` component enables users to filter posts based on selected topics within the Universal Feed. This component displays a scrollable list of selected topics, allowing users to filter, add, or remove topics dynamically. It also includes a "Clear" button to reset topic filters and fetches all available topics from the server.

<img
src={require('../../../../../static/img/reactNative/filterTopicsSelected.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMFilterTopics` provides:
- A selectable list of topics to filter posts.
- An option to clear selected topics and reset the feed.
- Dynamic topic loading to handle large topic lists efficiently.

## Integration

To use this component, import it and add it as a child of the `UniversalFeed`.

Here’s how you integrate `LMFilterTopics` within a screen:

```jsx
import React from "react";
import { LMFilterTopics, UniversalFeed } from "@likeminds.community/feed-rn-core";

const FeedScreen = () => {
  return (
    <UniversalFeed>
      <LMFilterTopics />
      {/* Other feed components */}
    </UniversalFeed>
  );
};

export default FeedScreen;
```

- Use the `FeedScreen` component with [all other feed components](../../Screens/LMFeedUniversalFeedScreen.md#ui-components) as a child of the `UniversalFeed` component in the relevant screens:
  - [Feed Screen](../../Screens/LMFeedUniversalFeedScreen.md)