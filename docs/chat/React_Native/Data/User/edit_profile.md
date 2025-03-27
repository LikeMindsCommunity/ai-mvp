---
sidebar_position: 2
title: Edit Profile
slug: /react-native/data/user/edit-profile
---

# Edit Profile

The Edit Profile method empowers users to modify their profile information seamlessly. With this function, users can update their user name, profile picture and other details.

## Editing a profile

1. For an user to leave a community, use the `editProfile()` method of the client you initialised.
2. Pass in the required parameter which are `userUniqueId`, `userName` and `imageUrl`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  uuid: "ENTER_UUID",
  userName: "ENTER_USER_NAME",
  imageUrl: "ENTER_PROFILE_IMAGE_URL",
};

const response = await lmChatClient.editProfile(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Edit Profile Payload

List of parameters supported.

| Variable       | Type   | Description       | Optional           |
| -------------- | ------ | ----------------- | ------------------ |
| `userUniqueId` | string | uuid of user      | :heavy_check_mark: |
| `userName`     | string | user name of user | :heavy_check_mark: |
| `imageUrl`     | string | image url of user |                    |
