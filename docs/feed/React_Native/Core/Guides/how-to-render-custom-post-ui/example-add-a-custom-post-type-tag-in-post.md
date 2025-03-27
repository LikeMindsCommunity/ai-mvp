---
sidebar_position: 2
title: How to add a custom Post Type Tag in a Post?
slug: /react-native/core/guide/how-to-add-a-custom-post-type-tag-in-post
---

## Overview

In this guide we will walkthrough how we can create a Universal Feed Screen that displays a custom made Post UI giving you the freedom and choice of creating unique designs that suits your needs and adding more functionality

## Steps

### Step 1: Create your Custom Post component

```jsx
import React from "react"
import {
  useLMPostContext,
  LMPostHeader.
  Layout,
  LMPostHeading,
  LMPostContent,
  LINK_ATTACHMENT_TYPE,
  LMPostTopResponse,
  LMPostQnAFeedFooter
} from "@likeminds.community/feed-rn-core"
const CustomPostComponent = React.memo(() => {
  // Get all the core methods and state required to make your custom UI functional from the Likminds Feed SDK
  const { post, footerProps, headerProps } = useLMPostContext();

  // Tags to be displayed in a post
  const tags = [
    {
      title: "question",
      id: 1,
    },
    {
      title: "tip",
      id: 2,
    },
  ];

  return (
    <View style={{ width: "100%", paddingTop: 10, marginBottom: 10 }}>
      <LMPostHeader />

      {/* custom tags section */}
      <View
        style={{ flexDirection: "row", gap: 5, marginLeft: 10, marginTop: 5 }}
      >
        {tags.map((item) => (
          <View
            style={{
              paddingVertical: 3,
              paddingHorizontal: 10,
              borderRadius: 10,
              backgroundColor: STYLES.$COLORS.PRIMARY,
            }}
          >
            <Text
              style={[
                {
                  fontSize: Layout.normalize(14),
                  color: STYLES.$COLORS.WHITE,
                  paddingVertical: Layout.normalize(2),
                  paddingHorizontal: Layout.normalize(8),
                  fontFamily: STYLES.$FONT_TYPES.LIGHT,
                },
              ]}
            >
              {item?.title}
            </Text>
          </View>
        ))}
      </View>

      <LMPostHeading />

      {(post?.text ||
        post?.attachments?.find(
          (item) => item?.attachmentType === LINK_ATTACHMENT_TYPE
        )?.attachmentType === LINK_ATTACHMENT_TYPE) && <LMPostContent />}

      {post?.attachments && post?.attachments.length > 0 && <LMPostMedia />}

      <LMPostTopResponse />

      <LMPostQnAFeedFooter />
    </View>
  );
});
```

Here are the components that Likeminds Feed SDK uses to display a post

| Component             | Description                                                |
| --------------------- | ---------------------------------------------------------- |
| `LMPostHeader`        | Shows the post’s metadata, like author name and timestamp. |
| `LMPostHeading`       | Displays the title or heading of the post.                 |
| `LMPostContent`       | Displays the main content of a post (Textual Description). |
| `LMPostMedia`         | Handles media elements such as images, videos, documents.  |
| `LMPostFooter`        | Renders actions like likes, comments, and share options.   |
| `LMPostQnAFeedFooter` | Provides Q&A-specific actions such as voting and answers.  |
| `LMPostTopResponse`   | Renders the response/comment with most upvotes.            |

### Step 2: Create a Custom Universal Feed Component

```jsx
import {
  UniversalFeed,
  LMFilterTopics,
  LMPostUploadIndicator,
  PostsList,
  LMCreatePostButton,
} from "@likeminds.community/feed-rn-core";
import { useAppSelector } from "@likeminds.community/feed-rn-core";

const CustomUniversalFeed = () => {
  const mappedTopics = useAppSelector((state: any) => state.feed.mappedTopics);
  return (
    <View style={{ flex: 1, backgroundColor: "black" }}>
      <UniversalFeed isHeadingEnabled={true} isTopResponse={true}>
        <LMUniversalFeedHeader />
        <LMFilterTopics />
        <LMPostUploadIndicator />
        <PostsList
          items={mappedTopics}
          customWidgetPostView={<CustomPostComponent />} // Pass your custom post component here
        />
        <LMCreatePostButton customText="ASK QUESTION" />
      </UniversalFeed>
    </View>
  );
};
```

### Step 3: Create a Custom Post Detail Screen Component

```jsx
import {
  UniversalFeedContextProvider,
  PostDetailContextProvider,
  PostDetail,
} from "@likeminds.community/feed-rn-core";

const CustomPostDetailScreen = ({ navigation, route }: any) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostDetailContextProvider navigation={navigation} route={route}>
        {/* @ts-ignore */}
        <PostDetail
          customWidgetPostView={<CustomPostComponent />} // pass your custom component here
        />
      </PostDetailContextProvider>
    </UniversalFeedContextProvider>
  );
};
```

### Step 4: Wrap the `<CustomUniversalFeed/>` component with the imported wrappers

```jsx
import {
  UniversalFeedContextProvider
  PostListContextProvider
} from "@likeminds.community/feed-rn-core";
const CustomFeedScreen = ({ navigation, route }) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostListContextProvider navigation={navigation} route={route}>
        <CustomUniversalFeed />
      </PostListContextProvider>
    </UniversalFeedContextProvider>
  );
};
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
      {/*...other screens */}
      <Stack.Screen
        name={UNIVERSAL_FEED_SCREEN}
        component={<CustomFeedScreen />}
      />
      <Stack.Screen name={POST_DETAIL} component={<CustomPostDetailScreen />} />
    </Stack.Navigator>
  </NavigationContainer>
</LMOverlayProvider>
```

### Result

<p align="center">
    <img
    src="/img/react-native-post-ui-custom-widget.png"
    alt="LMFeedLikeListScreen"
    width="180"
    />
</p>
