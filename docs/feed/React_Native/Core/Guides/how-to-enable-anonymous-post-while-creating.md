---
sidebar_position: 7
title: How to Enable Anonymous Post while Creating?
slug: /react-native/core/guide/how-to-enable-anonymous-post-while-creating.md
---

# How to Enable Anonymous Posting in the Create Post Screen

This guide walks you through enabling anonymous posting when creating a post with the LikeMinds Feed SDK in React Native. By setting a specific prop, you can allow users to post anonymously.

## Step 1: Create a Custom Create Post Screen and pass `isAnonymousPostAllowed` as true

Ensure you have imported the necessary components from `@likeminds.community/feed-rn-core`.

```jsx
import React from "react";
import {
  CreatePost,
  useCreatePostContext,
} from "@likeminds.community/feed-rn-core";
import {
  CreatePostContextProvider,
  UniversalFeedContextProvider,
  LMCreatePostAttachmentSelection,
  LMCreatePostHeader,
  LMCreatePostHeading,
  LMCreatePostMedia,
  LMCreatePostTextInput,
  LMCreatePostTopics,
  LMCreatePostUIRender,
  LMCreatePostUserTagging,
  LMUserProfileSection,
  LMCreatePostAnonymousCheckbox,
} from "@likeminds.community/feed-rn-core";
import STYLES from "@likeminds.community/feed-rn-core/constants/Styles";

const CreatePostScreen = () => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <CreatePostContextProvider navigation={navigation} route={route}>
        <CreatePost isHeadingEnabled={false} isAnonymousPostAllowed={true}>
          <LMCreatePostHeader />
          <LMCreatePostUIRender>
            <LMUserProfileSection />
            <LMCreatePostAnonymousCheckbox />
            <LMCreatePostTopics />
            <LMCreatePostHeading />
            <LMCreatePostTextInput />
            <LMCreatePostUserTagging />
            <LMCreatePostMedia />
          </LMCreatePostUIRender>
          <LMCreatePostAttachmentSelection />
        </CreatePost>
      </CreatePostContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default CreatePostScreen;
```

### Step 2: Integrating with the Stack Navigator

Once your `CustomCreatePostScreen` component is set up, you need to integrate it into your stack navigator to render this screen when required. Here’s an example of how to add the CreateScreen to your stack:

```jsx
import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import CustomCreatePostScreen from "<path_to_custom_create_post_screen";
import { CREATE_POST } from "@likeminds.community/feed-rn-core";

const Stack = createStackNavigator();

const StackScreen = () => {
  return (
    <Stack.Navigator>
      {/* Other screens */}
      <Stack.Screen
        name={CREATE_POST}
        component={CustomCreatePostScreen} // Reference to your custom CreateScreen
      />
    </Stack.Navigator>
  );
};

export default StackScreen;
```
