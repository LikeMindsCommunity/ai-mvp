---
sidebar_position: 6
title: Mute/Unmute Chatroom
slug: /react-native/data/chatroom/group-chat/mute-unmute-chatroom
---

# Mute/Unmute Chatroom

Muting a chatroom in LikeMinds React Native Chat SDK ensures that you won't receive any notifications for new conversations happen within that chatroom.

## Steps to Mute/Unmute a Chatroom

1. To mute on a chatroom use the method `muteChatroom()`.
2. Pass in the required parameters `chatroomId` and `value`.
3. Set the `value` to `true` for muting a chatroom or `false` to unmute it.
4. Process the response of type `LMResponse<Nothing>` as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  value: true, // true if you want to mute the chatroom or false for unmuting.
};
const response = await lmChatClient?.muteChatroom(payload);
if (response.success) {
  // Update mute status in local db as well
  lmChatClient?.updateMuteStatus(chatroomId);
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Mute Chatroom Payload

List of parameters for the `muteChatroom()` method.

| Variable     | Type    | Description | Optional |
| ------------ | ------- | ----------- | -------- |
| `chatroomId` | number  | Chatroom Id |          |
| `value`      | boolean | Mute value  |          |
