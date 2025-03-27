---
sidebar_position: 9
title: View Participants
slug: /react-native/data/chatroom/group-chat/view-participants
---

# View Participants

To retrieve the list of participants in a chatroom, LM React Native Chat SDK provides this feature. It enables you to retrieve user details, such as usernames or profile information, for better engagement and interaction within the chatroom.

## Steps to Get the List of Participants in a Chatroom

1. To fetch the list of the participants, use the method `getParticipants` provided by the client you initialised.
2. Pass in the required parameters `chatroomId`, `page`, `pageSize` and `isSecret`.
3. Process the response as per your requirement.

```ts
const payload: any = {
  chatroomId: "ENTER_CHATROOM_ID",
  isSecret: true, // true if the chatroom is secret
  page: "ENTER_REQUIRED_PAGE_NO",
  pageSize: "ENTER_PAGE_SIZE", /
};
const response = await lmChatClient?.getParticipants(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### View Participants Payload

List of parameters for the `getParticipants` method.

| Variable     | Type    | Description        | Optional           |
| ------------ | ------- | ------------------ | ------------------ |
| `chatroomId` | number  | Chatroom Id        |                    |
| `page`       | number  | Page int           |                    |
| `pageSize`   | number  | Page size          |                    |
| `isSecret`   | boolean | Is secret chatroom |                    |
| `search`     | String  | Search string      | :heavy_check_mark: |

### View Participants Response

List of parameters in the response.

| Variable                   | Type    | Description              |
| -------------------------- | ------- | ------------------------ |
| `participants`             | array   | List of participants     |
| `total_participants_count` | boolean | Total participants Count |
