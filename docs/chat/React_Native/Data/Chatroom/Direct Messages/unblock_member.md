---
sidebar_position: 4
title: Unblock Member
slug: /react-native/data/chatroom/direct-messages/unblock-member
---

# Unblock Member

LM React Native Chat SDK includes a robust `Unblock Member` functionality, empowering you to effectively manage your chat environment. With this feature, you can easily unblock blocked members, ensuring a secure and comfortable communication experience

## Steps to unblock member

1. To unblock a member, use the method `blockMember()`.
2. Pass in the required parameters `chatroomId` and `status`.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
// To block a member, set the status to 0
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  status: 1,
};
const response = await lmChatClient?.blockMember(payload);

if (response.success) {
  // Update state in local db as well, 0 for blocked and 1 for unblocked
  await lmChatClient?.updateChatRequestState(chatroomId, 1);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Block Member Payload

List of parameters for the `blockMember` function.

| Variable     | Type   | Description | Optional |
| ------------ | ------ | ----------- | -------- |
| `chatroomId` | number | Chatroom Id |          |
| `status`     | number | Member Id   |          |
