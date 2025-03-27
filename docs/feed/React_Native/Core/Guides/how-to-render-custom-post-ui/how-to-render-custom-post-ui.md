---
sidebar_position: 1
title: How to render Custom Post UI?
slug: /react-native/core/guide/how-to-render-custom-post-ui
---

## Overview

The LikeMinds Feed SDK allows allows developers to customize the appearance and layout of posts in the app to align with specific design needs or branding guidelines. By implementing custom UI components, you can modify elements such as the header, content, attachments, and actions to create a unique user experience.

In this guide, we will walkthrough how to create a Universal Feed Screen and Post Detail Screen that displays a custom Post UI.

## Steps

### Step 1: Create your own Custom Post Component i.e `<CustomPostComponent/>`

```jsx
const CustomPostComponent = () => {
  <></>;
};
```

### Step 2: Create a `<CustomFeed/>` or `<CustomPostDetail/>` Component

1.  Display your Custom Post Component on the Feed screen:

```jsx
import {
    LMCreatePostButton,
    LMFilterTopics,
    LMPostUploadIndicator,
    LMUniversalFeedHeader,
    PostsList,
    UniversalFeed,
} from "@likeminds.community/feed-rn-core";
import { useAppSelector } from "@likeminds.community/feed-rn-core/store"
import { View } from "react-native"

const CustomFeed = () => {
 const mappedTopics = useAppSelector((state: any) => state.feed.mappedTopics);
    return (
        {/* @ts-ignore */}
        <View style={{ flex: 1 }}>
            <UniversalFeed isHeadingEnabled={true} isTopResponse={true}>
                <LMUniversalFeedHeader />
                <LMFilterTopics />
                <LMPostUploadIndicator />
                <PostsList
                items={mappedTopics}
                customWidgetPostView={<CustomPostComponent />}
                />
                <LMCreatePostButton customText={CUSTOM_TEXT} />
            </UniversalFeed>
        </View>
    );
};
```

2.  Display your Custom Post Component on the Post Detail screen:

```jsx
import { PostDetail } from "@likeminds.community/feed-rn-core";

const CustomPostDetail = ({ navigation }) => {
    return (
        {/* @ts-ignore */}
        <PostDetail
        navigation={navigation}
        route={route}
        customWidgetPostView={<CustomPostComponent />}
        />
    );
};
```

### Step 3: Wrap your `<CustomFeed/>` or `<CustomPostDetail/>` Component with the wrappers imported from the LM Feed SDK

1.  If you want to show your `<CustomPostComponent/>` on the Feed screen:

```jsx
import {
  UniversalFeedContextProvider,
  PostListContextProvider,
} from "@likeminds.community/feed-rn-core";
const CustomFeedScreen = ({ navigation, route }) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostListContextProvider navigation={navigation} route={route}>
        <CustomFeed />
      </PostListContextProvider>
    </UniversalFeedContextProvider>
  );
};
```

2.  If you want to show your `<CustomPostComponent/>` on the Post Detail Screen:

```jsx
import {
  UniversalFeedContextProvider,
  PostDetailContextProvider,
} from "@likeminds.community/feed-rn-core";
const CustomPostDetailScreen = ({ navigation, route }: any) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostDetailContextProvider navigation={navigation} route={route}>
        <CustomPostDetail navigation={navigation} />
      </PostDetailContextProvider>
    </UniversalFeedContextProvider>
  );
};
```

### Step 4: Add the Wrapped Components to the Stack Navigator

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
      <Stack.Screen name={UNIVERSAL_FEED_SCREEN} component={<CustomFeed />} />
      <Stack.Screen name={POST_DETAIL} component={<CustomPostDetailScreen />} />
    </Stack.Navigator>
  </NavigationContainer>
</LMOverlayProvider>
```
