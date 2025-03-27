---
sidebar_position: 12
title: Report Screen
slug: /react-native/core/screens/report-screen
---

## Overview

The `ReportMessage` screen allows users to report inappropriate or harmful messages within the LikeMinds chat application. It provides a straightforward interface for users to select a reason for the report and submit their concerns, ensuring that the platform maintains a safe and respectful environment. This feature empowers users to take action against misconduct and helps moderators manage content effectively.

<img
src={require('../../../../static/img/reactNative/lmReportScreen.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Data Variables

- `conversationId`: Id of the conversation to be reported.
- `reason`: Reporting reason.

## Props

| Property           | Type      | Description                                                      | Default | Required           |
| ------------------ | --------- | ---------------------------------------------------------------- | ------- | ------------------ |
| `conversationID`   | `string`  | Unique identifier for the conversation.                          |         | :heavy_check_mark: |
| `isDM`             | `boolean` | Indicates if the conversation is a direct message (DM).          | `false` |                    |
| `chatroomID`       | `string`  | Unique identifier for the chatroom.                              |         | :heavy_check_mark: |
| `selectedMessages` | `any[]`   | Array containing messages that have been selected for reporting. |         |                    |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `ReportScreen` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import { REPORT, ReportScreen, Themes } from "@likeminds.community/chat-rn-core";
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
      theme={<"SDK_THEME">} // // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={REPORT}
            component={ReportScreen}
            initialParams={{
              conversationID: "ENTER_CONVERSATION_ID",
              isDM: false,
              chatroomID: "ENTER_CHATROOM_ID",
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
