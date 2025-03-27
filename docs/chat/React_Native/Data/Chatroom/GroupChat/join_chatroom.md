---
sidebar_position: 3
title: Join Chatroom
slug: /react-native/data/chatroom/group-chat/join-chatroom
---

# Join Chatroom

Joining a chatroom with LikeMinds React Native Chat SDK allows you to receive all the conversations happening within that chatroom.Experience real-time engagement and never miss out on any important conversations by joining the chatroom using LikeMinds React Native Chat SDK.

## Steps to Join a chatroom

1. To join a chatroom use the method `followChatroom()`.
2. Pass in the required parameters `chatroomId`, `uuid` and `value`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
// To leave a chatroom, set the value to false
const payload: any = {
  collabcardId: "ENTER_CHATROOM_ID",
  value: true,
};
const response = await lmChatClient?.followChatroom(payload);

if (response.success) {
  // Update followStatus to true in local db as well
  await lmChatClient?.updateChatroomFollowStatus(chatroomId, true);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Join Chatroom Payload

List of parameters for the `followChatroom()` method.

| Variable       | Type    | Description  | Optional |                    |
| -------------- | ------- | ------------ | -------- | ------------------ |
| `collabcardId` | number  | Chatroom Id  |          |                    |
| `uuid`         | string  | Member Uuid  |          | :heavy_check_mark: |
| `value`        | boolean | Follow value |          |                    |
