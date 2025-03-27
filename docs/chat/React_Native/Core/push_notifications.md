---
sidebar_position: 5
title: Push Notifications
---

# Push Notifications

Push notifications are a powerful way to engage with your users and keep them informed about important updates and events within your React Native application. By integrating push notification functionality into your app using the React Native SDK, you can send targeted and personalized messages directly to your users' devices, even when your app is not actively running.

By following the step-by-step instructions in this guide and leveraging the capabilities of the React Native SDK, you will be able to seamlessly integrate push notifications into your React Native application and unlock the full potential of real-time communication with your users.

Let's get started with implementing push notification functionality in your React Native app!

## Set up the Firebase Server key

Update Firebase Server Key on the LikeMinds dashboard. You can find a detailed tutorial [here](/docs/notification.md).

## Set up notifications in your React Native project.

This is some boilerplate code example using some common React Native libraries to get information for the device, setup notifications, accessing token and managing permissions. It is upto you how you want to implement it and send the data. We require the `xDeviceId`, `xPlatformCode` and `token` to register the device with LikeMinds. You need these two values to receive notifications from LikeMinds.

1. Setup notications in your React Native project, below code is given for your reference.

In order to retrieve the device ID using the `getUniqueId` method, we utilize the `react-native-device-info` library. Alternatively, there are various other libraries available that can be employed to obtain the device ID in your preferred manner.

```tsx
/// Setup notifications
const pushAPI = async (fcmToken: string, accessToken: string) => {
  const deviceID = await getUniqueId();
  try {
    const payload = {
      token: fcmToken,
      xDeviceId: deviceID,
      xPlatformCode: Platform.OS === "ios" ? "ios" : "an",
    };
    await lmChatClient?.registerDevice(payload);
  } catch (error) {
    Alert.alert(`${error}`);
  }
};
```

You can use this code snippet below which uses the `firebase_messaging` plugin to get the FCM token, and initialize messaging instance.

```tsx
// Setup Firebase messaging on your app, to work with LikeMinds notifications
async function requestUserPermission() {
  const authStatus = await messaging().requestPermission();
  const enabled =
    authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    authStatus === messaging.AuthorizationStatus.PROVISIONAL;
  return enabled;
}

// Get the token only when permission is granted
const fetchFCMToken = async () => {
  const fcmToken = await messaging().getToken();
  return fcmToken;
};
```

2. Call the above function in your `App.tsx || App.js` file before running your React Native application

```tsx
function App() {
  useEffect(() => {
    const token = async () => {
      const isPermissionEnabled = await requestUserPermission();
      if (isPermissionEnabled) {
        let fcmToken = await fetchFCMToken();
        if (!!fcmToken) {
          setFCMToken(fcmToken);
        }
      }
    };
    token();
  }, []);

  useEffect(() => {
    if (FCMToken && accessToken) {
      pushAPI(FCMToken, accessToken);
    }
  }, [FCMToken, accessToken]);

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
```

:::note
If you don't already have `setBackgroundMessageHandler`, navigate to the `setup.ts` file present `@likeminds.community/chat-rn-core` dependency and uncomment the `messaging().setBackgroundMessageHandler` method
:::
