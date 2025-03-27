---
sidebar_position: 8
title: Create Post User Tagging
slug: /react-native/core/components/universal-feed/create-post-user-tagging
---

# LMCreatePostUserTagging

`LMCreatePostUserTagging` is a React component used to display and handle user tagging functionality within a post creation screen. It allows users to tag other users by displaying a list of suggestions and updating the post content with tagged usernames.

<img
src={require('../../../../../static/img/reactNative/createPostUserTagging.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Customisations with Styles

| Prop                   | Type     | Description                              |
| ---------------------- | -------- | ---------------------------------------- |
| `postHeaderStyle`      | `object` | Custom styles for the post header.       |
| `userTaggingListStyle` | `object` | Custom styles for the user tagging list. |

To see all the properties, visit [PostListStyleProps.header](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L40) & [PostDetailStyleProps.userTaggingListStyle](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L274)

## Usage Example

```jsx
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  STYLES,
  LMCreatePostUserTagging,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setPostDetailStyles({
      userTaggingListStyle: {
        taggingListView: { backgroundColor: "red" },
      },
    });
  }, []);
  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostUserTagging />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
