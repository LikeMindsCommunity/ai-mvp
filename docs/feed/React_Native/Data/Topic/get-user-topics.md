---
sidebar_position: 2
title: Get User Topics
slug: /react-native/data/topic/get-user-topics
---

# Get User Topics

The LikeMinds ReactNative Feed SDK allows developers to retrieve a list of topics associated with specific users. This can be useful for personalizing user experiences or displaying relevant content.

## Steps to Get User Topics

1. Use the `getUserTopics()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetUserTopicsRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
import {GetUserTopicsRequest} from '@likeminds.community/feed-rn';

try {
  const userTopicsRequest = GetUserTopicsRequest.builder()
      .setUuids(['USER_UUID_1', 'USER_UUID_2']) // Replace with the UUIDs of the users whose topics you want to fetch
      .build();

  const response = await lmFeedClient.getUserTopics(userTopicsRequest);
  console.log(response.topics); // Access the list of topics
} catch (error) {
  // Handle the error as necessary
}
```

## GetUserTopicsRequest

| **VARIABLE** | **TYPE**   | **DESCRIPTION**                                     |
| :----------- | :--------- | :-------------------------------------------------- |
| `uuids`      | `string[]` | An array of user UUIDs for whom to retrieve topics. |

## GetUserTopicsResponse

| **VARIABLE** | **TYPE**                   | **DESCRIPTION**                                      |
| :----------- | :------------------------- | :--------------------------------------------------- |
| `topics`     | `Record<string, Topic>`    | Map of topics, with each topic ID as the key.        |
| `userTopics` | `Record<string, string[]>` | Map of user UUIDs to lists of topic IDs they follow. |
| `users`      | `Record<string, User>`     | Map of user information, with UUIDs as keys.         |
