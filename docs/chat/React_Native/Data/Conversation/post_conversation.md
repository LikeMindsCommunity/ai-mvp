---
sidebar_position: 3
title: Post Conversation
slug: /react-native/data/conversation/post-conversation
---

# Post Conversation

LikeMinds React Native Chat SDK allows you to conveniently post a conversation in an existing chatroom by specifying the chatroom ID. This powerful feature enables you to contribute to ongoing discussions, share important information, or engage with other participants in real-time.

## Steps to Post a Conversation

1. To post a conversation, use the `postConversation()` method provided by the client you initialised.
2. Pass in the required parameter.
3. Process the response as per your requirement.

```ts
const payload: any = {
  text: "ENTER_MESSAGE",
  chatroomId: "ENTER_CHATROOM_ID",
  hasFiles: false, // true if the conversation inclued attachments
};
const response = await lmChatClient?.postConversation(payload);

if (response.success) {
  // your function to process the response data

  // to update message locally
  await myClient?.replaceSavedConversation(response?.conversation);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Post Conversation Payload

List of parameters provided by `postConversation()`

| Variable          | Type    | Description                               | Optional           |
| ----------------- | ------- | ----------------------------------------- | ------------------ |
| `chatroomId`      | number  | Chatroom Id                               |                    |
| `text`            | string  | Text to be posted                         |                    |
| `hasFiles`        | boolean | Whether the conversation has files        |                    |
| `attachmentCount` | number  | Number of attachments in the conversation | :heavy_check_mark: |

### Post Conversation Response

List of parameters in the response.

| Variable       | Type                                  | Description         |
| -------------- | ------------------------------------- | ------------------- |
| `conversation` | [Convesation](../Models/conversation) | Conversation object |
