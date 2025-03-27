---
sidebar_position: 7
title: Notification Feed
slug: /react-native/core/screens/notification-feed-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `LMFeedNotificationFeedScreen` is designed to present a list of notifications to the user. Users can pull to refresh the list of notifications, and the screen shows an empty state view when there are no notifications to display. It supports navigating to different parts of the app based on the notification's content.

<img
src={require('../../../../static/img/iOS/screens/notification.webp').default}
alt="LMFeedNotificationScreen"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="30%"
/>

## UI Components

- [LMNotificationFeedItem](../Components/LMFeedNotificationItem.md)
- [LMFeedLoader](../Components/Fundamentals/LMFeedLoader.md)
- [LMFeedText](../Components/Fundamentals/LMFeedText.md)

## Data Variables

- `notifications`: Stores the feed data conforming to [`LMActivityViewData[]`](../Models/LMActivityViewData.md).

## Callbacks

- `onNotificationItemClickedProp`: Triggered when a notification item is clicked. Provides the [`LMActivityViewData`](../Models/LMActivityViewData.md) notification object.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in `notificationFeedStyle` in `STYLES`.

## Customization Table

| Property                       | Type                                                      | Description                                                  |
| ------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------ |
| `screenHeader`                 | [`LMHeaderProps`](../Components/LMFeedHeader.md)          | Customizes the screen header.                                |
| `backgroundColor`              | `string`                                                  | Sets the background color of the screen.                     |
| `unreadBackgroundColor`        | `string`                                                  | Background color for unread notifications.                   |
| `activityTextStyles`           | `TextStyle`                                               | Styles for the activity text.                                |
| `timestampTextStyles`          | `TextStyle`                                               | Styles for the timestamp text.                               |
| `userImageStyles`              | [`UserImageStyles`](#userimagestyles-table)               | Styles for the user image, including fallback and size.      |
| `activityAttachmentImageStyle` | [`LMIconProps`](../Components/Fundamentals/LMFeedIcon.md) | Styles for the activity attachment image.                    |
| `noActivityViewText`           | `string`                                                  | Text to display when there are no activities.                |
| `noActivityViewTextStyle`      | `TextStyle`                                               | Styles for the text displayed when there are no activities.  |
| `noActivityViewImage`          | `React.ReactNode`                                         | Image to display when there are no activities.               |
| `noActivityViewImageStyle`     | `ImageStyle`                                              | Styles for the image displayed when there are no activities. |
| `customScreenHeader`           | `React.ReactNode`                                         | Custom component to replace the default screen header.       |
| `activityTextComponent`        | `Function`                                                | Custom component for rendering activity text.                |

### UserImageStyles Table

| Property               | Type         | Description                                                |
| ---------------------- | ------------ | ---------------------------------------------------------- |
| `fallbackTextStyle`    | `TextStyle`  | Styles for fallback text if the image fails to load.       |
| `size`                 | `number`     | Size of the user image.                                    |
| `onTap`                | `Function`   | Callback function triggered when the user image is tapped. |
| `fallbackTextBoxStyle` | `ViewStyle`  | Styles for the fallback text box.                          |
| `profilePictureStyle`  | `ImageStyle` | Styles for the user profile picture.                       |

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `NotificationScreenWrapper` file which will wrap the `NotificationScreen` within the `NotificationFeedContextProvider` so that the callbacks becomes accessible inside of the `NotificationScreen`.
- Create `notificationFeedStyles` for customisation and call the `setNotificationFeedStyles` to set the customisation.

<Tabs>
<TabItem value="NotificationScreen" label="NotificationScreen">

```tsx
import {
  LMFeedNotificationFeedScreen,
  useNotificationFeedContext,
} from "@likeminds.community/feed-rn-core";

const NotificationScreen = () => {
  const { handleActivityOnTap, handleScreenBackPress } =
    useNotificationFeedContext();

  // customised handleActivityOnTap callback
  const customNotificationOnTap = (activity) => {
    console.log("do something before notification tap", activity);
    handleActivityOnTap(activity);
    console.log("do something after notification tap");
  };

  const notificationFeedStyles = {
    backgroundColor: "green",
    unreadBackgroundColor: "red",
  };

  // notification feed screen customisation
  if (notificationFeedStyles) {
    STYLES.setNotificationFeedStyles(notificationFeedStyles);
  }

  return (
    <LMFeedNotificationFeedScreen
      onNotificationItemClickedProp={(activity) =>
        customNotificationOnTap(activity)
      }
    />
  );
};

export default NotificationScreen;
```

</TabItem>
<TabItem value="NotificationScreenWrapper" label="NotificationScreenWrapper">

```tsx
import { NotificationFeedContextProvider } from "@likeminds.community/feed-rn-core";
import NotificationScreen from "<<path_to_NotificationScreen.tsx>>";

const NotificationScreenWrapper = ({ navigation, route }) => {
  return (
    <NotificationFeedContextProvider navigation={navigation} route={route}>
      <NotificationScreen />
    </NotificationFeedContextProvider>
  );
};

export default NotificationScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator`in the`NavigationContainer`wrapped by `LMOverlayProvider`.
- Add `NotificationScreenWrapper` as a Stack screen in your `NavigationContainer`.

```ts
import {
  NOTIFICATION_FEED,
  LMOverlayProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";
import NotificationScreenWrapper from "<<path_to_NotificationScreenWrapper.tsx>>";
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
            name={NOTIFICATION_FEED}
            component={NotificationScreenWrapper}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
