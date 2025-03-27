---
sidebar_position: 11
title: Secret Chatroom Invite
slug: /react-native/data/chatroom/group-chat/secret-chatroom-invite
---

# Secret Chatroom Invite

LikeMinds React Native Chat SDK offers a convenient feature for sending secret chatroom invites. It allows you to send invites to a specific user within a group chat.

## Steps to send Secret Chatroom Invite to a participant

1. Send Invite to selected members using `sendInvites()` method.
2. Pass the required parameters `chatroomId`, `isSecret` and `chatroomParticipants`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  isSecret: true,
  chatroomParticipants: ["ENTER_LIST_OF_IDs_OF_PARTICIPANTS"],
};
const response = await myClient?.sendInvites(payload);

if (response.success) {
  // your function to process the response data
  processResponse();
} else {
  // your function to process error message
  processError(response);
}
```

### Secret Chatroom Invite Payload

List of parameters for the `sendInvites()` function.

| Variable               | Type    | Description                  | Optional |
| ---------------------- | ------- | ---------------------------- | -------- |
| `chatroomId`           | number  | Chatroom Id                  |          |
| `isSecret`             | boolean | true if chatroom is secret   |          |
| `chatroomParticipants` | array   | List the IDs of participants |          |
