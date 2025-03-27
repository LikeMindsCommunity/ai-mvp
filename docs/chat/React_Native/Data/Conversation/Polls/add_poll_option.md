---
sidebar_position: 4
title: Add Poll Option
slug: /react-native/data/conversation/polls/add-poll
---

# Add Poll Option

The "Add Poll Option" method permits users to contribute new response options, expanding the poll's flexibility and inclusivity. You can integrate this feature by following the given steps.

## Steps to Add Poll Option

1. To add a new poll option, use the `addPollOption()` method provided by the client.
2. Pass in the required parameters.
3. Process the response as per your requirement.

```js
const payload = {
  conversationId: "ENTER_CONVERSATION_ID"
  poll: {
    text: "ENTER_TEXT_FOR_NEW_POLL_OPTION",
  },
};
const response = await lmChatClient?.addPollOption(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Add Poll Option Payload

| Variable       | Type   | Description                                | Optional |
| -------------- | ------ | ------------------------------------------ | -------- |
| conversationId | number | Conversation Id                            |          |
| poll           | object | Poll object containing the new option text |          |

### Add Poll Option Response

| Variable | Type   | Description                             | Optional           |
| -------- | ------ | --------------------------------------- | ------------------ |
| data     | object | Data object containing the poll details | :heavy_check_mark: |
