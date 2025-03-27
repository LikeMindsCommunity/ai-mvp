---
sidebar_position: 13
title: User Onboarding
slug: /react-native/core/screens/user-onboarding-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `LMUserOnboardingScreen` is designed to provide users the interface to set up their profile which includes their username and an optional profile picture.

<Tabs>
    <TabItem value="withNoStyle" label="Without Custom Styles">
        <p align="center">
            <img
            src="/img/reactNative/react-native-onboarding-without-styles.webp"
            alt="LMFeedLikeListScreen"
            style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
            />
        </p>
    </TabItem>
    <TabItem value="withStyles" label="With Custom Styles">
         <p align="center">
            <img
            src="/img/reactNative/react-native-onboarding-with-styles.webp"
            alt="Another Image"
            style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
            />
        </p>
    </TabItem>
</Tabs>

## Callbacks

- `onCTAButtonClickedProp()`: Triggered when the user presses on the CTA button during user onboarding.
- `onPickProfileImageClickedProp()`: Triggered when a user presses on the pick image button to select an image as user profile from their gallery.

## Customisation with Props

| Property                    | Type     | Description                                        | Required           |
| --------------------------- | -------- | -------------------------------------------------- | ------------------ |
| `userNameMaxCharacterLimit` | `number` | Sets the maximum character limit for the username. |                    |
| `createScreenTitle`         | `string` | Title text for the creation screen.                | :heavy_check_mark: |
| `createScreenSubtitle`      | `string` | Subtitle text for the creation screen.             |                    |
| `createScreenHeaderTitle`   | `string` | Header title text for the creation screen.         |                    |
| `createScreenCtaButtonText` | `string` | Text for the CTA button on the creation screen.    |                    |
| `editScreenTitle`           | `string` | Title text for the edit screen.                    |                    |
| `editScreenSubtitle`        | `string` | Subtitle text for the edit screen.                 |                    |
| `editScreenHeaderTitle`     | `string` | Header title text for the edit screen.             |                    |
| `editScreenCtaButtonText`   | `string` | Text for the CTA button on the edit screen.        |                    |
| `addPicturePrompt`          | `string` | Text prompt for adding a picture.                  |                    |
| `maxPictureSizePrompt`      | `string` | Text prompt for the maximum picture size.          |                    |
| `userNameInputBoxLabel`     | `string` | Label text for the username input box.             |                    |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `LMUserOnboardingScreen` or added your own custom implmentation of it as a Stack screen in your `NavigationContainer`.

### Step 1: Create Custom Screen and Wrapper

```tsx
import React from "react";
import {
  UniversalFeedContextProvider,
  UserOnboardingContextProvider,
} from "../context";
import UserOnboardingScreen from "../screens/userOnboardingScreen";
import { useUserOnboardingContext } from "../context/userOnboardingContext";

function CustomUserOnboardingScreen() {
  const { onCTAButtonClicked, onPickProfileImageClicked } =
    useUserOnboardingContext();
  const customOnCTAButtonClickedHandler = () => {
    console.log("before");
    onCTAButtonClicked();
    console.log("after");
  };
  const customOnPickProfileImageClickedHandler = () => {
    console.log("before");
    onPickProfileImageClicked();
    console.log("after");
  };
  return (
    <UserOnboardingScreen
      userNameMaxCharacterLimit={25}
      createScreenHeaderTitle={"Create User Profile"}
      editScreenHeaderTitle={"Edit User Profile"}
      onCTAButtonClickedProp={customOnCTAButtonClickedHandler}
      onPickProfileImageClickedProp={customOnPickProfileImageClickedHandler}
    />
  );
}

export default function UserOnboardingScreenWrapper({
  navigation,
  route,
}: any) {
  return (
    <UserOnboardingContextProvider navigation={navigation} route={route}>
      <CustomUserOnboardingScreen />
    </UserOnboardingContextProvider>
  );
}
```

### Step 2: Add the above created Wrapper to the navigation stack

```tsx
import {
  LMFeedPollResult,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import { USER_ONBOARDING_SCREEN } from "@likeminds.community/feed-rn-core/constants/screenNames";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  const userOnboardingScreenStyles = {
    userNameInputBoxStyle: {
      placeholderText: "Enter your username",
    },
    ctaButtonStyle: {
      backgroundColor: "purple",
      borderRadius: 3,
    },
    ctaButtonTextStyle: {
      color: "white",
    },
    pickImageIconStyles: {
      color: "black",
    },
    pickImageButtonStyles: {
      backgroundColor: "white",
    },
  };

  // user onboarding screen customisation
  if (userOnboardingScreenStyles) {
    STYLES.setOnBoardingScreenStyles(userOnboardingScreenStyles);
  }

  return (
    <NavigationContainer ref={navigationRef} independent={true}>
      <LMOverlayProvider
        myClient={myClient} // pass in the LMFeedClient created
        apiKey={apiKey} // pass in the API Key generated
        userName={userName} // pass in the logged-in user's name
        userUniqueId={userUniqueID} // pass in the logged-in user's uuid
        isUserOnboardingRequired={true} // pass a boolean whether user onboarding is required or not
      >
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={USER_ONBOARDING_SCREEN}
            component={UserOnboardingScreenWrapper}
            options={{
              headerShown: false,
            }}
          />
        </Stack.Navigator>
      </LMOverlayProvider>
    </NavigationContainer>
  );
};
```
