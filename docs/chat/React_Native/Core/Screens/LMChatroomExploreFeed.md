---
sidebar_position: 2
title: Explore Feed Screen
slug: /react-native/core/screens/explore-feed-screen
---

## Overview

The `ExploreFeed` screen displays a feed of posts or conversations in the LikeMinds chat application. It allows users to browse through various content, interact with posts, and explore trending or recommended topics. This screen serves as a discovery hub, providing an engaging way for users to find new conversations or communities to join.

<img
src={require('../../../../static/img/reactNative/lmExploreFeed.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [ExploreFeedFilters](../Components/Explore%20Feed/LMChatroomExploreFeedFilters.md)
- [ExploreFeedItem](../Components/Explore%20Feed/LMChatroomExploreFeedItem.md)

## Data Variables

- `exploreChatrooms`: Contains a list of chatrooms available for users to explore within the feed.
- `pinnedChatroomsCount`: Stores the number of chatrooms that have been pinned by the user for quick access.
- `chats`: Holds the list of chats or conversations displayed in the feed.
- `filterState`: Represents the current state of filters applied to the feed, determining which content is shown.
- `isPinned`: A flag indicating whether a chatroom is pinned or not.

## Customisation

The `ExploreFeed` screen can be customised using the [`exploreChatroomStyles`](../Components/ExploreFeed/LMChatroomExploreFeedItem.md/#customisation)

## Props

| Property                | Type     | Description                                                 |
| ----------------------- | -------- | ----------------------------------------------------------- |
| `backIconPath`          | `string` | Path to the back icon for navigation.                       |
| `filterIconPath`        | `string` | Path to the filter icon used in the feed.                   |
| `participantsIconPath`  | `string` | Path to the participants icon used to display participants. |
| `totalMessagesIconPath` | `string` | Path to the total messages icon in the chatroom.            |
| `joinButtonPath`        | `string` | Path to the button icon for joining a chatroom.             |
| `joinedButtonPath`      | `string` | Path to the button icon for a joined chatroom.              |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `ExploreFeed` as a Stack screen in your `NavigationContainer`.
- Create `exploreChatroomStyle` for customisation and call the `setExploreChatroomStyle` to set the customisation.

```tsx title="App.tsx"
import {
  EXPLORE_FEED,
  ExploreFeed,
  STYLES,
  Themes
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  const exploreChatroomStyle = {
    header: {
      color: "red",
    },
    filterHeader: {
      color: "blue",
    },
  };

  if (exploreChatroomStyle) {
    STYLES.setExploreChatroomStyle(exploreChatroomStyle);
  }

  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">} // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={EXPLORE_FEED}
            component={ExploreFeed}
            initialParams={{
              backIconPath: "",
              filterIconPath: "",
              participantsIconPath: "",
              totalMessagesIconPath: "",
              joinButtonPath: "",
              joinedButtonPath: "",
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
