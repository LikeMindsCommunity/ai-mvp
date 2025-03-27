---
sidebar_position: 1
title: Universal Feed
slug: /react-native/core/screens/universal-feed-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

`UniversalFeed` displays a universal feed screen with a topic selection bar and a list of posts, create post button.

<img
src={require('../../../../static/img/iOS/screens/universalFeed.webp').default}
alt="LMUniversalFeedScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

The Universal Feed screen serves as a parent component, allowing you to incorporate as many child components as necessary, including your own custom components. Here are a few components that can be utilized to enhance the universal feed.

- [LMUniversalFeedHeader](../Components/UniversalFeed/LMUniversalFeedHeader.md)
- [LMFilterTopics](../Components/UniversalFeed/LMFilterTopics.md)
- [LMPostUploadIndicator](../Components/UniversalFeed/LMPostUploadIndicator.md)
- [PostsList](../Components/UniversalFeed/LMPostsList.md)
- [LMCreatePostButton](../Components/UniversalFeed/LMCreatePostButton.md)

## Callbacks

Below are the callback props available for `UniversalFeed`, allowing you to handle interactions within the feed.

- `postLikeHandlerProp`: Triggered when a post is liked, receiving the `id` of the post.
- `savePostHandlerProp`: Triggered when a post is saved or unsaved, with `id` and an optional `saved` boolean to indicate save state.
- `selectPinPostProp`: Triggered to pin or unpin a post, receiving `id` and `pinned` status.
- `selectEditPostProp`: Allows editing of a post, receiving `id` and post data.
- `onSelectCommentCountProp`: Triggered on comment count tap, receiving the post `id`.
- `onTapLikeCountProps`: Triggered when the like count is tapped, receiving the post `id`.
- `handleDeletePostProps`: Allows deletion of a post, with `visible` and `postId` parameters.
- `handleReportPostProps`: Handles reporting of a post, receiving the post `id`.
- `newPostButtonClickProps`: Custom action for the new post button click.
- `onOverlayMenuClickProp`: Custom action for overlay menu clicks, receiving event data, menu items, and the post `id`.
- `onTapNotificationBellProp`: Triggered on tapping the notification bell.
- `onSharePostClicked`: Handles post sharing, receiving the post `id`.
- `onSubmitButtonClicked`: Custom action for poll submission.
- `onAddPollOptionsClicked`: Custom action for adding poll options.
- `onPollOptionClicked`: Custom action when a poll option is clicked.
- `onCancelPressProp`: Custom action when cancel button is pressed for upload retry. 
- `onRetryPressProp`: Custom action when retry button is pressed for upload retry.
- `onSearchIconClickProp`: Custom action when search icon is pressed.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/context/universalFeedCallbacksContext.tsx).

## Customisation with Props

| Property           | Type      | Description                                              | Required           |
| ------------------ | --------- | -------------------------------------------------------- | ------------------ |
| `isHeadingEnabled` | `boolean` | Enables or disables the heading display.                 | :heavy_check_mark: |
| `isTopResponse`    | `boolean` | Shows the top response if set to true.                   |                    |
| `hideTopicsView`   | `boolean` | Hides the topics view on the feed screen if set to true. |                    |

## Customization with Styles

| Property             | Type                                                          | Description                                 |
| -------------------- | ------------------------------------------------------------- | ------------------------------------------- |
| `newPostButtonStyle` | `ViewStyle`                                                   | Style for the new post button.              |
| `newPostButtonText`  | `TextStyle`                                                   | Style for the text of the new post button.  |
| `newPostIcon`        | [`LMImageProps`](../Components/Media/LMFeedImage.md)          | Icon properties for the new post button.    |
| `screenHeader`       | [`LMHeaderProps`](../Components/Fundamentals/LMFeedHeader.md) | Header component properties for the screen. |

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `FeedScreenWrapper` file which will wrap the `FeedScreen` within the `UniversalFeedContextProvider` and `PostListContextProvider` so that the callbacks becomes accessible inside of the `FeedScreen`.
- Create `universalFeedStyles` for customisation and call the `setUniversalFeedStyles` to set the customisation.

