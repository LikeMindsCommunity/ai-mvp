---
sidebar_position: 2
title: Direct Messages Feed
slug: /react-native/data/direct-message-feed
---

# Direct Messages Feed

The Direct Messages Feed is a vital component of many applications, providing users with a centralized hub to discover and engage with various users. In the context of the React Native SDK, the Direct Messages Feed serves as a customizable and dynamic feed that can be tailored to suit your application's needs.

This guide provide step-by-step instructions, code snippets, and best practices for integrating the Direct Messages Feed and fetching community chatrooms in your React Native app.

Let's dive into the world of Direct Messages Feed integration with the React Native SDK and unlock the potential for vibrant chatroom communities within your application.

## Steps to fetch Direct Messages

1. Call `getFilteredChatrooms()` function using the instance of lmChatClient, and pass true as parameter.
2. Process the response as per your requirement.

```tsx
const response = await lmChatClient?.getFilteredChatrooms(true); // pass in true for dm feed

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

## Steps to Check Direct Messages Status

### Check DM Status

1. To check Direct Messages status, use the method `checkDMStatus()` provided by the client you initialised.
2. Pass in the required parameter `requestFrom`, to give the channel from where you are requesting.
3. Process the response as per your requirement.

```tsx
const payloadCheckDM: any = {
  requestFrom: "CHANNEL_FROM_WHERE_DM_IS_FETCHED",
};
const responseCheckDM = await lmChatClient?.checkDMStatus(payloadCheckDM);

if (responseCheckDM.success) {
  // your function to process the response data
  processResponse(responseCheckDM);
} else {
  // your function to process error message
  processError(responseCheckDM);
}
```

### Check DM Status Payload

| Variable    | Type   | Description                                                                | Optional |
| ----------- | ------ | -------------------------------------------------------------------------- | -------- |
| requestFrom | string | Channel from which you are fetching DM. Either group_channel or dm_feed_v2 |          |

### Check DM Status Response

| Variable | Type    | Description                                 | Optional |
| -------- | ------- | ------------------------------------------- | -------- |
| cta      | string  | Custom route for the target screen          |          |
| show_dm  | boolean | Direct Messages is ON or OFF from dashboard |          |
