---
sidebar_position: 3
title: Block Member
slug: /react-native/data/chatroom/direct-messages/block-member
---

# Block Member

LikeMinds React Native Chat SDK includes `Block Member` functionality, which you to effectively manage your chat environment. With this feature, you can easily block specific members, ensuring a secure and comfortable Community Chat Experience

## Steps to block member

1. To block a member, use the method `blockMember()`.
2. Pass in the required parameters `chatroomId` and `status`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
// To unblock a member, set the status to 1
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  status: 0,
};
const response = await lmChatClient?.blockMember(payload);

if (response.success) {
  // Update state in local db as well, 0 for blocked and 1 for unblocked
  await lmChatClient?.updateChatRequestState(chatroomId, 0);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Block Member Payload

List of parameters for the `blockMember()` function.

| Variable     | Type   | Description | Optional |
| ------------ | ------ | ----------- | -------- |
| `chatroomId` | number | Chatroom Id |          |
| `status`     | number | Member Id   |          |
