---
sidebar_position: 3
title: Get Poll Result
slug: /react-native/data/conversation/polls/get-poll-result
---

# Get Poll Result

With the "Get Poll Result" method, you can retrieve the poll results in real-time and display in your application. You can integrate the above by following the given steps.

## Steps to Get Poll Result

1. To get poll results, use the `getPollUsers()` method provided by the client.
2. Pass in the required parameter.
3. Process the response as per your requirement.

```js
const payload = {
  conversationId: "ENTER_CONVERSATION_ID",
  pollId: "ENTER_POLL_ID",
};
const response = await lmChatClient?.getPollUsers(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Get Poll Result Payload

| Variable       | Type   | Description     | Optional |
| -------------- | ------ | --------------- | -------- |
| conversationId | number | Conversation Id |          |
| pollId         | number | Poll Id         |          |

### Get Poll Result Response

| Variable | Type   | Description                                | Optional           |
| -------- | ------ | ------------------------------------------ | ------------------ |
| data     | object | Data object containing the list of members | :heavy_check_mark: |
