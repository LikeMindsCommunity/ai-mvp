---
sidebar_position: 1
title: "Getting Started"
slug: /react-native/getting-started
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

The LikeMinds React Native Feed SDK empowers you to integrate personalized and engaging feeds into your app, enhancing user experiences and driving user engagement. This guide will walk you through the steps to get started with the LikeMinds React Native Feed SDK and set up a dynamic feed in your application.

## Prerequisites

Before you begin, make sure you have the following installed:

- Node.js and npm (Node Package Manager)
- React Native CLI
- Xcode (for iOS development)
- Android Studio (for Android development)
- Generate API key from [LikeMinds dashboard](https://dashboard.likeminds.community/)

## Step-by-Step Integration Guide

Follow these steps to integrate the LikeMinds Feed SDK into your React Native application using NPM:

### Step 1 - Installation

LikeMinds Feed SDK has a number of peer dependencies that are required to take advantage of all of the out of the box features. It is suggested you follow the install instructions for each package to ensure it is properly setup. Most if not all of the required packages now support auto-linking so setup should be minimal.

#### Add LikeMinds Feed React Native SDK

```bash
npm install @likeminds.community/feed-rn-core@1.13.3 @likeminds.community/feed-rn@1.5.2
```

#### Setup React Native Firebase for Notifications, don't setup if it's already done. Do checkout React Native Firebase Docs

```bash
npm install @react-native-firebase/app @react-native-firebase/messaging @notifee/react-native
```

#### Add React Navigation dependencies, don't install if already installed

```bash
npm install @react-navigation/material-top-tabs @react-navigation/native @react-navigation/native-stack @react-navigation/stack react-native-screens react-native-safe-area-context react-native-pager-view
```

#### Add the listed dependencies

```bash
npm install @react-native-async-storage/async-storage@1.23.1 @react-native-community/datetimepicker@8.0.1 @react-native-community/netinfo@11.3.0 diff@5.1.0 react-native-create-thumbnail react-native-device-info@10.13.1 react-native-document-picker@9.1.0 react-native-file-viewer@2.1.5 react-native-gesture-handler@2.14.0 react-native-image-picker@7.1.0 react-native-image-zoom-viewer@3.0.1 react-native-pager-view@6.1.4 react-native-slider@0.11.0 react-native-swiper-flatlist@3.2.3 react-native-tab-view@3.5.0 react-native-toast-message@2.2.0 @types/react-native-video@5.0.14 react-native-video react-native-compressor react-native-svg react-native-circular-progress
```

#### Install Pods (iOS only)

```bash
npx pod-install
```

### Step 2 - Initiate LMFeedClient

1. To start using the package, import the `initMyClient()` method in your `App.tsx` or `App.js` file.

```ts
import { initMyClient } from "@likeminds.community/feed-rn-core";

export const lmFeedClient = initMyClient();

// To initiate user session, follow step 3
```

### Step 3 - Initiate User Session

You have successfully initiated `LMFeedClient`, now all you need to do is inflate Universal Feed Screen. You have the option to initiate a user session and navigate to Universal Feed Fragment using one of two approaches:

#### 1. With API Key

This approach should be used when you want to manage LikeMinds authentication tokens on frontend.

- Provide the API Key directly to the LikeMinds Feed SDK to initiate a user session.
- Pass the following parameters to `<LMOverlayProvider />` from `@likeminds.community/feed-rn-core`:
  - `apiKey`
  - `userName`
  - `uuid`
- If `userName` is not to be provided, set the `isUserOnboardingRequired` prop to `true` to onboard the user, allowing them to provide their own `userName`

```tsx
import {
  LMOverlayProvider,
  initMyClient,
} from "@likeminds.community/feed-rn-core";
import {LMFeedClient} from '@likeminds.community/feed-rn';
import { LMCoreCallbacks } from "@likeminds.community/feed-rn-core/setupFeed";
import { GestureHandlerRootView } from "react-native-gesture-handler";

const App = () => {
  const [myClient, setMyClient] = useState<LMFeedClient>();
  const apiKey = "<YOUR_API_KEY>";
  const userName = "<USER_NAME>";
  const uuid = "<USER_ID>";
  const onboardUser = <"BOOLEAN">;

  useEffect(() => {
    async function generateClient() {
      // Initiate LMChatClient as described in step 2
      const res: any = initMyClient();
      setMyClient(res);
    }
    generateClient();
  }, []);

  return (
    <>
      {userName && uuid && apiKey && myClient ? (
        <GestureHandlerRootView style={{ flex: 1 }}>
          <LMOverlayProvider
            myClient={myClient}
            apiKey={apiKey}
            userName={userName}
            userUniqueId={uuid}
            isUserOnboardingRequired={onboardUser}
          >
            {/* Follow step 4 to add navigation logic after user is successfully initiated with LM servers */}
          </LMOverlayProvider>
        </GestureHandlerRootView>
      ) : null}
    </>
  );
};

export default App;
```

#### 2. Without API Key

This approach should be used when you want to manage LikeMinds authentication tokens on your backend server.
In this case you eliminate the need to expose your API Key to your client app and your backend server is responsible for calling the [initiate API](https://docs.likeminds.community/rest-api/#/operations/sdkInitate) to obtain the `accessToken` and `refreshToken` which is passed to `<LMOverlayProvider />` from `@likeminds.community/feed-rn-core` to validate the user session.

1. Create a function to get `accessToken` and `refreshToken` from your backend using [initiate API](https://docs.likeminds.community/rest-api/#/operations/sdkInitate)

```tsx
function getTokens() {
  // Your implementation to fetch the LikeMinds authentication tokens
  // Also save these tokens in the initial state of the application as you will be required to pass these tokens to LMClientOverlayProvider.
}
```

2. Create an instance of `LMCoreCallbacks` and pass in the necessary callback functions.

:::info
`LMCoreCallbacks` takes two arguments:

1. `onAccessTokenExpiredAndRefreshed()`: This callback is triggered when the provided `accessToken` expires and is refreshed internally using the `refreshToken`.
2. `onRefreshTokenExpired()` This callback is triggered when the provided `refreshToken` expires. In this case, you need to provide a new `accessToken` and `refreshToken` from your backend server using our [initiate API](https://docs.likeminds.community/rest-api/#/operations/sdkInitate).

:::

```tsx
const lmCoreCallback = new LMCoreCallbacks(
  (accessToken: string, refreshToken: string) => {
    // Handle Access and Refresh token as per your implementation
  },
  async () => {
    // Get New Tokens and return it in the below format
    return {
      accessToken: "YOUR NEW ACCESS TOKEN",
      refreshToken: "YOUR NEW REFRESH TOKEN",
    };
  }
);
```

3. Add the `LMOverlayProvider` and pass the `accessToken` and `refreshToken` returned in Step 1.

```tsx
import {
  LMOverlayProvider
} from "@likeminds.community/feed-rn-core";
import {LMFeedClient} from '@likeminds.community/feed-rn';
import { LMCoreCallbacks } from "@likeminds.community/feed-rn-core/setupFeed";
import { GestureHandlerRootView } from "react-native-gesture-handler";

const App = () => {
  const [myClient, setMyClient] = useState<LMFeedClient>();
  const accessToken = "<YOUR_INITIAL_ACCESS_TOKEN>";
  const refreshToken = "<USER_INITIAL_REFRESH_TOKEN>";
  const onboardUser = <"BOOLEAN">;

  useEffect(() => {
    async function generateClient() {
      // Initiate LMChatClient as described in step 2
      const res: any = initMyClient();
      setMyClient(res);
    }
    generateClient();
  }, []);

  const lmCoreCallback = new LMCoreCallbacks(
    (accessToken: string, refreshToken: string) => {
      // Handle Access and Refresh token as per your implementation
    },
    async () => {
      // Get New Tokens and return it in the below format
      return {
        accessToken: "YOUR NEW ACCESS TOKEN",
        refreshToken: "YOUR NEW REFRESH TOKEN",
      };
    }
  );

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <LMOverlayProvider
        myClient={myClient}
        accessToken={accessToken}
        refreshToken={refreshToken}
        callbackClass={lmCoreCallback}
        isUserOnboardingRequired={onboardUser}
      >
        {/* Follow step 4 to add navigation logic after user is successfully initiated with LM servers */}
      </LMOverlayProvider>
    </GestureHandlerRootView>
  );
};

export default App;
```

:::tip
By choosing the appropriate method based on your backend infrastructure and security preferences, you can seamlessly integrate the Feed SDK into your application while ensuring secure and efficient session management.
:::

### Step 4 - Configure Navigation

Set up the navigation for your application using React Navigation. Create a `StackNavigator` in your `App.js` or equivalent file:

<Tabs>
<TabItem value="SocialFeed" label="Social Feed">

```tsx
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  UNIVERSAL_FEED,
  POST_DETAIL,
  CREATE_POST,
  CAROUSEL_SCREEN,
  POST_LIKES_LIST,
  LMOverlayProvider,
  CarouselScreen,
  LMFeedPollResult,
  NOTIFICATION_FEED,
  LMSocialFeedPostDetailScreen,
  LMCreatePollScreen,
  LMLikesScreen,
  LMNotificationScreen,
  LMTopicFeedScreen,
  LMSocialFeedScreen,
  LMUserOnboardingScreen,
  LMSocialFeedSearchScreenWrapper,
} from "@likeminds.community/feed-rn-core";
import {
  CREATE_POLL_SCREEN,
  POLL_RESULT,
  TOPIC_FEED,
  USER_ONBOARDING_SCREEN,
  SEARCH_SCREEN
} from "@likeminds.community/feed-rn-core/constants/screenNames";
import LMSocialFeedCreateScreen from "@likeminds.community/feed-rn-core/wrappers/socialFeedCreateWrapper";
import { FeedType } from "@likeminds.community/feed-rn-core";

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={USER_ONBOARDING_SCREEN}
            component={LMUserOnboardingScreen}
            options={{
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={UNIVERSAL_FEED}
            component={LMSocialFeedScreen}
            initialParams={{
              feedType: FeedType.UNIVERSAL_FEED,
            }}
          />
          <Stack.Screen
            name={POST_DETAIL}
            component={LMSocialFeedPostDetailScreen}
          />
          <Stack.Screen
            name={CREATE_POST}
            component={LMSocialFeedCreateScreen}
          />
          <Stack.Screen name={POST_LIKES_LIST} component={LMLikesScreen} />
          <Stack.Screen
            name={TOPIC_FEED}
            component={LMTopicFeedScreen}
            options={{ headerShown: true }}
          />
          <Stack.Screen
            name={NOTIFICATION_FEED}
            component={LMNotificationScreen}
          />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={CAROUSEL_SCREEN}
            component={CarouselScreen}
          />
          <Stack.Screen
            name={POLL_RESULT}
            component={LMFeedPollResult}
            options={{
              gestureEnabled: false,
            }}
          />
          <Stack.Screen
            name={CREATE_POLL_SCREEN}
            component={LMCreatePollScreen}
          />
          <Stack.Screen
            name={SEARCH_SCREEN}
            component={LMSocialFeedSearchScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

</TabItem>
<TabItem value="QnA Feed" label="QnA Feed">

```tsx
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import {
  UNIVERSAL_FEED,
  POST_DETAIL,
  CREATE_POST,
  CAROUSEL_SCREEN,
  POST_LIKES_LIST,
  LMOverlayProvider,
  CarouselScreen,
  LMFeedPollResult,
  NOTIFICATION_FEED,
  LMCreatePollScreen,
  LMLikesScreen,
  LMNotificationScreen,
  LMTopicFeedScreen,
  LMQnAFeedCreatePostScreen,
  LMQnAPostDetailScreen,
  LMQnAFeedScreen,
  LMUserOnboardingScreen,
  LMQnaFeedSearchScreenWrapper,
  FeedType,
} from "@likeminds.community/feed-rn-core";
import {
  CREATE_POLL_SCREEN,
  POLL_RESULT,
  TOPIC_FEED,
  USER_ONBOARDING_SCREEN,
  SEARCH_SCREEN
} from "@likeminds.community/feed-rn-core/constants/screenNames";

const Stack = createStackNavigator();

const App = () => {
  return (
    <>
      <NavigationContainer>
        {/* Navigation logic to be added after user is initiated as described in step 3 */}
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={USER_ONBOARDING_SCREEN}
            component={LMUserOnboardingScreen}
            options={{
              headerShown: false,
            }}
          />
          <Stack.Screen
            name={UNIVERSAL_FEED}
            component={LMQnAFeedScreen}
            initialParams={{
              feedType: FeedType.UNIVERSAL_FEED,
            }}
          />
          <Stack.Screen name={POST_DETAIL} component={LMQnAPostDetailScreen} />
          <Stack.Screen
            name={CREATE_POST}
            component={LMQnAFeedCreatePostScreen}
          />
          <Stack.Screen name={POST_LIKES_LIST} component={LMLikesScreen} />
          <Stack.Screen
            name={TOPIC_FEED}
            component={LMTopicFeedScreen}
            options={{ headerShown: true }}
          />
          <Stack.Screen
            name={NOTIFICATION_FEED}
            component={LMNotificationScreen}
          />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={CAROUSEL_SCREEN}
            component={CarouselScreen}
          />
          <Stack.Screen
            name={POLL_RESULT}
            component={LMFeedPollResult}
            options={{
              gestureEnabled: false,
            }}
          />
          <Stack.Screen
            name={CREATE_POLL_SCREEN}
            component={LMCreatePollScreen}
          />
          <Stack.Screen
            name={SEARCH_SCREEN}
            component={LMQnaFeedSearchScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

export default App;
```

</TabItem>
</Tabs>
