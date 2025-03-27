---
sidebar_position: 2
title: Get Chatroom Actions
slug: /react-native/data/chatroom/group-chat/get-chatroom-actions
---

# Get Chatroom Actions

These diverse chatroom types cater to various communication needs, providing flexibility and control over the conversations within your React Native chat application. A chatroom can be created by the community manager through Dashboard only.

Chatroom Actions returns the actions allowed in the chatroom like `Mute/Unmute`, `Join/Unjoin`, `ShareChatroom` and `ViewParticipants` along with total number of participants.

## Fetch chatroom actions

1. To fetch the chatroom, use the `getChatroomActions()` method of the client you initialised.
2. Pass in the required parameter `chatroomId`.
3. Process the response as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
};
const response = await lmChatClient?.getChatroomActions(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Chatroom Request

List of parameters supported.

| Variable     | Type   | Description | Optional |
| ------------ | ------ | ----------- | -------- |
| `chatroomId` | number | Chatroom Id |          |

### Get Chatroom Response

List of parameters returned in the response

| Variable                  | Type                                                         | Description                                 | Optional |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------- | -------- |
| accessWithoutSubscription | boolean                                                      | Boolean to access without subscription      |          |
| canAccessSecretChatroom   | boolean                                                      | Boolean to check access for secret chatroom |          |
| chatroomActions           | [ChatroomActions[]](../Models/chatroom.md/#chatroom-actions) | Array of chatroom actions                   |          |
| participantCount          | number                                                       | Total number of participants in a chatroom  |          |
