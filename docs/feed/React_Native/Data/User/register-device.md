---
sidebar_position: 3
title: Register Device
slug: /react-native/data/user/register-device
---

The `registerDevice()` function is used to register User Device for Push Notifications.

## Steps to Register User Device

1. Use the `registerDevice()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `RegisterDeviceRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const RegisterDeviceRequest = RegisterDeviceRequest.builder()
    .setDeviceId("<ENTER_DEVICE_ID>") // unique id of the device
    .setToken("<ENTER_TOKEN>") // FCM Token
    .build();
  const response = await lmFeedClient.registerDevice(RegisterDeviceRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### RegisterDeviceRequest

| Variable   | Type   | Description  | Optional |
| ---------- | ------ | ------------ | -------- |
| `token`    | string | Unique token |          |
| `deviceId` | string | Device Id    |          |
