---
sidebar_position: 3
title: Update User Topics
slug: /react-native/data/topic/update-user-topics
---

# Update User Topics

The LikeMinds ReactNative Feed SDK allows developers to modify the list of topics associated with specific users. This can be useful for ensuring that user interests are accurately represented in the application.

## Steps to Update User Topics

1. Use the `updateUserTopics()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `UpdateUserTopicsRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
import { UpdateUserTopicsRequest } from "@likeminds.community/feed-rn";

try {
  const updateUserTopicRequest = UpdateUserTopicsRequest.builder()
    .setTopicsIds({
      topic_id_1: true,
      topic_id_2: true,
      topic_id_3: false,
    }) // Replace with the UUIDs of the users whose topics you want to fetch
    .setUuid("uuid_of_user")
    .build();

  const response = await lmFeedClient.updateUserTopics(updateUserTopicsRequest);
  console.log(response); // Handle the response as needed
} catch (error) {
  // Handle the error as necessary
}
```

## UpdateUserTopicsRequest

| **VARIABLE** | **TYPE**               | **DESCRIPTION**                                         |
| :----------- | :--------------------- | :------------------------------------------------------ |
| `uuid`      | `string`               | UUID of the user whose topics are updating              |
| `topicsIds`  | Record<string,boolean> | An array of user topic IDs for whom to retrieve topics. |
