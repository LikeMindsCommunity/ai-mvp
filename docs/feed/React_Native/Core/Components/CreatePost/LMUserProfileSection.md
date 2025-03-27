---
sidebar_position: 9
title: Create Post User Profile
slug: /react-native/core/components/universal-feed/create-post-user-profile
---

# LMUserProfileSection

`LMUserProfileSection` is a React component designed to display the user's profile section within the context of creating or editing a post. It showcases the user's profile picture (or initials as a fallback) and the user's name, leveraging styles and data from the context.

<img
src={require('../../../../../static/img/reactNative/createPostUserProfileSection.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Customisations with Styles

| Prop                | Type        | Description                        |
| ------------------- | ----------- | ---------------------------------- |
| `postHeaderStyle`   | `object`    | Custom styles for the post header. |
| `userNameTextStyle` | `TextStyle` | Custom styles for the user name.   |

To see all the properties, visit [PostListStyleProps.header](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L40) & [CreatePostStyleProps.userNameTextStyle](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L298)

## Usage Example

```jsx
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  STYLES,
  LMUserProfileSection,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setPostListStyles({
      header: {
        profilePicture: {
          size: 10,
          fallbackTextBoxStyle: {
            backgroundColor: "pink",
          },
        },
      },
    });
  }, []);

  return (
    <View style={{ flex: 1 }}>
      <LMUserProfileSection />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)