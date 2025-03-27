---
sidebar_position: 1
title: Get Conversations
slug: /react-native/data/conversation/get-conversation
---

# Get Conversations

Simplify your chat application development with LikeMinds React Native Chat SDK. Enhance user conversations, enable real-time messaging, and provide seamless communication experiences with minimal coding effort. By utilizing this feature you can view all the conversations in the chatroom.

## Steps to fetch Conversations inside a Chatroom

1. Call `getConversations()` function using the instance of lmChatClient.
2. Process the response as per your requirement.

```ts
const getConversationsRequest = GetConversationsRequestBuilder.builder()
  .setChatroomId("ENTER_CHATROOM_ID")
  .setLimit("ENTER_PAGE_SIZE")
  .build();
const repsonse = lmChatClient?.getConversations(getConversationsRequest);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### GetConversationsRequest

| Variable           | Type                                          | Description                                      | Optional |
| ------------------ | --------------------------------------------- | ------------------------------------------------ | -------- |
| chatroomId         | string                                        | ID of the chatroom                               |          |
| limit              | number                                        | Maximum number of conversations to fetch         |          |
| medianConversation | [Conversation](../Models/conversation.md)     | Median conversation for pagination               | ✔️       |
| type               | [GetConversationsType](#getconversationstype) | Enum containing type of conversation to retrieve | ✔️       |

### GetConversationsType

| Enum Value | Description                                         |
| ---------- | --------------------------------------------------- |
| ALL        | Fetches all conversations                           |
| ABOVE      | Fetches conversations above the median conversation |
| BELOW      | Fetches conversations below the median conversation |
