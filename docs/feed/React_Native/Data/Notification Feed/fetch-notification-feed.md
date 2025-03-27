---
sidebar_position: 1
title: Fetch Notification Feed
slug: /react-native/data/notification-feed/fetch-notification-feed
---

Notification feed is a great way to populate notifications for a user. You can achieve the same with LikeMinds SDK, by following the steps given below.

## Steps to fetch notification feed

1. Use the `getNotificationFeed()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetNotificationFeedRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getNotificationFeedRequest = GetNotificationFeedRequest.builder()
    .setPage(1) // page number for the paginated notification feed data
    .setPageSize(10) // page number for the paginated notification feed data
    .build();
  const response = await lmFeedClient.getNotificationFeed(
    getNotificationFeedRequest
  );
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetNotificationFeedRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                                   | **OPTIONAL** |
| :----------- | :------- | :------------------------------------------------ | :----------: |
| `page`       | int      | Page number for paginated notification feed data. |              |
| `pageSize`   | int      | Page size for paginated notification feed data.   |              |

### GetNotificationFeedResponse

| **VARIABLE** | **TYPE**                                         | **DESCRIPTION**                              | **OPTIONAL** |
| :----------- | :----------------------------------------------- | :------------------------------------------- | :----------: |
| `activities` | List<[Activity](../Models/activity-model.md)>    | List of activities inside notification feed. |              |
| `users`      | Record<string,[User](../Models/user-model.md)>   | Dictionary of UUID to user object.           |              |
| `topics`     | Record<string,[Topic](../Models/topic-model.md)> | Map of topic id to topic object.             |              |
