---
sidebar_position: 7
title: Set Topic Chatroom
slug: /react-native/data/chatroom/group-chat/set-chatroom-topic
---

# Set Topic Chatroom

With the LikeMinds ReactNative Chat SDK, you can enhance communication within a chatroom by utilizing the topic-setting feature. This functionality enables you to highlight a specific message, ensuring its prominence at the top of the chatroom screen. This not only facilitates easy readability but also provides a convenient navigation point for other users.

## Steps to set a chatroom topic

1. Create an object of the `SetChatroom` class using chatroom ID and the topic.
2. For setting a topic for a chatroom call `setChatroomTopic()` present in `LMChatClient` class using your request object.
3. Process the response (`LMResponse<Nothing>`) as per your requirement.

```ts
const payload = {
  chatroomId: "ENTER_CHATROOM_ID",
  conversationId: "ENTER_CONVERSATION_ID",
};

const conversation = {}; // selected conversation object, check conversation model for reference.
const response = await lmChatClient?.setChatroomTopic(payload, conversation);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

## Models

### Set Chatroom

List of parameters for the `SetChatroom` class

| Variable         | Type   | Description     | Optional |
| ---------------- | ------ | --------------- | -------- |
| `chatroomId`     | number | Chatroom Id     |          |
| `conversationId` | number | Conversation Id |          |

### Conversation

| Variable       | Type                                         | Description             |
| -------------- | -------------------------------------------- | ----------------------- |
| `conversation` | [Conversation](../../Models/conversation.md) | Details of Conversation |
