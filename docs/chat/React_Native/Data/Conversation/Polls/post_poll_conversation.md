---
sidebar_position: 1
title: Create Poll
slug: /react-native/data/conversation/polls/post-poll
---

# Create Poll

LikeMinds Chat SDK Poll Features enables you to engage your users, to create and participate in polls right within your in-app community. The "Create Poll" method allows you to empower your users to craft their own polls with customized questions and response options. You can integrate the above by following the given steps.

## Steps to Create Poll

1. To create a poll, use the `postPollConversation()` method provided by the client.
2. Pass in the required parameters to define the poll question and options.
3. Process the response as per your requirement.

```js
const payload = {
  chatroomId: "ENTER_CHATROOM_ID",
  text: "ENTER_POLL_QUESTION",
  expiryTime: "ENTER_EXPIRY_TIME", // epoch time
  pollType: 0, // The type of poll, it can be "0 | 1".
  isAnonymous: false, // Determines if the poll is anonymous (true/false).
  allowAddOption: false, // Determines if participants can add their own options to the poll (true/false).
  polls: [
    {
      text: "", // The text representing a poll option.
    },
  ],
  state: 10, // The state 10 signifies that the conversation is a poll .
};

const response = await lmChatClient?.postPollsConversation(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

:::note

Poll type can be 0 or 1

- 0 refers to Instant Poll
- 1 refers to Deferred Poll.

:::

### Create Poll Payload

| Variable            | Type             | Description                                                                                                  | Optional |
| ------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------ | -------- |
| chatroomId          | number           | Chatroom Id.                                                                                                 |          |
| text                | string           | The title/question for the poll.                                                                             |          |
| expiryTime          | number           | Time in epoch format when the poll expires.                                                                  |          |
| pollType            | numnber          | Type of poll <br/> - 0 for **Instant Poll** <br/> - 1 for **Deferred Poll**                                  |          |
| isAnonymous         | boolean          | Indicates if the poll responses are anonymous.                                                               |          |
| allowAddOption      | boolean          | Allows users to add options to the poll.                                                                     |          |
| polls               | Array of objects | An array of poll options.                                                                                    |          |
| state               | number           | State of the poll.                                                                                           |          |
| multipleSelectState | number           | State of multiple-choice poll:<br/> - 0 for **Exactly** <br/> - 1 for **At max** <br/> - 2 for **At least**. |          |
| multipleSelectNo    | number           | Number of options that can be selected (used with `multipleSelectState`).                                    |          |

### Create Poll Response

List of parameters in the response.

| Variable     | Type   | Description              | Optional           |
| ------------ | ------ | ------------------------ | ------------------ |
| conversation | object | Poll Conversation object | :heavy_check_mark: |
