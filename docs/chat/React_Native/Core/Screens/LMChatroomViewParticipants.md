---
sidebar_position: 9
title: View Participants Screen
slug: /react-native/core/screens/view-participants-screen
---

## Overview

The `ViewParticipants` screen displays a list of participants in a chatroom within the LikeMinds chat application. It provides users with an overview of who is currently in the chat, including their usernames and potentially their status. This feature enhances community engagement by allowing users to see and connect with other participants, fostering interaction within the chatroom. The screen may also include options for managing participants, such as blocking or viewing profiles.

<img
src={require('../../../../static/img/reactNative/lmViewParticipants.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Data Variables

- `participants`: List of participants to be rendered.
- `chatroomID`: Id of the chatroom.
- `chatroomName`: Name of the chatroom.

## Customisation

The `ViewParticipants` screen can be customised using the [`memberDirectoryStyles`](../Widgets/Components/LMChatroomMemberList.md)

## Props

| Property       | Type      | Description                                     | Required           |
| -------------- | --------- | ----------------------------------------------- | ------------------ |
| `chatroomID`   | `string`  | Unique identifier for the chatroom.             | :heavy_check_mark: |
| `isSecret`     | `boolean` | Indicates if the chatroom is a secret chatroom. | :heavy_check_mark: |
| `chatroomName` | `string`  | The name of the chatroom being viewed.          | :heavy_check_mark: |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `ViewParticipants` as a Stack screen in your `NavigationContainer`.
- Create `memberDirectoryStyles` for customisation and call the `setMemberDirectoryStyle` to set the customisation.

```tsx title="App.tsx"
import {
  VIEW_PARTICIPANTS,
  ViewParticipants,
  STYLES,
  Themes
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  const memberDirectoryStyles = {
    userNameStyles: {
      color: "red",
    },
    userTitleStyles: {
      color: "blue",
    },
  };

  if (memberDirectoryStyles) {
    STYLES.setMemberDirectoryStyle(memberDirectoryStyles);
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
            name={VIEW_PARTICIPANTS}
            component={ViewParticipants}
            initialParams={{
              chatroomName: "LikeMinds ChatSpace",
              chatroomID: "495675",
              isSecret: false,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
