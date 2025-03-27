---
sidebar_position: 6
title: Tag Member in Conversation
slug: /react-native/data/conversation/tag-member
---

# Tag Member in Conversation

LikeMinds React Native Chat SDK provides the convenient Tag Member feature, allowing you to tag members participating in a conversation. This feature enables efficient categorization and organization of members based on specific criteria or characteristics, enhancing communication and facilitating targeted interactions within the chat platform.

## Steps to tag member in a conversation

1. To get the list of members which can be tagged in a chatroom, call `getTaggingList()` provided by the client you initialised.
2. Process the response as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  page: "ENTER_REQUIRED_PAGE",
  pageSize: "ENTER+PAGE_SIZE",
  searchName: "ENTER_SEARCH_STRING",
};
const response = await lmChatClient?.getTaggingList(payload);
if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Get Tagging List Payload

List of parameters provided by the `getTaggingList()`

| Variable     | Type   | Description   | Optional |
| ------------ | ------ | ------------- | -------- |
| `chatroomId` | number | Chatroom Id   |          |
| `page`       | number | Page int      |          |
| `pageSize`   | number | Page size     |          |
| `searchName` | string | Search string |          |

### Get Tagging List Response

List of parameters in the response.

| Variable                | Type   | Description                                                                                |
| ----------------------- | ------ | ------------------------------------------------------------------------------------------ |
| `group_tags`            | object | List of groups tags that are available, these tags are available to Community Manager only |
| `community_members`     | object | List of member in that community, used in open chatroom                                    |
| `chatroom_participants` | object | List of chatroom_participants, used in secret chatroom                                     |
