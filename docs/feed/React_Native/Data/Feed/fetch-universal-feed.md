---
sidebar_position: 1
title: Universal Feed
slug: /react-native/data/feed/universal-feed
---

The LikeMinds ReactNative Feed SDK provides a powerful Universal Feed feature for your Android/iOS app. Easily integrate a versatile feed that allows all the users in the community to view a common **feed**

## Steps to fetch Universal feed

1. Use the `getFeed()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetFeedRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getFeedRequest = GetFeedRequest.builder()
    .setPage(1) // page number for paginated feed data
    .setPageSize(10) // page size for paginated feed data
    .build();
  const response = await lmFeedClient.getFeed(getFeedRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Steps to fetch Universal feed with selected topics

1. Use the `getTopics()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetFeedRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getFeedRequest = GetFeedRequest.builder()
    .setPage(1) // page number for paginated feed data
    .setPageSize(10) // page size for paginated feed data
    .topics(["ENTER_TOPIC_IDs"]) // fetches posts with given topics from feed
    .build();
  const response = await lmFeedClient.getFeed(getFeedRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetFeedRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                      | **OPTIONAL** |
| :----------- | :------- | :----------------------------------- | :----------: |
| `page`       | int      | Page number for paginated feed data. |              |
| `pageSize`   | int      | Page size for paginated feed data.   |              |
| `topicIds`   | string[] | Array of Topic IDs selected by user  |      ✔       |

### GetFeedResponse

| **VARIABLE**        | **TYPE**                                                      | **DESCRIPTION**                       | **OPTIONAL** |
| :------------------ | :------------------------------------------------------------ | :------------------------------------ | :----------: |
| `post`              | [Post](../Models/post-model.md)                               | Object of the created post.           |              |
| `users`             | Record<string,[User](../Models/user-model.md)>                | Map of user unique id to user object. |              |
| `topics`            | Record<string,[Topic](../Models/topic-model.md)>              | Map of topic id to topic object.      |              |
| `widgets`           | Record<string,Widget>                                         | Map of widget id to widget object.    |              |
| `filtered_comments` | [FilteredComments](../Models/post-model.md/#filteredcomments) | Object of the filtered comments       |              |
