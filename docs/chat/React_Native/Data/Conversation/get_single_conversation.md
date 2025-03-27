---
sidebar_position: 2
title: Get Single Conversation
slug: /react-native/data/conversation/get-single-conversation
---

# Get Conversation

LikeMinds React Native Chat SDK offers this feature which enables you to access and analyze individual conversations, empowering you to implement customized functionalities or perform specific operations within your chat application.

## Steps to Get a Single Conversation

1. Create a `syncConversationRequest` object using `SyncConversationRequest.builder` class by passing all the required parameters.
2. Call `syncConversation()` function using the instance of `lmChatClient`.
3. Process the response `LMResponse<SyncConversationResponse>` as per your requirement.

```ts
const syncConversationRequest = SyncConversationRequest.builder()
  .setChatroomId("ENTER_CHATROOM_ID")
  .setPage("ENTER_REQURIED_PAGE_NO")
  .setMinTimestamp("ENTER_MIN_TIMESTAMP")
  .setMaxTimestamp(Date.now())
  .setPageSize("ENTER_PAGE_SIZE")
  .setConversationId("ENTER_CONVERSATION_ID")
  .build();
const repsonse = lmChatClient?.syncConversation(syncConversationRequest);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Sync Conversation Payload

List of parameters provided by `syncConversation()`.

| Variable         | Type    | Description                                                | Optional |
| ---------------- | ------- | ---------------------------------------------------------- | -------- |
| `chatroomId`     | number  | chatroom Id                                                |          |
| `conversationId` | number? | conversation id for which you want to get the conversation |          |
| `page`           | number  | page number                                                |          |
| `pageSize`       | number  | page size for paginated response                           |          |
| `maxTimestamp`   | number  | maximum timestamp                                          |          |
| `minTimestamp`   | number  | minimum timestamp                                          |          |

### Sync Conversation Response

List of parameters in the response.

| Variable | Type | Description | Optional |
| -------- | ---- | ----------- | -------- |

| `userMeta` | Member | User data | |
| `conversationMeta` | [Conversation](../Models/conversation) | Conversation data | |
| `conversationData` | [Conversation](../Models/conversation)[] | List of conversations | |
| `communityMeta` | [Community](../Models/community) | Community data | |
| `chatroomsMeta` | [Chatroom](../Models/chatroom) | Chatroom data | |
| `chatroomReactionsMeta` | [ReactionMeta](../Models/conversation/#reactions)[] | List of reactions | |
| `convReactionsMeta` | [ReactionMeta](../Models/conversation/#reactions)[] | List of reactions | |
| `convAttachmentsMeta` | [Attachment](../Models/attachments)[] | List of attachments | |
| `convPollsMeta` | [Poll](../Models/conversation/#polls)[] | List of Polls | |
