---
sidebar_position: 3
title: Chatroom Header
slug: /react-native/core/components/chatroom-header
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `ChatroomHeader` component is designed to display chatroom name, number of participants and chatroom actions, etc on the top.

<img
src={require('../../../../../static/img/reactNative/lmChatroomHeader.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Callbacks

- `navigateToGroupDetails`: Its trigerred on pressing of the chatroom name, and it returns the chatroom details.

## Customisation

| Property                      | Type                                                        | Description                                |
| ----------------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| `chatroomNameHeaderStyle`     | [ChatroomNameHeaderStyle](#chatroomnameheaderstyle)         | Custom style for the chatroom name header  |
| `chatroomSubHeaderStyle`      | [ChatroomSubHeaderStyle](#chatroomsubheaderstyle)           | Custom style for the chatroom subheader    |
| `chatroomSelectedHeaderIcons` | [ChatroomSelectedHeaderIcons](#chatroomselectedheadericons) | Custom style for the selected header icons |

### Chatroom Name Header Style

| Property     | Type   | Description                      |
| ------------ | ------ | -------------------------------- |
| `color`      | string | Text color of the chatroom name  |
| `fontSize`   | number | Font size of the chatroom name   |
| `fontFamily` | string | Font family of the chatroom name |

### Chatroom SubHeader Style

| Property     | Type   | Description                           |
| ------------ | ------ | ------------------------------------- |
| `color`      | string | Text color of the chatroom subheader  |
| `fontSize`   | number | Font size of the chatroom subheader   |
| `fontFamily` | string | Font family of the chatroom subheader |

### Chatroom Selected Header Icons

| Property    | Type   | Description                      |
| ----------- | ------ | -------------------------------- |
| `tintColor` | string | Tint color of the selected icons |

## Props

| Property                        | Type    | Description                                        |
| ------------------------------- | ------- | -------------------------------------------------- |
| `showChatroomIcon`              | boolean | Specifies whether to display the chatroom icon     |
| `customChatroomUserTitle`       | string  | Custom title for the chatroom user                 |
| `showThreeDotsOnHeader`         | boolean | Indicates whether to show three dots on the header |
| `showThreeDotsOnSelectedHeader` | boolean | Indicates whether to show three dots when selected |
| `gradientStyling`               | any     | Custom gradient styling for the header             |
| `backIconPath`                  | string  | Path for the custom back icon                      |
| `groupIcon`                     | any     | Custom group icon                                  |
| `hideSearchIcon`                | boolean | Indicates whether to hide the search icon          |

## Usage Example

:::info
The `ChatroomHeader` screen can be used by wrapping it inside the `ChatRoom` screen, and the callbacks object will be passed as a prop to `LMOverlayProvider`.
:::

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `ChatroomScreenWrapper` file which will wrap the `ChatroomScreen` within the `Chat` so that the callbacks becomes accessible inside of the `ChatroomScreen`.
- Create `chatroomHeaderStyles` for customisation and call the `setChatroomHeaderStyle` to set the customisation.

<Tabs>
<TabItem value="ChatroomScreen" label="ChatroomScreen">

```tsx
import {
  STYLES,
  ChatroomHeader,
  ChatRoom,
} from "@likeminds.community/chat-rn-core";

const ChatroomScreen = () => {
  const chatroomHeaderStyles = {
    chatroomNameHeaderStyle: {
      color: "white",
      fontSize: 18,
      fontFamily: "NunitoSans-Bold",
    },
    chatroomSubHeaderStyle: {
      color: "white",
      fontSize: 13,
    },
    chatroomSelectedHeaderIcons: {
      tintColor: "white",
    },
  };
  // chatroom header customisation
  if (chatroomHeaderStyles) {
    STYLES.setChatroomHeaderStyle(chatroomHeaderStyles);
  }

  return (
    <ChatRoom>
      <ChatroomHeader
        showChatroomIcon={true}
        customChatroomUserTitle={true}
        showThreeDotsOnHeader={true}
        showThreeDotsOnSelectedHeader={true}
        backIconPath={""} // path to your customised back icon
        groupIcon={""} // path to your customised group icon
        hideSearchIcon={false}
      />
      {/* Other chat components */}
    </ChatRoom>
  );
};

export default ChatroomScreen;
```

</TabItem>
<TabItem value="ChatroomScreenWrapper" label="ChatroomScreenWrapper">

```tsx
import { Chat } from "@likeminds.community/chat-rn-core";
import { ChatroomScreen } from "<<path_to_ChatroomScreen.tsx>>";

function ChatroomScreenWrapper() {
  return (
    <Chat>
      <ChatroomScreen />
    </Chat>
  );
}

export default ChatroomScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `ChatroomScreenWrapper` as a Stack screen in your `NavigationContainer`.

```ts
import {
  CHATROOM,
  LMOverlayProvider,
  STYLES,
  NavigateToGroupDetailsParams,
} from "@likeminds.community/feed-rn-core";
import { ChatroomScreenWrapper } from "<<path_to_ChatroomScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  // custom callback class implementing carouselCallBackClass
  class CustomCallbacks implements LMCarouselScreenCallbacks {
    navigateToGroupDetails(params: NavigateToGroupDetailsParams) {
      // Override navigateToGroupDetails with custom logic
    }
  }

  const lmFeedInterface = new CustomCallbacks();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      lmFeedInterface={lmFeedInterface} // object having customised callbacks
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={CHATROOM}
            component={ChatroomScreenWrapper}
            initialParams={{
              chatroomID: chatroomId,
              announcementRoomId: announcementRoomId,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
