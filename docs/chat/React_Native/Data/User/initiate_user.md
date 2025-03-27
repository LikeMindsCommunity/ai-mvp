---
sidebar_position: 1
title: Initiate User
slug: /react-native/data/user/initiate-user
---

# Initiate User

To start using the LikeMinds Chat and enable personalized experiences for your users, you need to initiate them within the system. This process associates a user in your application with a user in the LikeMinds Chat, allowing for seamless integration and realtime messaging in your application.

## Steps to initiate a User

1. To initialise a user, use the method `initiateUser()` provided by the `LMChatClient` you created.
2. Pass the required `uuid` and `userName` to the function. An optional parameter `isGuest` to be provided if the logging profile is of the guest user.
3. Use the response as per your requirement

```tsx
const payload: any = {
  isGuest: false, // true for guest user
  uuid: "ENTER_USER_UUID",
  userName: "ENTER_USER_NAME",
};
const response = await lmChatClient?.initiateUser(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

#### Initiate User Payload

List of parameters provided by `initiateUser()`

| Variable   | Type    | Description            | Optional           |
| ---------- | ------- | ---------------------- | ------------------ |
| `uuid`     | string  | Unique ID for the user |                    |
| `userName` | string  | Name of the userName   |                    |
| `isGuest`  | boolean | Is the user a guest?   | :heavy_check_mark: |

#### Initiate User Response

List of parameters for the response

| Variable    | Type                             | Description       |
| ----------- | -------------------------------- | ----------------- |
| `community` | [Community](../Models/community) | Community details |
| `user`      | [Member](../Models/member.md)    | User details      |
