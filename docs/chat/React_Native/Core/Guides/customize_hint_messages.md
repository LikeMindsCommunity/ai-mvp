---
sidebar_position: 3
title: How to customize input box hint messages
---

# Introduction

This page demonstrates how to customize input box hint messages. Hint messages are predefined, hardcoded messages that provide contextual information to users. The customizable hint messages include:

### Step 1: Getting Started

Follow the [Getting Started](../../getting-started.md) section to install dependency required along with creation of `lmChatClient` for interaction with data layer.

### Step 2: Use of LMOverlayProvider

Create a component which will get rendered on switching to Community tab and import the `LMOverlayProvider` from the core layer which we have just installed in [getting started](../../getting-started.md) step, and use it by providing all required props. The `LMOverlayProvider` will be the highest level screen and it will wrap all other screens.

```tsx
import { LMOverlayProvider } from "@likeminds.community/chat-rn-core";

function CommunityScreen(): React.JSX.Element {
  return (
    <LMOverlayProvider
      lmChatClient={lmChatClient}
      userName={userName}
      userUniqueId={userUniqueId}
      profileImageUrl={profileImageUrl}
      lmChatInterface={lmChatInterface}
    >
      {/* Add navigation container */}
    </LMOverlayProvider>
  );
}

export default CommunityScreen;
```
### Step 3: Creation of Chatroom screen with custom hint messages

#### Interface

```tsx
interface HintMessages {
  messageForRightsDisabled?: string;
  messageForMemberCanMessage?: string;
  messageForAnnouncementRoom?: string;
  respondingDisabled?: string;
}
```

| Parameter                    | Description                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| `messageForRightsDisabled`   | A message indicating that the user does not have the rights to perform a certain action |
| `messageForMemberCanMessage` | A message indicating that the member is allowed to send messages                        |
| `messageForAnnouncementRoom` | A message specific to announcement rooms                                                |
| `respondingDisabled`         | A message indicating that responding is disabled                                        |

#### Usage

```tsx
import {
  ChatRoom,
  ChatroomHeader,
  MessageList,
  MessageInput,
} from "@likeminds.community/chat-rn-core";

interface HintMessages {
  messageForRightsDisabled?: string;
  messageForMemberCanMessage?: string;
  messageForAnnouncementRoom?: string;
  respondingDisabled?: string;
}

export function ChatroomScreen() {

  const hintMessages: HintMessages = {
    messageForMemberCanMessage:
      "Sorry, at this time only CM's can message here!",
    messageForRightsDisabled:
      'Sorry your rights has been disabled, contact you CM for more info!',
  };

  return (
    <ChatRoom>
      <ChatroomHeader />
      <MessageList />
      <MessageInput hintMessages={hintMessages} />
    </ChatRoom>
  );
}
```

### Step 4: Navigation Setup

Next, install the below dependencies for creation of a StackNavigator

```bash
npm install @react-navigation/native @react-navigation/native-stack;
```

After installing the above dependencies, create a `RootNavigation` file with `navigationRef` exported from it, which later will be used for navigation purposes.

`RootNavigation.js` :

```tsx
import {
  StackActions,
  createNavigationContainerRef,
} from "@react-navigation/native";

export const navigationRef = createNavigationContainerRef();

// to navigate from one screen to another
export function navigate(name, params) {
  if (navigationRef.isReady()) {
    navigationRef.navigate(name, params);
  }
}

// to push one screen in the stack over another
export function push(name, params) {
  if (navigationRef.isReady()) {
    navigationRef.current?.dispatch(StackActions.push(name, params));
  }
}

// to pop one screen in the stack
export function pop() {
  if (navigationRef.isReady()) {
    navigationRef.current?.dispatch(StackActions.pop());
  }
}

// to get recent routes in the navigation stack
export function getRecentRoutes() {
  if (navigationRef.isReady()) {
    return navigationRef.getRootState();
  }
}
```

Now, create a StackNavigator which will enable to navigate between different screens imported from `@likeminds.community/chat-rn-core`.

```tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import {
  CarouselScreen,
  CreatePollScreen,
  ImageCropScreen,
  PollResult,
  VideoPlayer,
  LMOverlayProvider,
} from "@likeminds.community/chat-rn-core";
import { navigationRef } from "./RootNavigation";

const Stack = createNativeStackNavigator();

function CommunityScreen(): React.JSX.Element {
  const chatroomId = ""; // pass in the chatroom id of chatroom to be displayed
  return (
    <LMOverlayProvider
      lmChatClient={lmChatClient}
      userName={userName}
      userUniqueId={userUniqueId}
      profileImageUrl={profileImageUrl}
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator>
          <Stack.Screen
            name="Chatroom"
            component={ChatroomScreen}
            initialParams={{
              chatroomID: chatroomId,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
}

export default CommunityScreen;
```