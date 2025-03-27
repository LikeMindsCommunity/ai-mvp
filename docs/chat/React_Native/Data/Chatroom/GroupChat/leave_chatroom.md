---
sidebar_position: 4
title: Leave Chatroom
slug: /react-native/data/chatroom/group-chat/leave-chatroom
---

# Leave Chatroom

Leaving a chatroom with LM React Native Chat SDK allows you to exit a chatroom that you no longer want to be a part of.

## Steps to Leave a Open Chatroom

1. To leave a chatroom, use the method `followChatroom()`.
2. Pass in the required parameters `collabcardId`, `uuid` and `value`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
// To leave a chatroom, set the value to false
const payload: any = {
  collabcardId: "ENTER_CHATROOM_ID",
  value: true,
};
const response = await lmChatClient?.followChatroom(payload);

if (response.success) {
  // Update followStatus to false in local db as well
  await lmChatClient?.updateChatroomFollowStatus(chatroomId, false);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Leave Chatroom Payload

List of parameters for the `followChatroom()` method.

| Variable       | Type    | Description  | Optional |
| -------------- | ------- | ------------ | -------- | ------------------ |
| `collabcardId` | number  | Chatroom Id  |          |                    |
| `uuid`         | string  | Member Uuid  |          | :heavy_check_mark: |
| `value`        | boolean | Follow value |          |                    |

## Steps to Leave a Secret Chatroom

1. To leave a secret chatroom use the method `leaveSecretChatroom()`.
2. pass in the required parameter `chatroomId` and `isSecret`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  isSecret: true,
};
const response = await lmChatClient?.leaveSecretChatroom(payload);

if (response.success) {
  // Update followStatus to false in local db as well
  await lmChatClient?.updateChatroomFollowStatus(chatroomId, false);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Leave Secret Chatroom Payload

List of parameters for the function `leaveSecretChatroom`.

| Variable     | Type    | Description                            | Optional           |
| ------------ | ------- | -------------------------------------- | ------------------ |
| `chatroomId` | number  | Chatroom Id                            |                    |
| `isSecret`   | boolean | Set to true in case of secret chatroom | :heavy_check_mark: |
