---
sidebar_position: 2
title: Submit Poll
slug: /react-native/data/conversation/polls/submit-poll
---

# Submit Poll

Once the polls are created, users can submit their responses to the polls effortlessly. The "Submit Poll" method ensures that their answers are recorded accurately and promptly, fostering a smooth and interactive user experience. You can integrate the above by following the given steps.

## Steps to Submit a Poll

1. To submit a poll response, use the `submitPoll()` method provided by the client.
2. Pass in the required parameters.
3. Process the response of type `LMResponse<Nothing>` as per your requirement.

```js
const payload = {
  conversationId: "ENTER_CONVERSATION_ID"
  polls: [
    {
      id: "ID_OF_SELECTION_OPTION"
    },
  ], // An array of IDs for the selected options
};
const response = await lmChatClient?.submitPoll(payload);

if (response.success) {
  // update poll votes in local db
  await lmChatClient?.updatePollVotes(
    response?.conversations,
    user?.sdkClientInfo?.community
  );
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Submit Poll Payload

| Variable       | Type            | Description                               | Optional |
| -------------- | --------------- | ----------------------------------------- | -------- |
| conversationId | number          | Conversation Id                           |          |
| polls          | array of object | An array of selected options for the poll |          |
