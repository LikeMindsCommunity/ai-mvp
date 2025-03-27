---
sidebar_position: 8
title: Put Reaction
slug: /react-native/data/conversation/put-reaction
---

# Put Reaction

Reactions are used to add context to a message, such as by indicating that the user agree or disagree with something that was said. You can integrate reactions to react to chat messages and enable your users to react to these messages by following the given steps

## Steps to Put Reaction from a Conversation

1. To post a conversation, use the `putReaction()` method provided by the client you initialised.
2. Pass the required parameters `conversationId` and `reaction`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload = {
  conversationId: "ENTER_CONVERSATION_ID"
  reaction: "ENTER_REACTIONS",
};

const response = await lmChatClient?.putReaction(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

## Models

### PutReactionRequest

List of parameters for the `PutReactionRequest` class

| Variable         | Type   | Description     | Optional           |
| ---------------- | ------ | --------------- | ------------------ |
| `chatroomId`     | number | Chatroom Id     | :heavy_check_mark: |
| `conversationId` | number | Conversation Id |                    |
| `reaction`       | string | Reaction        |                    |
