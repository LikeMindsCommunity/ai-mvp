---
sidebar_position: 4
title: Poll Result Screen
slug: /react-native/core/screens/poll-result-screen
---

## Overview

The `PollResult` component displays the results of a poll in the LikeMinds chat application, showcasing the poll question, options, and vote counts, along with visual elements to represent vote distribution, providing users with an engaging view of how others have voted.

<img
src={require('../../../../static/img/reactNative/lmPollResult.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [`LMChatroomHeader`](../Components/LMChatroomHeader.md)
- [`LMChatIcon`](../Components/Fundamentals/icon.md)
- [`LMChatTextView`](../Components/Fundamentals/text_view.md)

## Data Variables

- `userList`: Stores the list of users who have voted in the poll.

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `PollResult` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import {
  POLL_RESULT,
  PollResult,
  LMOverlayProvider,
  STYLES,
  Themes
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  const pollResultStyles = {
    fontColor: "red",
    primaryColor: "blue",
    fontTypes: {
      fontFamilyLight: "Nunito-light",
      fontFamilyMedium: "Nunito-medium",
    },
  };

  // poll result screen customisation
  if (pollResultStyles) {
    STYLES.setTheme(pollResultStyles);
  }

  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">} // // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={POLL_RESULT}
            component={PollResult}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
