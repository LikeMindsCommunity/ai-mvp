---
sidebar_position: 4
title: How to use React Native SDK to Initiate Direct Messaging with a user
---

# Introduction

This is an example page showcasing what steps to be performed to initiate Direct Messaging with a person. The following steps help you perform the above mentioned.

### Step 1: Getting Started

Follow the [getting started](../../getting-started.md) section to install dependency required along with creation of `lmChatClient` for interaction with data layer.

### Step 2: Check DM Limit

Call the `checkDMLimit()` method firstly using `lmChatClient` created with payload as `uuid` of the user with whom we want to initiate Direct Messaging.

```tsx
const payload: any = {
  uuid: 23233, // Enter the uuid of the logged in user
}
const response = await lmChatClient?.checkDMLimit(payload)

if (response.success) {
  // your function to process the response data
  processResponse(response)
} else {
  // your function to process error message
  processError(response)
}
```

If the response have `chatroomId` in it, then you can directly navigate to the [Channel screen](../Screens/channel.md) using the `chatroomId` passed as prop to the Channel screen. Continue to Step 5.

### Step 3: Create DM Request

Next, if the `checkDMLimit()` does not return a `chatroomId`, it means that Direct Messaging with that particular user is for the first time and hence we have to create a DM channel for it using the `createDMChatroom()` method with payload as `uuid` of the user with whom we want to initiate Direct Messaging..

```tsx
const payload: any = {
  uuid: 23233, // Enter the uuid of the user with whom we want to initiate Direct Messaging.
}
const response = await lmChatClient?.createDMChatroom(payload)

if (response.success) {
  // your function to process the response data
  processResponse(response)
} else {
  // your function to process error message
  processError(response)
}
```

In response of this one, you will get the `chatroomId` for the new DM channel created and then navigate to the [Channel screen](../Screens/channel.md) using this `chatroomId`.

### Step 4: Get chatroom info

You can hit the `getChatroom` method with the `chatroomId` as payload, and it will return all details of chatroom including `unreadCount` and `lastConversation`.

```tsx
const payload: any = {
  chatroomId: 89899, // pass in your chatroomId.
}
const response = await lmChatClient.getChatroom(payload)

if (response.success) {
  // your function to process the response data
  processResponse(response)
} else {
  // your function to process error message
  processError(response)
}
```

### Step 5: Navigation Setup

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
} from "@react-navigation/native"

export const navigationRef = createNavigationContainerRef()

// to navigate from one screen to another
export function navigate(name, params) {
  if (navigationRef.isReady()) {
    navigationRef.navigate(name, params)
  }
}

// to push one screen in the stack over another
export function push(name, params) {
  if (navigationRef.isReady()) {
    navigationRef.current?.dispatch(StackActions.push(name, params))
  }
}

// to pop one screen in the stack
export function pop() {
  if (navigationRef.isReady()) {
    navigationRef.current?.dispatch(StackActions.pop())
  }
}

// to get recent routes in the navigation stack
export function getRecentRoutes() {
  if (navigationRef.isReady()) {
    return navigationRef.getRootState()
  }
}
```

Now, create a StackNavigator which will enable to navigate between different screens imported from `@likeminds.community/chat-rn-core`.

```tsx
import { NavigationContainer } from "@react-navigation/native"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { ChatRoom } from "@likeminds.community/chat-rn-core"
import { navigationRef } from "./RootNavigation"

const Stack = createNativeStackNavigator()

function CommunityScreen(): React.JSX.Element {
  const chatroomId = "89982" // pass in the chatroom id of chatroom to be displayed
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
            component={ChatRoom}
            initialParams={{
              chatroomID: chatroomId,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  )
}

export default CommunityScreen
```
