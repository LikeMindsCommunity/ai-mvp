---
sidebar_position: 5
title: Mark Read Chatroom
slug: /react-native/data/chatroom/group-chat/mark-read-chatroom
---

# Mark Read Chatroom

In LikeMinds React Native Chat SDK, you have the ability to mark conversations within a chatroom as read. This feature enables you to keep track of your chatroom discussions and easily identify which messages have been viewed or not.

## Steps to Mark a Chatroom as Read

1. To mark a chatroom as read, use the method `markReadChatroom()`.
2. Pass in the required parameter `chatroomId`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
};
const response = await lmChatClient?.markReadChatroom(payload);
if (response.success) {
  // Update unseenCount in local db as well
  await lmChatClient?.updateUnseenCount(chatroomId);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Mark Read Chatroom Payload

List of parameters for the `markReadChatroom()` method.

| Variable     | Type   | Description | Optional |
| ------------ | ------ | ----------- | -------- |
| `chatroomId` | number | Chatroom Id |          |
