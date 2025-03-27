---
sidebar_position: 4
title: Create Poll Screen
slug: /react-native/core/screens/create-poll-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `CreatePollScreen` component is responsible for rendering the UI that allows users to create a poll within a chatroom or conversation. It provides input fields for entering poll options, a question, and other related configurations. This component manages the state of the poll creation process and ensures that the input data is validated before submission. It also supports customization of styles and integrates with the broader chat system for submission and interaction.

<img
src={require('../../../../static/img/reactNative/lmCreatePollUI.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [`LMChatroomHeader`](../Components/Chatroom/LMChatroomHeader.md)
- [`LMChatroomCreatePollUI`](../Components/Poll/LMChatroomCreatePoll.md)
- [`LMChatIcon`](../Components/Fundamentals/icon.md)
- [`LMChatTextView`](../Components/Fundamentals/text_view.md)

## Data Variables

- `memberData`: Stores the chat logged in member data.

## Callbacks

- `onPollExpiryTimeClicked`: Triggered when the poll expiry time is clicked.
- `onAddOptionClicked`: Triggered when the option to add a new poll option is clicked.
- `onPollOptionCleared`: Triggered when a poll option is cleared. Provides the index of the cleared option.
- `onPollCompleteClicked`: Triggered when the complete poll button is clicked.

## Customisation

The `CreatePollScreen` can be customised using the [`pollStyles`](../Components/Poll/LMChatroomCreatePoll.md/#customisation).

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `CreatePollScreenWrapper` file which will wrap the `CreatePollScreen` within the `CreatePollContextProvider` so that the callbacks becomes accessible inside of the `CreatePollScreen`.
- Create `createPollStyle` for customisation and call the `setCreatePollStyles` to set the customisation.

<Tabs>
<TabItem value="CreatePollScreen" label="CreatePollScreen">

```tsx
import {
  CreatePollScreen,
  useCreatePollContext,
  STYLES,
} from "@likeminds.community/chat-rn-core";
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
    <CreatePollScreen
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
import { CreatePollContextProvider } from "@likeminds.community/chat-rn-core";
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

```tsx title="App.tsx"
import { LMOverlayProvider, STYLES, Themes } from "@likeminds.community/chat-rn-core";
import { CREATE_POLL_SCREEN } from "@likeminds.community/chat-rn-core/constants/screenNames";
import CreatePollScreenWrapper from "<<path_to_CreatePollScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();

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
            name={CREATE_POLL_SCREEN}
            component={CreatePollScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
