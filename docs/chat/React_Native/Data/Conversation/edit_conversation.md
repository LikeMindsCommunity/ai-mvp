---
sidebar_position: 4
title: Edit Conversation
slug: /react-native/data/conversation/edit-conversation
---

# Edit Conversation

Editing a conversation means that you can change the text content of specified conversation corresponding to a unique conversation ID.

## Steps to edit a conversation

1. For editing a conversation call `editConversation()` method provided by the client you initialised.
2. Process the response as per your requirement.

```ts
const payload: any = {
  conversationId: "ENTER_CONVERSATION_ID",
  text: "ENTER_EDITED_TEXT",
};

const response = await lmChatClient?.editConversation(payload);

if (response.success) {
  // your function to process the response data

  const conversationId = response?.data?.conversation?.id;

  // to update message locally
  await lmChatClient?.updateConversation(
    conversationId.toString(),
    response?.data?.conversation
  );
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Edit Conversation Payload

List of parameters provided by `editConversation()`.

| Variable         | Type   | Description     | Optional |
| ---------------- | ------ | --------------- | -------- |
| `conversationId` | number | Conversation Id |          |
| `text`           | string | Text content    |          |

### Edit Conversation Response

List of parameters in the response.

| Variable       | Type                                   | Description         |
| -------------- | -------------------------------------- | ------------------- |
| `conversation` | [Conversation](../Models/conversation) | Edited conversation |
