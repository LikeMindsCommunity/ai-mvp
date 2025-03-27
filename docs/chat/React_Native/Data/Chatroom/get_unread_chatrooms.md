---
sidebar_position: 1
title: Get Unread Chatrooms
slug: /react-native/data/chatroom/group-chat/get-unread-chatrooms
---

# Get Unread Chatrooms

The `getUnreadChatrooms` function retrieves a list of unread chatrooms from the local database using Realm. It accepts a `Chatroom` and the `lastConversation` as input, updating or creating relevant records within the local database. If the chatroom exists, it updates the `unseenCount`, `unreadConversationsCount`, and conversation details. If the chatroom is not found, it creates new chatroom, conversation, and member records. The method filters chatrooms with active follow status, no mute status, and unseen messages, then sorts them by the latest conversation timestamp. It returns a maximum of 7 chatrooms wrapped in an `LMResponse`.

## Fetch a single chatroom

1. To fetch the unread chatrooms, use the `getUnreadChatrooms()` method of the `lmChatClient` you initialised.
2. Pass in the required parameter.
3. Process the response as per your requirement.

```ts
const payload = {
  chatroom: "ENTER_YOUR_CHATROOM_OBJECT",
  lastConversation: "ENTER_YOUR_LAST_CONVERSATION_OBJECT",
};
const response = await lmChatClient.getUnreadChatrooms(payload).data;

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Get Unread Chatroom Payload

List of parameters supported.

| Variable           | Type                                      | Description                             | Optional |
| ------------------ | ----------------------------------------- | --------------------------------------- | -------- |
| `chatroom`         | [Chatroom](../Models/chatroom.md)         | Information about the chatroom          |          |
| `lastConversation` | [Conversation](../Models/conversation.md) | Information about the last conversation |          |

### Get Unread Chatroom Response

List of parameters in the response.

| Variable   | Type                                 | Description         |
| ---------- | ------------------------------------ | ------------------- |
| `chatroom` | [Chatroom](../../Models/chatroom.md) | Details of chatroom |
