---
sidebar_position: 5
title: How to use React Native SDK for Single Channel as Community
---

# Introduction

This is an example page showcasing how we can use the screens, widgets, analytics and sdk functions to use single channel as community in your app. The following steps help you launch Community in your app using LikeMinds React Native Chat SDK:

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

### Step 3: Configure Navigation
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
import FileUploadScreenWrapper from '@likeminds.community/chat-rn-core/ChatSX/wrappers/FileUploadWrapper';
import ChatroomScreenWrapper from '@likeminds.community/chat-rn-core/ChatSX/wrappers/ChatroomScreenWrapper';

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
            component={ChatroomScreenWrapper}
            initialParams={{
              chatroomID: chatroomId,
            }}
          />
          <Stack.Screen
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
            }}
            name={"FileUpload"}
            component={FileUploadScreenWrapper}
            initialParams={{
              backIconPath: "", // add your back icon path here
              imageCropIcon: "", // add your image crop icon path here
            }}
          />
          <Stack.Screen name={"VideoPlayer"} component={VideoPlayer} />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={"CarouselScreen"}
            component={CarouselScreen}
          />
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={"PollResult"}
            component={PollResult}
          />
          <Stack.Screen
            name={"CreatePollScreen"}
            component={CreatePollScreen}
          />
          <Stack.Screen
            options={{ headerShown: false }}
            name={"ImageCropScreen"}
            component={ImageCropScreen}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
}

export default CommunityScreen;
```

### Step 7: Overriding of Callbacks

You can also override few exposed callbacks with custom logic as below:

```tsx
import {
  LMChatCallbacks,
  LMChatroomCallbacks,
  NavigateToProfileParams,
  NavigateToGroupDetailsParams,
} from "@likeminds.community/chat-rn-core";

// Override callBacks with custom logic
class CustomCallbacks implements LMChatCallbacks, LMChatroomCallbacks {
  navigateToProfile(params: NavigateToProfileParams) {
    // Override navigateToProfile with custom logic
  }

  navigateToHomePage() {
    // Override navigateToHomePage with custom logic
  }

  onEventTriggered(eventName: string, eventProperties?: Map<string, string>) {
    // Override onEventTriggered with custom logic
  }

  navigateToGroupDetails(params: NavigateToGroupDetailsParams) {
    // Override navigateToGroupDetails with custom logic
  }
}

// Creation of object for above overrided class
const lmChatInterface = new CustomCallbacks();
```

Pass in the `lmChatInterface` object created to `LMOverlayProvider` as well.

```tsx
return (
  <LMOverlayProvider
    lmChatClient={lmChatClient}
    userName={userName}
    userUniqueId={userUniqueId}
    profileImageUrl={profileImageUrl}
    lmChatInterface={lmChatInterface} // add this line in LMOverlayProvider props
  >
    {/* Add navigation container */}
  </LMOverlayProvider>
);
```

### Step 8: Customisations

You can customise the components and screens as well by overriding the setting the styles as below:

```tsx
import { STYLES } from "@likeminds.community/chat-rn-core";

function CommunityScreen(): React.JSX.Element {
  const themeStyles = {
    hue: 10,
    fontColor: "black",
    primaryColor: "green",
    secondaryColor: "green",
    lightBackgroundColor: "#d7f7ed",
  };

  if (themeStyles) {
    STYLES.setTheme(themeStyles);
  }

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
  };

  if (chatroomHeaderStyles) {
    STYLES.setChatroomHeaderStyle(chatroomHeaderStyles);
  }

  return(
    // return code as above
  )
}

export default CommunityScreen;
```

In this way, we can override all other customsations available listed in [MessageInputBox](../Widgets/Components/input_box.md), [Message](../Widgets/Components/message.md) and [ReactionList](../Widgets/Components/reaction_list.md) section inside Components in Widgets.
