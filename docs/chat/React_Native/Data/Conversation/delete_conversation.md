---
sidebar_position: 5
title: Delete Conversation
slug: /react-native/data/conversation/delete-conversation
---

# Delete Conversation

Deleting a conversation means that you can delete the text content of specified conversation corresponding to a unique conversation ID.

## Steps to delete a conversation

1. To delete a conversation, use the method `deleteConversations()` provided by the client you initialised.
2. Pass in the required parameter `conversationIds` and `reason`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload = {
  conversationIds: [], // Pass in the id's of the conversation you want to delete.
  reason: "", // Pass in the reason to delete the conversation.
};
const response = await lmChatClient?.deleteConversations(payload);

if (response.success) {
  // your function to process the response data
  const conversationId: response?.data?.conversations?.id, // Pass in the id of the conversation you want to delete.
    user: {}, // Pass in logged uer info
    conversations: []; // Pass in the list of the conversations from which you want to delete the item.

  // to update message locally
  await lmChatClient?.deleteConversation(conversationId, user, conversations);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Delete Conversations Payload

List of parameters required by the `deleteConversations()` method.

| Variable          | Type     | Description                      | Optional |
| ----------------- | -------- | -------------------------------- | -------- |
| `conversationIds` | number[] | Conversations Ids                |          |
| `reason`          | string   | Reason for conversation deletion |          |
