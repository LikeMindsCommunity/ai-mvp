---
sidebar_position: 11
title: Create Poll
slug: /react-native/core/screens/create-poll-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `CreatePollScreen` allows users to create poll by adding question, options. It provides various UI components and functionalities to facilitate the poll creation process.

<img
src={require('../../../../static/img/Poll/CreatePoll.webp').default}
alt="LMFeedLikeListScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMFeedHeader](../Components/Fundamentals/LMFeedHeader.md)
- [LMFeedProfilePicture](../Components/Fundamentals/LMFeedProfilePicture.md)
- [LMFeedCreatePoll](../Components/Poll/LMFeedCreatePoll.md)
- [LMFeedText](../Components/Fundamentals/LMFeedText.md)

## Data Variables

- `memberData`: Stores the feed logged in member data.

## Callbacks

- `onPollExpiryTimeClicked`: Triggered when the poll expiry time is clicked.
- `onAddOptionClicked`: Triggered when the option to add a new poll option is clicked.
- `onPollOptionCleared`: Triggered when a poll option is cleared. Provides the index of the cleared option.
- `onPollCompleteClicked`: Triggered when the complete poll button is clicked.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMFeedCreatePollScreen`. You can set the `header` styles in [`pollStlye`](../Components/Poll/LMFeedCreatePoll.md) in `STYLES`.

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `CreatePollScreenWrapper` file which will wrap the `CreatePollScreen` within the `CreatePollContextProvider` so that the callbacks becomes accessible inside of the `CreatePollScreen`.
- Create `createPollStyle` for customisation and call the `setCreatePollStyles` to set the customisation.

<Tabs>
<TabItem value="CreatePollScreen" label="CreatePollScreen">

```tsx
import {
  LMFeedCreatePollScreen,
  useCreatePollContext,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import React from "react";

const CreatePollScreen = () => {
  const { showDatePicker, addNewOption, removeAnOption, postPoll } =
    useCreatePollContext();

  // customised showDatePicker callback
  const onPollExpiryTimeClicked = () => {
    console.log("do something before onPollExpiryTimeClicked");
    showDatePicker();
    console.log("do something after onPollExpiryTimeClicked");
  };

  // customised addNewOption callback
  const onAddOptionClicked = () => {
    console.log("do something before onAddOptionClicked");
    addNewOption();
    console.log("do something after onAddOptionClicked");
  };

  const createPollStyle = {
    pollQuestionsStyle: {
      fontSize: 16,
      color: "black",
      borderBottomWidth: 1,
      borderBottomColor: "gray",
      marginBottom: 10,
    },
    pollOptionsStyle: {
      fontSize: 16,
      color: "black",
      borderBottomWidth: 1,
      borderBottomColor: "gray",
      marginBottom: 10,
    },
    pollExpiryTimeStyle: {
      fontSize: 16,
      color: "black",
      marginBottom: 10,
    },
    pollAdvancedOptionTextStyle: {
      fontSize: 16,
      color: "blue",
      marginBottom: 10,
    },
    pollAdvanceOptionsSwitchThumbColor: "green",
    pollAdvanceOptionsSwitchTrackColor: "lightgreen",
  };

  // create poll screen customisation
  if (createPollStyle) {
    STYLES.setCreatePollStyles(createPollStyle);
  }

  return (
    <LMFeedCreatePollScreen
      onPollExpiryTimeClicked={onPollExpiryTimeClicked}
      onAddOptionClicked={onAddOptionClicked}
    />
  );
};

export default CreatePollScreen;
```

</TabItem>
<TabItem value="CreatePollScreenWrapper" label="CreatePollScreenWrapper">

```tsx
import {
  LMFeedCreatePollScreen,
  CreatePollContextProvider,
} from "@likeminds.community/feed-rn-core";
import CreatePollScreen from "<<path_to_CreatePollScreen.tsx>>";

const CreatePollScreenWrapper = ({ navigation, route }) => {
  return (
    <CreatePollContextProvider navigation={navigation} route={route}>
      <CreatePollScreen />
    </CreatePollContextProvider>
  );
};

export default CreatePollScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your ` App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `CreatePollScreenWrapper` as a Stack screen in your `NavigationContainer`.

```ts
import { LMOverlayProvider, STYLES } from "@likeminds.community/feed-rn-core";
import { CREATE_POLL_SCREEN } from "@likeminds.community/feed-rn-core/constants/screenNames";
import CreatePollScreenWrapper from "<<path_to_CreatePollScreenWrapper.tsx>>";
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
            name={CREATE_POLL_SCREEN}
            component={CreatePollScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
