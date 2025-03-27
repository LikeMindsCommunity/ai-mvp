---
sidebar_position: 1
title: Get Chatroom
slug: /react-native/data/chatroom/group-chat/get-chatroom
---

# Get Chatroom

A chatroom is a place where users can interact with each other. LikeMinds React Native Chat SDK supports different types of chatrooms, including:

- Open chatrooms: Open to all users within the community, allowing for broad participation and discussions.
- Secret chatrooms: Highly secure and hidden, accessible only to invited members, ensuring utmost privacy and confidentiality.

These diverse chatroom types cater to various communication needs, providing flexibility and control over the conversations within your React Native chat application. A chatroom can be created by the community manager through Dashboard only.

## Fetch a single chatroom

1. To fetch the chatroom, use the `getChatroom()` method of the client you initialised.
2. Pass in the required parameter `chatroomId`.
3. Process the response as per your requirement.

```ts
const response = await lmChatClient.getChatroom(chatroomId: "ENTER_CHATROOM_ID").data;

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Get Chatroom Payload

List of parameters supported.

| Variable     | Type   | Description | Optional |
| ------------ | ------ | ----------- | -------- |
| `chatroomId` | number | Chatroom Id |          |

### Get Chatroom Response

List of parameters in the response.

| Variable   | Type                                 | Description         |
| ---------- | ------------------------------------ | ------------------- |
| `chatroom` | [Chatroom](../../Models/chatroom.md) | Details of chatroom |
