---
sidebar_position: 2
title: Create Direct Message Chatroom
slug: /react-native/data/chatroom/direct-messages/create-direct-message
---

# Create Direct Message Chatroom

LikeMinds React Native Chat SDK offers a convenient feature to create Direct Message Chatrooms, allowing you to communicate privately with specific individuals.

## Steps to check Direct Messages limit

1. Check Direct Message Chatroom already exist or not and member have not crossed its limit to send Direct Message request, use the method `checkDMLimit()`
2. Pass in the required parameter `uuid`.
3. Process the response as per your requirement.

```ts
const payload: any = {
  uuid: "ENTER_MEMBER_UUID",
};
const response = await lmChatClient?.checkDMLimit(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### Check DM Limit Payload

List of parameters for the `checkDMLimit()` function.

| Variable | Type             | Description | Optional |
| -------- | ---------------- | ----------- | -------- |
| `uuid`   | number or string | Member Uuid |          |

### Check DM Limit Response

List of parameters in the response.

| Variable    | Type   | Description |
| ----------- | ------ | ----------- |
| chatroom_id | number | Chatroom ID |

## Steps to create direct message chatroom

1. If Direct Message Chatroom does not exist and limit is not exceeded, use the method `createDMChatroom()`
2. Pass in the required parameter `uuid`.
3. Process the response as per your requirement.

```ts
const payload: any = {
  uuid: "ENTER_UUID, // Enter the member's uuid to initiate a private message.
};
const response = await lmChatClient?.checkDMLimit(payload);

if (response.success) {
  // your function to process the response data
  let res = response?.data;
  if (!!res?.chatroom_id) {
    //DM already created
    processResponse(response); // Open the respective chatroom
  } else {
    if (res?.is_request_dm_limit_exceeded === false) {
      const payloadCreateDM: any = {
        uuid: "ENTER_UUID", // Enter the member's uuid to initiate a private message.
      };
      const responseCreateDM = await lmChatClient?.createDMChatroom(
        payloadCreateDM
      );

      if (responseCreateDM.success) {
        // your function to process the response data
        processResponse(responseCreateDM);
      } else {
        // your function to process error message
        processError(responseCreateDM);
      }
    } else {
      Alert.alert("Request limit exceeded"); ////Show disclaimer popup on limit exceed.
    }
  }
} else {
  // your function to process error message
  processError(response);
}
```

### Create DM Chatroom Payload

List of parameters for the `createDMChatroom()` function.

| Variable | Type             | Description | Optional |
| -------- | ---------------- | ----------- | -------- |
| `uuid`   | number or string | Member Uuid |          |

### Create DM Chatroom Response

List of parameters in the response.

| Variable | Type   | Description      |
| -------- | ------ | ---------------- |
| chatroom | object | Chatroom Details |
