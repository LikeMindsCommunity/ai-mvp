---
sidebar_position: 1
title: Validate User
slug: /react-native/data/user/validate-user
---

# Validate User

The `validateUser` method is an asynchronous function responsible for validating a user based on the provided ValidateUser request object.

## Steps to validate a User

1. To validate a user, use the method `validateUser()` provided by the `lmChatClient` you created.
2. Pass the required `refreshToken` and `accessToken` to the function.
3. Use the response as per your requirement

```tsx
const payload: any = {
  refreshToken: "ENTER_REFRESH_TOKEN",
  accessToken: "ENTER_ACCESS_TOKEN",
};
const response = await lmChatClient?.validateUser(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

#### Validate User Payload

List of parameters provided by `validateUser()`

| Variable       | Type   | Description                   |
| -------------- | ------ | ----------------------------- |
| `refreshToken` | string | Refresh token for the session |
| `accessToken`  | string | Access token for the session  |

#### Validate User Response

List of parameters for the response

| Variable       | Type                                | Description                                |
| -------------- | ----------------------------------- | ------------------------------------------ |
| community      | [Community](../Models/community.md) | Community object                           |
| accessToken    | string                              | Access token for authentication            |
| refreshToken   | string                              | Refresh token for authentication           |
| user           | User                                | User object                                |
| appAccess      | boolean                             | Indicates if the app access is granted     |
| hasAnswers     | boolean                             | Indicates if the user has provided answers |
| logoutResponse | `LMResponse<Nothing>`               | Response object for logout action          |
