---
sidebar_position: 7
title: Topic Selection
slug: /react-native/core/screens/topic-selection-screen
---

## Overview

`LMFeedTopicSelectionScreen` provides a user interface for selecting topics. It displays a list of topics in a table view, with the ability to search and filter the topics.

<img
src={require('../../../../static/img/iOS/screens/topicSelection.webp').default}
alt="LMFeedTopicSelectionScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Data Variables

- `topics`: Stores the topic data received as a response of an API call.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `topicsStyle` in `STYLES`.

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `TopicFeedWrapper` file which will wrap the `TopicFeed` within the `CreatePostContextProvider` along with `UniversalFeedContextProvider`.

```ts
import {
  TopicFeed,
  UniversalFeedContextProvider,
} from "@likeminds.community/feed-rn-core";
import { CreatePostContextProvider } from "@likeminds.community/feed-rn-core/context/createPostContext";

const TopicFeedWrapper = ({ navigation, route }) => {
  const topicsStyle = {
    allTopicPlaceholder: "Type in something...",
    topicListStyle: {
      color: "red",
    },
  };

  // topic feed screen customisation
  if (topicsStyle) {
    STYLES.setTopicsStyles(topicsStyle);
  }
  return (
    <UniversalFeedContextProvider navigation={navigation} route={route}>
      <CreatePostContextProvider navigation={navigation} route={route}>
        <TopicFeed />
      </CreatePostContextProvider>
    </UniversalFeedContextProvider>
  );
};

export default TopicFeedWrapper;
```
### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `TopicFeedWrapper` as a Stack screen in your `NavigationContainer`.


```ts
import {
  TOPIC_FEED,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import { TopicFeedWrapper } from "<<path_to_TopicFeedWrapper.tsx>>";
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
          <Stack.Screen name={TOPIC_FEED} component={TopicFeedWrapper} />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
