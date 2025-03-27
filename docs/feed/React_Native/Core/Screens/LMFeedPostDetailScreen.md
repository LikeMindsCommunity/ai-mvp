---
sidebar_position: 3
title: Post Detail
slug: /react-native/core/screens/post-details-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

LikeMindsFeed SDK offers various Post Detail Screen implementations to cater to different use cases. These screens are responsible for displaying detailed information about a post, including comments and replies, with each variant optimized for specific content types or interactions.

In the Post Detail screen, the LikeMinds Feed SDK reuses the components from the Post List screen. While these cells share a similar UI, separate classes have been created for each to allow customization and extensibility.

<img
src={require('../../../../static/img/iOS/screens/postDetail.webp').default}
alt="LMFeedPostDetailScreen"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## UI Components

- [LMFeedHeader](../Components/Fundamentals/LMFeedHeader.md)
- [LMFeedPostHeader](../Components/Post/LMFeedPostHeader.md)
- [LMFeedPostFooter](../Components/Post/LMFeedPostFooter.md)
- [LMFeedPostContent](../Components/Post/LMFeedPostContent.md)
- [LMFeedCarousel](../Components/Media/LMFeedCarousel.md)
- [LMFeedDocument](../Components/Media/LMFeedDocument.md)
- [LMFeedImage](../Components/Media/LMFeedImage.md)
- [LMFeedLinkPreview](../Components/Media/LMFeedLinkPreview.md)
- [LMFeedVideo](../Components/Media/LMFeedVideo.md)
- [LMFeedCommentItem](../Components/LMFeedCommentItem.md)
- [LMFeedLoader](../Components/Fundamentals/LMFeedLoader.md)

## Data Variables

- `postData`: Stores the post data conforming to [`LMPostViewData`](../Models/LMPostViewDataModel.md).
- `commentsData`: An array of [`LMCommentViewData`](../Models/LMCommentViewData.md) representing the comments and replies data.
- `isCommentingEnabled`: A Boolean indicating whether commenting is enabled for the current user.

## Callbacks

- `getCommentsRepliesProp`: Fetches the replies for a given comment by post ID and comment ID, invoking a callback with the response.
- `addNewCommentProp`: Adds a new comment to the specified post.
- `addNewReplyProp`: Adds a new reply to a specific comment within a post.

For information about more callbacks, click [here](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/context/postDetailCallbacksContext.tsx).

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `postDetailStyle` in `STYLES`.

