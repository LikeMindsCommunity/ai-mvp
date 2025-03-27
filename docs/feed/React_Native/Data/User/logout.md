---
sidebar_position: 4
title: Logout
slug: /react-native/data/user/logout
---

To disconnect a user (for example you want to switch user profile or logout the user) you can call the `logoutUser()` method.

## Steps to logout User

1. Use the `logoutUser()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `LogoutUserRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const logoutRequest = {
    deviceId: "<ENTER_DEVICE_ID>", // add deviceId only if you have register device id using registerDevice method
  };
  const response = await lmFeedClient.logoutUser(logoutRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### LogoutUserRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**          | **OPTIONAL** |
| :----------- | :------- | :----------------------- | :----------: |
| `deviceId`   | string   | Unique id of the device. |      ✔       |
