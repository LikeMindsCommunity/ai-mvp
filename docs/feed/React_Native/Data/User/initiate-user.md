---
sidebar_position: 1
title: Initiate User
slug: /react-native/data/user/initiate-user
---

# Initiate User

To start using the LikeMinds Feed and enable personalized experiences for your users, you need to initate them within the system. This process associates a user in your application with a user in the LikeMinds Feed, allowing for seamless integration and personalized recommendations.

## Steps to Initiate an User

1. Use the `initiateUser()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `InitiateUserRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const initiateUserRequest = InitiateUserRequest.builder()
    .setUserName("ENTER_USER_NAME")
    .setUUID("ENTER_UUID")
    .setApiKey("ENTER_API_KEY")
    .setImageUrl("ENTER_USER_PROFILE_IMAGE_URL")
    .setIsGuest("ENTER_IS_GUEST")
    .build();
  const response = await lmFeedClient.initiateUser(initiateUserRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::tip
We suggest that you use the unique ID from your database for the user so that you do not have to save the one we generate.
:::

## Models

### InitiateUserRequest

| Variable   | Type    | Description                 | Optional |
| ---------- | ------- | --------------------------- | -------- |
| `userName` | string  | User's name                 |          |
| `uuid`     | string  | User's UUID                 |          |
| `isGuest`  | boolean | If the User is a guest user |          |
| `apikey`   | string  | API Key of the community    |          |
| `imageUrl` | string  | Profile Image URL of user   |    ✔     |

### InitiateUserResponse

| Variable       | Type                                             | Description    | Optional |
| -------------- | ------------------------------------------------ | -------------- | -------- |
| `accessToken`  | string                                           | Access Token   |          |
| `refreshToken` | string                                           | Refresh Token  |          |
| `user`         | [User](../Models/user-model.md)                  | User data      |          |
| `community`    | [Community](../User/initiate-user.md/#community) | Community info |          |
| `appAccess`    | boolean                                          | App access     |          |

### Community

| Variable       | Type   | Description               | Optional |
| -------------- | ------ | ------------------------- | -------- |
| `id`           | string | Community Id              |          |
| `name`         | string | Community Name            |          |
| `imageUrl`     | string | Community Image url       |          |
| `membersCount` | int    | Community Member's count  |          |
| `updatedAt`    | int    | Community last updated at |          |
