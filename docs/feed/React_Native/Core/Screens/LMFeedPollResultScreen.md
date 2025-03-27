---
sidebar_position: 12
title: Poll Result
slug: /react-native/core/screens/poll-result-screen
---

## Overview

`LMFeedPollResultScreen` is a view controller responsible for displaying poll results. It provides a user interface with a horizontally scrollable list of poll options and a paginated view of user lists for each option.

<img
src={require('../../../../static/img/Poll/PollResult.webp').default}
alt="LMFeedLikeListScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMFeedHeader](../Components/Fundamentals/LMFeedHeader.md)
- [LMFeedProfilePicture](../Components/Fundamentals/LMFeedProfilePicture.md)
- [LMFeedLoader](../Components/Fundamentals/LMFeedLoader.md)
- [LMFeedText](../Components/Fundamentals/LMFeedText.md)

## Data Variables

- `userList`: Stores the list of users who have voted in the poll.

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `LMFeedPollResult` as a Stack screen in your `NavigationContainer`.

### App.tsx

```ts
import {
  POLL_RESULT,
  LMFeedPollResult,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
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
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={POLL_RESULT}
            component={LMFeedPollResult}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
