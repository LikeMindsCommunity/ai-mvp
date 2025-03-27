---
sidebar_position: 6
title: Create Post Topics
slug: /react-native/core/components/universal-feed/create-post-topics
---

# LMCreatePostTopics

`LMCreatePostTopics` allows users to view and select topics for their post. The component dynamically updates based on the context values and selected topics from Redux state. It also integrates with an external API to fetch topics when necessary.

- Displays selected topics with custom styles.
- Allows navigation to a topic feed to explore additional topics.
- Fetches and filters topics based on their availability and enablement state.
- Supports conditional rendering based on whether predefined topics exist and the visibility settings defined in context.

<img
src={require('../../../../../static/img/reactNative/createPostTopics.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

---

## Customization Options

The component supports the following customization through context, these values need to be passed through `CreatePost` component.

| Property               | Type      | Description                                        |
| ---------------------- | --------- | -------------------------------------------------- |
| `hideTopicsViewCreate` | `boolean` | Flag to hide the topics view when creating a post. |
| `hideTopicsViewEdit`   | `boolean` | Flag to hide the topics view when editing a post.  |

## Customisations with Styles

| Prop                     | Type         | Description                                           |
| ------------------------ | ------------ | ----------------------------------------------------- |
| `selectTopicPlaceholder` | `string`     | Placeholder text for the "Select Topics" button.      |
| `selectedTopicsStyle`    | `ViewStyle`  | Custom styles for the displayed selected topics.      |
| `plusIconStyle`          | `ImageStyle` | Custom style for the "+" icon used to add new topics. |

To see all the properties, visit [TopicsStyle](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L371)

## Usage Example

```jsx
import React, { useEffect } from "react";
import { View } from "react-native";
import { STYLES, LMCreatePostTopics } from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setTopicsStyles({
      selectedTopicsStyle: {
        color: "red",
      },
    });
  }, []);

  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostTopics />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
