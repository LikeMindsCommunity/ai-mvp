---
sidebar_position: 1
title: Search Screen
slug: /react-native/core/screens/search-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

`SearchFeed` displays a feed screen with an input box and a list of posts that are fetched based on the given search query.

<img
src={require('../../../../static/img/reactNative/search-feed.webp').default}
alt="LMSearchFeedScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Callbacks

Below are the callback props available for `SearchFeed`, allowing you to handle interactions within the feed.

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
- `onSharePostClicked`: Handles post sharing, receiving the post `id`.
- `onSubmitButtonClicked`: Custom action for poll submission.
- `onAddPollOptionsClicked`: Custom action for adding poll options.
- `onPollOptionClicked`: Custom action when a poll option is clicked.
- `onBackArrowPressProp`: Custom action when back arrow is pressed.
- `onCrossPressProp`: Custom action when clear input text icon is pressed.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/context/universalFeedCallbacksContext.tsx).

## Customisation with Props

| Property               | Type      | Description                                              | Required           |
| ---------------------- | --------- | -------------------------------------------------------- | ------------------ |
| `isHeadingEnabled`     | `boolean` | Enables or disables the heading display.                 | :heavy_check_mark: |
| `isTopResponse`        | `boolean` | Shows the top response if set to true.                   |                    |
| `hideTopicsView`       | `boolean` | Hides the topics view on the feed screen if set to true. |                    |
| `lmPostCustomFooter`   | `JSX`     | Custom Footer Component.                                 |                    |
| `customWidgetPostView` | `JSX`     | Custom Post Component to be displayed in post list       |                    |

## Customization with Styles

| Property                | Type                                                      | Description                              |
| ----------------------- | --------------------------------------------------------- | ---------------------------------------- |
| `placeholderText`       | `string`                                                  | Text to display when the input is empty. |
| `placeholderTextColor`  | `string`                                                  | Color of the placeholder text.           |
| `searchQueryTextStyle`  | `TextStyle`                                               | Style for the search query text.         |
| `inputBoxStyle`         | `ViewStyle`                                               | Style for the input box container.       |
| `crossIconStyle`        | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Style for the cross (clear) icon.        |
| `backIconStyle`         | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Style for the back navigation icon.      |
| `listEmptyStyle`        | `object`                                                  | Styles for the empty list state.         |
| ├ `listEmptyTextStyle`  | `TextStyle`                                               | Style for the empty list text.           |
| └ `listEmptyImageStyle` | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Style for the empty list image/icon.     |

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `CustomSearchFeed` file which will wrap the `SearchFeed` within the `SearchedPostListContextProvider` so that the callbacks becomes accessible inside of the `SearchFeed`.
- Create `SearchFeedStyles` for customisation and call the `setSearchFeedStyles` to set the customisation.

<Tabs>
<TabItem value="CustomSearchFeed" label="CustomSearchFeed">

```tsx
import {
  SearchFeed,
  SearchedPostListContextProvider,
  useSearchedPostListContext,
} from "@likeminds.community/feed-rn-core";
import STYLES from "@likeminds.community/feed-rn-core/constants/Styles";

const CustomSearchFeed = ({ navigation, route }) => {
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
  } = useSearchedPostListContext();

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

  const searchFeedStyles = {
    crossIconStyle: {
      height: 20,
      width: 20,
      color: "blue",
      assetPath: require("./gallery_icon3x.png"),
    },
    backIconStyle: {
      color: "red",
      assetPath: require("./gallery_icon3x.png"),
    },
    placeholderText: "PLACEHOLDER...",
    placeholderTextColor: "grey",
    searchQueryTextStyle: {
      color: "red",
    },
  };

  STYLES.setSearchFeedStyles(searchFeedStyles);

  return (
    <SearchFeed
      postLikeHandlerProp={(id) => customPostLike(id)}
      savePostHandlerProp={(id, saved) => customPostSave(id, saved)}
      selectEditPostProp={(id, post) => customHandleEdit(id, post)}
      selectPinPostProp={(id, pinned) => customHandlePin(id, pinned)}
      isHeadingEnabled={true}
      isTopResponse={true}
      navigation={navigation}
      route={route}
    />
  );
};

export default CustomSearchFeed;
```

</TabItem>
<TabItem value="SearchFeedScreenWrapper" label="SearchFeedScreenWrapper">

```tsx
import CustomSearchFeed from "<<path_to_CustomSearchFeed.tsx>>";
import {
  PostListContextProvider,
  UniversalFeedContextProvider,
  SearchType
} from "@likeminds.community/feed-rn-core";

const SearchFeedScreenWrapper = ({ navigation, route }) => {
  return (
    <SearchedPostListContextProvider
      searchType={<"SEARCH_TYPE">} // Pass a value present in the SearchType Enum
      navigation={navigation}
      route={route}
    >
        <CustomSearchFeed navigation={navigation} route={route} />
    </UniversalFeedContextProvider>
  );
};

export default SearchFeedScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `SearchFeedScreenWrapper` as a Stack screen in your `NavigationContainer`.

```tsx
import {
  SEARCH_SCREEN,
  LMOverlayProvider,
} from "@likeminds.community/feed-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import SearchFeedScreenWrapper from "<<path_to_SearchFeedScreenWrapper.tsx>>";

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
          <Stack.Screen
            name={SEARCH_SCREEN}
            component={SearchFeedScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
