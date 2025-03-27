---
sidebar_position: 8
title: How to show feed and create a post with followed topics?
slug: /react-native/core/guide/how-to-show-feed-and-create-a-post-with-followed-topics
---

## Overview

This guide explains how to display a feed filtered by followed topics and how to create a post that includes only topics the user is following. This functionality enhances user engagement by tailoring content and post creation options to topics of interest.

## Steps

### Step 1: Create your custom Universal Feed component

```jsx
import React, { useEffect, useState } from 'react';
import { View } from "react-native";
import {
    LMFilterTopics,
    LMPostUploadIndicator,
    LMUniversalFeedHeader,
    PostsList,
    UniversalFeed,
    LMCreatePostButton,
    LMPostQnAFeedFooter
    usePostListContext,
    useUniversalFeedContext,
} from '@likeminds.community/feed-rn-core';

function CustomUniversalFeed() {
  return (
    <View style={{flex: 1, backgroundColor: 'black'}}>
      <UniversalFeed>
        <LMUniversalFeedHeader />
        <LMPostUploadIndicator />
        <PostsList />
        <LMCreatePostButton />
      </UniversalFeed>
    </View>
  );
}
```

### Step 2: Wrap the `<CustomUniversalFeed/>` with context providers

```jsx
import {
  UniversalFeedContextProvider,
  PostListContextProvider,
} from "@likeminds.community/feed-rn-core";
import { Client } from '@likeminds.community/feed-rn-core/client';
import {GetUserTopicsRequest} from '@likeminds.community/feed-rn';

function CustomUniversalFeedScreen({ navigation, route }) {
  const [selectedTopics, setSelectedTopics] = useState([]);
  // use Client class imported from the LikeMinds Feed SDK to make an API request to get user followed topics
  const getUserFollowedTopics = async () => {
    const { data } = await Client?.myClient?.getUserTopics(
      GetUserTopicsRequest.builder()
        .setUuids(["<UUID_OF_USER>"])
        .build(),
    );
    return data.userTopics["<UUID_OF_USER>"]; // returns an array of Topics IDs followed by the given user
  };

  useEffect(async () => {
    const response = await getUserFollowedTopics();
    if (response) {
      setSelectedTopics(response);
    }
  }, []);
  return (
    <>
      {selectedTopics.length > 0 ? (
        <UniversalFeedContextProvider
          navigation={navigation}
          route={route}
          predefinedTopics={selectedTopics}
        >
          <PostListContextProvider navigation={navigation} route={route}>
            <Feed />
          </PostListContextProvider>
        </UniversalFeedContextProvider>
      ) : null}
    </>
  );
}
```

### Step 3: Create a Custom Create Post component

`<CreatePost>` acts as a context provider to its childen allowing for customization of inner child components, in place of prebuilt componentes imported from the Likeminds Feed SDk custom component can also be created and used instead.
As all child components of `<CreatePost>` get access to all the methods and state made available through `useCreatePostContext` hook.

```jsx
import {
  CreatePost,
  LMCreatePostHeader,
  LMCreatePostUIRender,
  LMUserProfileSection,
  LMCreatePostTopics,
  LMCreatePostHeading,
  LMCreatePostTextInput,
  LMCreatePostUserTagging,
  LMCreatePostMedia,
  LMCreatePostUIRender,
  LMCreatePostAttachmentSelection,
  LMCreatePostAnonymousCheckbox,
} from "@likeminds.community/feed-rn-core";
import Client from "@likeminds.communtity/feed-rn-core/client";
import {GetUserTopicsRequest} from '@likeminds.community/feed-rn';

const CustomCreatePost = ({ isHeadingEnabled }) => {
  const { onPostClick } = useCreatePostContext();

  // use Client class imported from the LikeMinds Feed SDK to make an API request to get user followed topics
  const getUserFollowedTopics = async () => {
    const { data } = await Client?.myClient?.getUserTopics(
      GetUserTopicsRequest.builder()
        .setUuids(["<UUID_OF_USER>"])
        .build(),
    );
    return data.userTopics["<UUID_OF_USER>"]; // returns an array of Topics IDs followed by the given user
  };

  async function customOnPostClick(
    allMedia: Array<LMAttachmentViewData>,
    linkData: Array<LMAttachmentViewData>,
    content: string,
    heading: string,
    topics: string[],
    poll: any,
    isAnonymous: boolean
  ) {
    const userFollowedTopics = await getUserFollowedTopics();

    onPostClick(
      allMedia,
      linkData,
      content,
      heading,
      userFollowedTopics, // pass default topics/user followed topics
      poll,
      isAnonymous
    );
  }

  return (
    /* @ts-ignore */
    <CreatePost onPostClickProp={customOnPostClick}>
      {/* screen header section*/}
      <LMCreatePostHeader />

      {/* handles the UI to be rendered for edit post and create post */}
      <LMCreatePostUIRender>
        {/* user profile section */}
        <LMUserProfileSection />

        {/* Anonymous post checkbox */}
        <LMCreatePostAnonymousCheckbox />

        {/* post topics section */}
        <LMCreatePostTopics />

        {/* post heading section */}
        <LMCreatePostHeading />

        {/* text input field */}
        <LMCreatePostTextInput />

        {/* users tagging list */}
        <LMCreatePostUserTagging />

        {/* selected media section */}
        <LMCreatePostMedia />

        {/* selection options section */}
        <LMCreatePostAttachmentSelection />
      </LMCreatePostUIRender>
    </CreatePost>
  );
};
```

### Step 4: Wrap the `<CustomCreatePost/>` with context providers

```jsx
function CustomCreatePostScreen({ navigation, route }) {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <CreatePostContextProvider navigation={navigation} route={route}>
        <CustomCreatePost />
      </CreatePostContextProvider>
    </UniversalFeedContextProvider>
  );
}
```

### Step 5: Used the created custom screens on your stack navigator

```jsx
<LMOverlayProvider
  myClient={myClient}
  apiKey={apiKey}
  userName={userName}
  userUniqueId={userUniqueID}
  lmFeedInterface={lmFeedInterface}
>
  <NavigationContainer ref={navigationRef} independent={true} {...props}>
    <Stack.Navigator>
      {/* ...other screens */}
      <Stack.Screen
        name={UNIVERSAL_FEED_SCREEN}
        component={<CustomUniversalFeedScreen />}
      />
      <Stack.Screen name={CREATE_POST} component={<CustomCreatePostScreen />} />
    </Stack.Navigator>
  </NavigationContainer>
</LMOverlayProvider>
```
