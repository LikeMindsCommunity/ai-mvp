---
sidebar_position: 9
title: How to hide a topic in post view and during post creation?
slug: /react-native/core/guide/how-to-hide-a-topic-in-post-view-and-during-post-creation
---

## Overview

The LikeMinds Feed SDK allows developers to control the visibility of specific topics in the post view and the post creation screen. This is useful for managing sensitive topics, reducing clutter, or customizing the user experience based on specific criteria.

In this guide, we will walk you through creating a Universal Feed Screen and Post Detail Screen with hidden topic views, as well as disabling topic selection in the Create Post Screen during post creation.

## Steps

### Step 1: Create a Custom Universal Feed component and pass `hideTopicsView` as true

```jsx
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
import { useAppSelector } from "@likeminds.community/feed-rn-core/store"

function CustomUniversalFeed() {
    const mappedTopics = useAppSelector((state: any) => state.feed.mappedTopics);
    return (
        <View style={{ flex: 1, backgroundColor: "black" }}>
            <UniversalFeed
            hideTopicsView={true} // Hide topics view for all posts visible in the universal feed
            >
                <LMUniversalFeedHeader />
                <LMPostUploadIndicator />
                <PostsList
                items={mappedTopics}
                />
                <LMCreatePostButton />
            </UniversalFeed>
        </View>
    )
}
```

### Step 2: Create a Custom Post Detail Screen and pass `hideTopicsView` as true

```jsx
import {
  UniversalFeedContextProvider,
  PostDetailContextProvider,
  PostDetail,
} from "@likeminds.community/feed-rn-core";

const PostDetailScreen = ({ navigation, route }: any) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostDetailContextProvider navigation={navigation} route={route}>
        {/* @ts-ignore */}
        <PostDetail
          hideTopicsView={true} // hides topics view in the post detail screen
        />
      </PostDetailContextProvider>
    </UniversalFeedContextProvider>
  );
};
```

### Step 3: Wrap `<CustomUniversalFeed/>` with context providers as shown

```jsx
import {
    UniversalFeedContextProvider,
    PostListContextProvider
} from "@likeminds.community/feed-rn-core"
function CustomUniversalFeedScreen = ({navigation, route}) {
    return(
        <UniversalFeedContextProvider navigation={navigation} route={route}>
            <PostListContextProvider navigation={navigation} route={route}>
                <CustomUniversalFeed />
            </PostListContextProvider>
        </UniversalFeedContextProvider>
    )
}
```

### Step 4: Create a custom Post Create component and pass your customisations as props

To disable topic creation while creating a post, follow either of the steps

1. Pass `hideTopicsViewCreate`, `hideTopicsViewEdit` props as true.
2. Omit using the `<LMCreatePostTopics />` Component as a child inside `<CreatePost />`

```jsx
import {
  CreatePost,
  LMCreatePostHeader,
  LMCreatePostUIRender,
  LMUserProfileSection,
  LMCreatePostHeading,
  LMCreatePostTextInput,
  LMCreatePostUserTagging,
  LMCreatePostMedia,
  LMCreatePostUIRender,
  LMCreatePostAttachmentSelection,
  LMCreatePostAnonymousCheckbox,
} from "@likeminds.community/feed-rn-core";

const CustomPostCreate = () => {
  return (
    /* @ts-ignore */
    <CreatePost
      hideTopicsViewCreate={true} // hides topics selection when creating a post
      hideTopicsViewEdit={true} // hides topics selection while editing a post
    >
      {/* screen header section*/}
      <LMCreatePostHeader />

      {/* handles the UI to be rendered for edit post and create post */}
      <LMCreatePostUIRender>
        {/* user profile section */}
        <LMUserProfileSection />

        {/* Anonymous post checkbox*/}
        <LMCreatePostAnonymousCheckbox />

        {/* Instead of passing props, we can also omit using the <LMCreatePostTopics/> component */}

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

### Step 5: Wrap the `<CustomPostCreate/>` with context providers imported from Likeminds Feed SDK

```jsx
import {
  UniversalFeedContextProvider,
  CreatePostContextProvider,
} from "@likeminds.communtiy/feed-rn-core";
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

### Step 6: Used the created custom screens on your stack navigator

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
      {/*
            ...other screens
            */}
      <Stack.Screen
        name={UNIVERSAL_FEED_SCREEN}
        component={<CustomUniversalFeedScreen />}
      />
      <Stack.Screen name={CREATE_POST} component={<CustomCreatePostScreen />} />
    </Stack.Navigator>
  </NavigationContainer>
</LMOverlayProvider>
```