<Tabs>
<TabItem value="FeedScreen" label="FeedScreen">

```tsx
import React, { useEffect, useState } from "react";
import {
  LMCreatePostButton,
  LMFilterTopics,
  LMPostUploadIndicator,
  LMUniversalFeedHeader,
  PostsList,
  UniversalFeed,
  usePostListContext,
  useUniversalFeedContext,
} from "@likeminds.community/feed-rn-core";
import { Alert, Platform, Share } from "react-native";
import { useAppSelector } from "@likeminds.community/feed-rn-core/store/store";
import STYLES from "@likeminds.community/feed-rn-core/constants/Styles";
import { useNavigation } from "@react-navigation/native";

const Feed = () => {
  const {
    postLikeHandler,
    savePostHandler,
    handleEditPost,
    handlePinPost,
    onTapCommentCount,
    onTapLikeCount,
    handleDeletePost,
    handleReportPost,
    onOverlayMenuClick,
  } = usePostListContext();
  const {
    newPostButtonClick,
    onTapNotificationBell,
    addPollOption,
    setSelectedPollOptions,
    submitPoll,
  } = useUniversalFeedContext();
  const mappedTopics = useAppSelector((state) => state.feed.mappedTopics);
  const navigation = useNavigation();

  const customPostLike = (postId) => {
    console.log("before like ");
    postLikeHandler(postId);
    console.log("after like", postId);
  };
  const customPostSave = (postId, saved) => {
    console.log("before save");
    savePostHandler(postId, saved);
    console.log("after save", postId, saved);
  };
  const customHandleEdit = (postId, post) => {
    console.log("before edit select", post);
    handleEditPost(postId, post);
    console.log("after edit select", postId);
  };
  const customHandlePin = (postId, pinned) => {
    console.log("before pin select");
    handlePinPost(postId, pinned);
    console.log("after pin select", postId, pinned);
  };

  const universaleFeedStyles = {
    newPostButtonStyle: {
      backgroundColor: "red",
      border: 1,
    },
    screenHeader: {
      heading: "LikeMinds",
      subHeading: "Welcome to LM Documentation",
      onBackPress: () => navigation.goBack(),
    },
  };

  // universal feed screen customisation
  if (universaleFeedStyles) {
    STYLES.setUniversalFeedStyles(universaleFeedStyles);
  }

  return (
    <UniversalFeed
      postLikeHandlerProp={(id) => customPostLike(id)}
      savePostHandlerProp={(id, saved) => customPostSave(id, saved)}
      selectEditPostProp={(id, post) => customHandleEdit(id, post)}
      selectPinPostProp={(id, pinned) => customHandlePin(id, pinned)}
      isHeadingEnabled={true}
      isTopResponse={true}
    >
      <LMUniversalFeedHeader />
      <LMFilterTopics />
      <LMPostUploadIndicator />
      <PostsList items={mappedTopics} />
      <LMCreatePostButton />
    </UniversalFeed>
  );
};

export default Feed;
```

</TabItem>
<TabItem value="FeedScreenWrapper" label="FeedScreenWrapper">

```tsx
import FeedScreen from "<<path_to_FeedScreen.tsx>>";
import {
  PostListContextProvider,
  UniversalFeedContextProvider,
} from "@likeminds.community/feed-rn-core";

const FeedWrapper = ({ navigation, route }) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostListContextProvider navigation={navigation} route={route}>
        <FeedScreen />
      </PostListContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default FeedWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `FeedWrapper` as a Stack screen in your `NavigationContainer`.

```tsx
import {
  UNIVERSAL_FEED,
  LMOverlayProvider,
} from "@likeminds.community/feed-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { FeedWrapper } from "<<path_to_CustomisedUniversalFeed.tsx>>";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: true }}>
          <Stack.Screen name={UNIVERSAL_FEED} component={FeedWrapper} />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
