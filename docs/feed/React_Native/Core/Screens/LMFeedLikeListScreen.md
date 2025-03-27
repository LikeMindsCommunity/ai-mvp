---
sidebar_position: 6
title: Like List
slug: /react-native/core/screens/like-list-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `LMFeedLikeListScreen` is designed to present a list of users who have liked a specific post/comment. It displays the user images along with their names and a custom title (if available), and provides a count of the total number of likes for the post.

<img
src={require('../../../../static/img/iOS/screens/likeList.webp').default}
alt="LMFeedLikeListScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMFeedHeader](../Components/Fundamentals/LMFeedHeader.md)
- [LMFeedMemberListItem](../Components/LMFeedMemberItem.md)
- [LMFeedLoader](../Components/Fundamentals/LMFeedLoader.md)

## Data Variables

- `totalLikes`: Stores the total number of likes conforming to `number` datatype.
- `postLike`: Stores the likes on a particular post conforming to `[]`.

## Callbacks

- `onTapUserItemProp`: Triggered when a user item is tapped. Provides the `LMUserUI` object of the tapped user.
- `handleScreenBackPressProp`: Triggered when the back button is pressed on the screen.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `postLikesListStyle` in `STYLES`.

| Property                   | Type                                             | Description                            |
| -------------------------- | ------------------------------------------------ | -------------------------------------- |
| `screenHeader`             | [`LMHeaderProps`](../Components/LMFeedHeader.md) | The header component for the screen.   |
| `likeListItemStyle`        | `ViewStyle`                                      | Style for each like list item.         |
| `userNameTextStyle`        | `TextStyle`                                      | Style for the user's name text.        |
| `userDesignationTextStyle` | `TextStyle`                                      | Style for the user's designation text. |

For member's profile picture, the customisation is done using `profilePicture` in `header` of [`postListStyle`](./LMFeedPostListScreen.md/#customisation)

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `LikesScreenWrapper` file which will wrap the `LikesScreen` within the `PostLikesListContextProvider` so that the callbacks becomes accessible inside of the `LikesScreen`.
- Create `postLikesListStyles` for customisation and call the `setPostLikesListStyles` to set the customisation.

<Tabs>
<TabItem value="LikesScreen" label="LikesScreen">

```tsx
import {
  PostLikesList,
  usePostLikesListContext,
} from "@likeminds.community/feed-rn-core";

const LikesScreen = ({ route }) => {
  const { navigation, handleScreenBackPress } = usePostLikesListContext();

  // customised handleScreenBackPress callback
  const customBackHandler = () => {
    console.log("do something before back click");
    handleScreenBackPress();
    console.log("do something after back click");
  };

  const postLikesListStyles = {
    userNameTextStyle: {
      color: "green",
    },
    userDesignationTextStyle: {
      color: "red",
    },
  };

  // like list screen customisation
  if (postLikesListStyles) {
    STYLES.setPostLikesListStyles(postLikesListStyles);
  }
  return (
    <PostLikesList
      route={route}
      navigation={navigation}
      handleScreenBackPressProp={() => customBackHandler()}
    />
  );
};

export default LikesScreen;
```

</TabItem>
<TabItem value="LikesScreenWrapper" label="LikesScreenWrapper">

```tsx
import { PostLikesListContextProvider } from "@likeminds.community/feed-rn-core";
import LikesScreen from "<<path_to_LikesScreen.tsx>>";

const LikesScreenWrapper = ({ navigation, route }) => {
  return (
    <PostLikesListContextProvider navigation={navigation} route={route}>
      <LikesScreen route={route} />
    </PostLikesListContextProvider>
  );
};

export default LikesScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `LikesScreenWrapper` as a Stack screen in your `NavigationContainer`.

```ts
import {
  POST_LIKES_LIST,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import LikesScreenWrapper from "<<path_to_LikesScreenWrapper.tsx>>";
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
          <Stack.Screen name={POST_LIKES_LIST} component={LikesScreenWrapper} />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
