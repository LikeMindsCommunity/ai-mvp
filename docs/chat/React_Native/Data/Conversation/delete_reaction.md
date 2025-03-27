---
sidebar_position: 9
title: Delete Reaction
slug: /react-native/data/conversation/delete-reaction
---

# Delete Reaction

You can integrate "remove reaction" which enables your user to remove their reaction from already reacted chat messages. You can do so by following the given steps.

## Steps to Delete Reaction from a Conversation

1. To post a conversation, use the `deleteReaction()` method provided by the client you initialised.
2. Pass in the required parameter.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload = {
  chatroomId: "ENTER_CHATROOM_ID",
  conversationId: "ENTER_CONVERSATION_ID",
  reaction: "ENTER_REACTIONS",
};

const response = await lmChatClient?.deleteReaction(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

## Models

### Delete Reaction Request

List of parameters for the `DeleteReactionRequest` class

| Variable         | Type   | Description     | Optional |
| ---------------- | ------ | --------------- | -------- |
| `chatroomId`     | number | Chatroom Id     |          |
| `conversationId` | number | Conversation Id |          |
| `reaction`       | string | Reaction        |          |
