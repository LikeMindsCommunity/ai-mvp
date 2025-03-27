---
sidebar_position: 4
title: Posts List View
slug: /react-native/core/components/universal-feed/lm-post-list
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `PostsList` component is responsible for rendering a list of posts in a feed. It handles the display of individual post items and provides support for infinite scrolling, ensuring smooth loading of new content as the user navigates through the feed. The component integrates with post content, media, header, and footer, offering extensive customization options for styling and functionality.

<img
src={require('../../../../../static/img/reactNative/postsList.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## UI Components

- [LMFeedLoader](../Fundamentals/LMFeedLoader.md)

## Data Variables

- `feedData`: Stores the feed data conforming to [`LMPostViewData[]`](../../Models/LMPostViewDataModel.md).

## Callbacks

- `postLikeHandlerProp`: Handles the action when a post is liked.
- `savePostHandlerProp`: Handles the action when a post is saved or unsaved.
- `selectPinPostProp`: Handles the action when a post is pinned or unpinned.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/context/universalFeedCallbacksContext.tsx).

## Customization with Props

| Property               | Type              | Description                                                                                        |
| ---------------------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| `items`                | `Array`           | Array of mapped topics, typically containing topic details like `id` and `name`.                   |
| `lmPostCustomFooter`   | `React.Component` | Custom footer component displayed beneath each post, often used for features like Q&A or comments. |
| `customWidgetPostView` | `React.Component` | Custom view for widget-based posts, allowing specific widgets or layouts per post.                 |

Each of these props offers flexibility for building more complex and dynamic feed layouts with tailored elements.

## Customisation with Styles

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `postListStyle` in `STYLES`.

| Property      | Type                                                                                 | Description                                                             |
| ------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `header`      | [`LMFeedHeaderProps`](../../Components/Post/LMFeedPostHeader.md#customisation)       | Customization for the header of the post.                               |
| `footer`      | [`LMFeedFooterProps`](../../Components/Post/LMFeedPostFooter.md#customisation)       | Customization for the footer of the post.                               |
| `postContent` | [`LMFeedPostContentProps`](../../Components/Post/LMFeedPostContent.md#customisation) | Customization for the post content area.                                |
| `media`       | [`LMFeedMediaProps`](../../Components/Post/LMFeedPostMedia.md#customisation)         | Customization for media like images, videos, and documents in the post. |
| `noPostView`  | `ViewStyle`                                                                          | Styling for the view when no post is available.                         |
| `noPostText`  | `TextStyle`                                                                          | Styling for the text displayed when no post is available.               |
| `listStyle`   | `ViewStyle`                                                                          | Styling for the overall list view.                                      |

## Usage Example

:::info
The `PostsList` screen can be used by wrapping it inside the `UniversalFeed` screen, and the selected topcis can be passed as a prop to this screen, so that filtered posts are displayed. The customised callbacks for `PostsList` screen are passed to `UniversalFeed` screen and are internally accessed by `PostsList` screen.
:::

### Step 1: Create Custom Screen and Wrapper

- Create a `FeedScreenWrapper` file which will wrap the `FeedScreen` within the `UniversalFeedContextProvider` and `PostListContextProvider` so that the callbacks becomes accessible inside of the `FeedScreen`.
- Create `postListStyles` for customisation and call the `setPostListStyles` to set the customisation.

<Tabs>
<TabItem value="FeedScreen" label="FeedScreen">

```tsx
import { PostsList, UniversalFeed, STYLES } from "@likeminds.community/feed-rn-core";
import { useAppSelector } from "@likeminds.community/feed-rn-core/store/store";

// here, mappedTopics are the selected topics according to which the posts will be shown
const mappedTopics = useAppSelector((state) => state.feed.mappedTopics);

export const SamplePostList = () => {
  const { postLikeHandler, savePostHandler, handleEditPost } =
    usePostListContext();

  // customised postLikeHandler method
  const customPostLike = (postId) => {
    console.log("before like ");
    postLikeHandler(postId);
    console.log("after like", postId);
  };
  // customised savePostHandler method
  const customPostSave = (postId, saved) => {
    console.log("before save");
    savePostHandler(postId, saved);
    console.log("after save", postId, saved);
  };
  // customised handlePinPost method
  const customHandlePin = (postId, pinned) => {
    console.log("before pin select");
    handlePinPost(postId, pinned);
    console.log("after pin select", postId, pinned);
  };

  const postListStyles = {
    header: {
      profilePicture: {
        size: 25,
        fallbackTextBoxStyle: {
          backgroundColor: "red",
        },
      },
    },
    showMemberStateLabel: true,
  };

  // universal feed screen customisation
  if (postListStyles) {
    STYLES.setPostListStyles(postListStyles);
  }

  return (
    <UniversalFeed
      postLikeHandlerProp={(id) => customPostLike(id)}
      savePostHandlerProp={(id, saved) => customPostSave(id, saved)}
      selectPinPostProp={(id, pinned) => customHandlePin(id, pinned)}
    >
      <PostsList items={mappedTopics} />
    </UniversalFeed>
  );
};
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

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
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