| Property                       | Type                                              | Description                                                       |
| ------------------------------ | ------------------------------------------------- | ----------------------------------------------------------------- |
| `screenHeader`                 | [`LMHeaderProps`](../Components/LMFeedHeader.md)  | Customization for the screen header.                              |
| `commentItemStyle`             | [`CommentItemStyle`](#commentitemstyle)           | Customization for the individual comment item.                    |
| `commentCountHeadingText`      | `TextStyle`                                       | Styling for the comment count heading text.                       |
| `noCommentViewStyle`           | `ViewStyle`                                       | Styling for the view shown when there are no comments.            |
| `noCommentHeadingTextStyle`    | `TextStyle`                                       | Styling for the heading text shown when there are no comments.    |
| `noCommentSubHeadingTextStyle` | `TextStyle`                                       | Styling for the subheading text shown when there are no comments. |
| `replyingViewStyle`            | [`ReplyingViewStyle`](#replyingviewstyle)         | Customization for the reply view.                                 |
| `userTaggingListStyle`         | [`UserTaggingListStyle`](#usertaggingliststyle)   | Customization for the user tagging list.                          |
| `commentTextInputStyle`        | [`CommentTextInputStyle`](#commenttextinputstyle) | Customization for the comment input text field.                   |

### CommentItemStyle

| Property                | Type                                                      | Description                                |
| ----------------------- | --------------------------------------------------------- | ------------------------------------------ |
| `onTapViewMore`         | `Function`                                                | Callback for when "View More" is tapped.   |
| `commentUserNameStyle`  | `TextStyle`                                               | Styling for the comment username.          |
| `commentContentProps`   | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Props for the comment content text.        |
| `replyTextProps`        | [`ReplyTextProps`](#replytextprops)                       | Customization for the reply text and icon. |
| `repliesCountTextStyle` | `TextStyle`                                               | Styling for the replies count text.        |
| `timeStampStyle`        | `TextStyle`                                               | Styling for the timestamp.                 |
| `viewMoreRepliesProps`  | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Props for "View More Replies" text.        |
| `onTapReplies`          | `Function`                                                | Callback for tapping on replies.           |

### ReplyTextProps

| Property      | Type                                                      | Description                                   |
| ------------- | --------------------------------------------------------- | --------------------------------------------- |
| `text`        | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Customization for the reply button text.      |
| `icon`        | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Customization for the reply button icon.      |
| `onTap`       | `Function`                                                | Callback for when the reply button is tapped. |
| `placement`   | `String`                                                  | Placement of the icon relative to the text.   |
| `buttonStyle` | `ViewStyle`                                               | Styling for the reply button.                 |
| `isClickable` | `Boolean`                                                 | Whether the reply button is clickable.        |

### ReplyingViewStyle

| Property          | Type                                                      | Description                              |
| ----------------- | --------------------------------------------------------- | ---------------------------------------- |
| `replyingView`    | `ViewStyle`                                               | Styling for the replying view container. |
| `replyingText`    | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Customization for the replying text.     |
| `cancelReplyIcon` | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Customization for the cancel reply icon. |

### UserTaggingListStyle

| Property           | Type        | Description                               |
| ------------------ | ----------- | ----------------------------------------- |
| `taggingListView`  | `ViewStyle` | Styling for the tagging list view.        |
| `userTagView`      | `ViewStyle` | Styling for the individual user tag view. |
| `userTagNameStyle` | `TextStyle` | Styling for the user tag name.            |

### CommentTextInputStyle

| Property               | Type                                | Description                                                      |
| ---------------------- | ----------------------------------- | ---------------------------------------------------------------- |
| `inputTextStyle`       | `TextStyle`                         | Styling for the input text field.                                |
| `placeholderText`      | `String`                            | Placeholder text for the input field.                            |
| `placeholderTextColor` | `String`                            | Color for the placeholder text.                                  |
| `rightIcon`            | [`RightIconProps`](#righticonprops) | Customization for the icon on the right side of the input field. |
| `textValueStyle`       | `TextStyle`                         | Styling for the text value in the input field.                   |
| `mentionTextStyle`     | `TextStyle`                         | Styling for the mentioned users' text.                           |
| `multilineField`       | `Boolean`                           | Whether the input field supports multiple lines.                 |

### RightIconProps

| Property      | Type                                                      | Description                                 |
| ------------- | --------------------------------------------------------- | ------------------------------------------- |
| `text`        | [`LMTextProps`](../Components/Fundamentals/LMFeedText.md) | Customization for the right icon's text.    |
| `icon`        | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Customization for the right icon's icon.    |
| `onTap`       | `Function`                                                | Callback for when the right icon is tapped. |
| `placement`   | `String`                                                  | Placement of the icon relative to the text. |
| `buttonStyle` | `ViewStyle`                                               | Styling for the right icon's button.        |
| `isClickable` | `Boolean`                                                 | Whether the right icon is clickable.        |

Few of the customisation like header customisation, turning on/off the autoplay, footer, etc are done using the [`postListStyle`](./LMFeedPostListScreen.md/#customisation) in `STYLES`

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `PostDetailsScreenWrapper` file which will wrap the `DetailsScreen` within the `PostDetailContextProvider` along with `UniversalFeedContextProvider` so that the callbacks becomes accessible inside of the `DetailsScreen`.
- Create `postDetailScreenStyles` for customisation and call the `setCreatePostStyles` to set the customisation.

<Tabs>
<TabItem value="DetailsScreen" label="DetailsScreen">

```tsx
import {
  PostDetail,
  usePostDetailContext,
  useUniversalFeedContext,
} from "@likeminds.community/feed-rn-core";
import { Alert, Platform, Share } from "react-native";

const DetailsScreen = ({ navigation }) => {
  const {
    route,
    getCommentsReplies,
    addNewComment,
    addNewReply,
    commentLikeHandler,
    handleDeleteComment,
    handleEditComment,
    handleReportComment,
    handleScreenBackPress,
    onCommentOverflowMenuClick,
  } = usePostDetailContext();
  const { addPollOption, addNewComment, addNewReply } =
    useUniversalFeedContext();

  // customised addNewComment callback
  const customAddNewCommentProp = (postId) => {
    console.log("before new comment");
    addNewComment(postId);
    console.log("after new comment", postId);
  };
  // customised addNewReply callback
  const customAddNewReplyProp = (postId, commentId) => {
    console.log("before add reply");
    addNewReply(postId, commentId);
    console.log("after add reply");
  };

  const postDetailScreenStyles = {
    shouldHideSeparator: false,
    noCommentViewStyle: {
      backgroundColor: "red",
    },
  };

  // post details screen customisation
  if (postDetailScreenStyles) {
    STYLES.setCreatePostStyles(postDetailScreenStyles);
  }

  return (
    <PostDetail
      route={route}
      navigation={navigation}
      addNewCommentProp={(id) => customAddNewCommentProp(id)}
      addNewReplyProp={(postId, commentId) =>
        customAddNewReplyProp(postId, commentId)
      }
    />
  );
};

export default DetailsScreen;
```

</TabItem>
<TabItem value="PostDetailsScreenWrapper" label="PostDetailsScreenWrapper">

```tsx
import DetailsScreen from "<<path_to_DetailsScreen.tsx>>";
import {
  PostDetailContextProvider,
  UniversalFeedContextProvider,
} from "@likeminds.community/feed-rn-core";

const PostDetailsScreenWrapper = ({ navigation, route }) => {
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <PostDetailContextProvider navigation={navigation} route={route}>
        <DetailsScreen />
      </PostDetailContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default PostDetailsScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `PostDetailsScreenWrapper` as a Stack screen in your `NavigationContainer`.

```ts
import {
  POST_DETAIL,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import PostDetailsScreenWrapper from "<<path_to_PostDetailsScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

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
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={POST_DETAIL}
            component={PostDetailsScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
