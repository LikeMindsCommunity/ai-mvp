---
sidebar_position: 1
title: Validate User
slug: /react-native/data/user/validate-user
---

# Validate User

To start using the LikeMinds Feed and enable personalized experiences for your users, you need to validate them within the system. This process associates a user in your application with a user in the LikeMinds Feed, allowing for seamless integration and personalized recommendations.

## Steps to Validate an User

1. Use the `validateUser()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `ValidateUserRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const validateUserRequest = ValidateUserRequest.builder()
    .setAccessToken("ENTER_ACCESS_TOKEN")
    .setRefreshToken("ENTER_REFRESH_TOKEN")
    .build();
  const response = await lmFeedClient.validateUser(validateUserRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::tip
We suggest that you use the unique ID from your database for the user so that you do not have to save the one we generate.
:::

## Models

### ValidateUserRequest

| Variable       | Type   | Description   | Optional |
| -------------- | ------ | ------------- | -------- |
| `accessToken`  | string | Access Token  |          |
| `refreshToken` | string | Refresh Token |          |

### ValidateUserResponse

| Variable         | Type                                             | Description     | Optional |
| ---------------- | ------------------------------------------------ | --------------- | -------- |
| `user`           | [User](../Models/user-model.md)                  | User data       |          |
| `community`      | [Community](../User/validate-user.md/#community) | Community info  |          |
| `appAccess`      | boolean                                          | App access      |          |
| `logoutResponse` | [LMResponse](../Models/response-wrapper.md)      | Logout response | ✔        |

### Community

| Variable       | Type   | Description               | Optional |
| -------------- | ------ | ------------------------- | -------- |
| `id`           | string | Community Id              |          |
| `name`         | string | Community Name            |          |
| `imageUrl`     | string | Community Image url       |          |
| `membersCount` | int    | Community Member's count  |          |
| `updatedAt`    | int    | Community last updated at |          |
