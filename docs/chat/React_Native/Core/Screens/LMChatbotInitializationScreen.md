---
sidebar_position: 13
title: Chatbot Initialization Screen
slug: /react-native/core/screens/LMChatbot-Initialization-Screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `LMChatbotInitializationScreen` component(Screen) acts as a splash screen while a chatroom with a user and AI Chatbot is being initialized and created.

<img
src={require('../../../../static/img/reactNative/AIChatbotInit.webp').default}
alt="LMChatbotInitializationScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%' }}
/>

## Styling Customizations


| Property               | Type        | Description                                     |
| ---------------------- | ------------| ----------------------------------------------- |
| `previewTextStyle`     | `TextStyle` | Styling for the preview text.                   |    
| `parentViewStyle`      | `ViewStyle` | Styling for the parent/root `<View>`.           |



## Props

| Property               | Type                  | Description                                     | Optional           |
| ---------------------- | --------------------- | ----------------------------------------------- | ------------------ |
| `navigation`           | `StackNavigationProp` | The navigation prop for stack-based navigation. |                    |
| `route`                | `RouteProp`           | The route object provided by the navigator.     |                    |
| `animationToShowPath`  | `Object`              | The object specifying the animation path.       | :heavy_check_mark: |
| `previewText`          | `string`              | The preview text to display.                    | :heavy_check_mark: |
| `animationToShowUrl`   | `string`              | The URL hosting lottie JSON file.               | :heavy_check_mark: |
| `lottieAnimationStyle` | `ViewStyle`           | The style for the Lottie animation.             | :heavy_check_mark: |



## Usage Example

### Step 1: Create a wrapper component
- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMChatBotOverlayProvider`.
- Create a wrapper component i.e `ChatbotInitScreenWrapper` for `LMChatbotInitializationScreen` imported from `@likeminds.community/chat-rn-core`.

```tsx title="ChatbotInitScreenWrapper.tsx"
import {
  LMChatbotInitializationScreen
} from "@likeminds.community/chat-rn-core";

function ChatbotInitScreenWrapper({ navigation, route }) {
  return (
    <LMChatbotInitializationScreen
      navigation={navigation}
      route={route}
      previewText="<YOUR_CUSTOM_PREVIEW_TEXT>"
      animationToShowPath={require("path/to/lottie/JSON")}
      lottieAnimationStyle={
        {
          // pass ViewStyle Object
        }
      }
    />
  );
}
```

### Step 2: Add the above created wrapper as a Stack Screen
- Add `ChatbotInitScreenWrapper` as a Stack screen in your `NavigationContainer`.
- Create `chatBotInitiateScreenStyles` and call the `setChatbotInitScreenStyle` to set the customisations related to styling.

```tsx title="App.tsx"
import {
  LMChatbotInitializationScreen
  STYLES,
  LMChatBotOverlayProvider
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import {
  CHATBOT_INITIATE_SCREEN
} from '@likeminds.community/chat-rn-core/ChatSX/constants/Screens';

export const App = () => {
  const Stack = createNativeStackNavigator();
  const chatBotInitiateScreenStyles = {
    previewTextStyle: {
        // Pass TextStyle Object
    },
    parentViewStyle: {
        // Pass ViewStyle Object
    },
  };

  if (chatBotInitiateScreenStyles) {
    STYLES.setChatbotInitScreenStyle(chatBotInitiateScreenStyles);
  }

  return (
    <LMChatBotOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={CHATBOT_INITIATE_SCREEN}
            component={ChatbotInitScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
