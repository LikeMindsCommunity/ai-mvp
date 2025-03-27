---
sidebar_position: 3
title: Logout User
slug: /react-native/data/user/logout-user
---

# Logout User

To disconnect a user (say that you’re for instance logging out and logging in as someone new) you can call the `logout()` method present in `LMChatClient` class.

## Logging out

1. For an user to logout, use the `logout()` method of the client you initialised.
2. Pass in the `refreshToken` which is a required parameter.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  refreshToken: "ENTER_REFRESH_TOKEN",
  deviceID: "ENTER_DEVICE_ID",
};

const response = await lmChatClient.logout(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Logout User Payload

List of parameters supported.

| Variable       | Type   | Description                    | Optional |
| -------------- | ------ | ------------------------------ | -------- |
| `refreshToken` | string | RefreshToken of user logged in |          |
| `deviceID`     | string | Id of the device               |          |
