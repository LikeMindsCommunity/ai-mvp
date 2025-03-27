---
sidebar_position: 8
title: Fetch Post Likes
slug: /react-native/data/post/fetch-post-likes
---

# Fetch Post Likes

The Fetch Post Likes feature in the LikeMinds ReactNative Feed SDK allows users to retrieve information about the number of likes received by a specific post. By utilizing this functionality, developers can display the total number of likes on a post and provide users with social validation and engagement metrics.

## Steps to fetch likes on a post

1. Use the `getPostLikes()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetPostLikesRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getPostLikesRequest = GetPostLikesRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .setPage(1)
    .setPageSize(10)
    .build();
  const response = await lmFeedClient.getPostLikes(getPostLikesRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetPostLikes

| Variable   | Type   | Description                                    | Optional |
| ---------- | ------ | ---------------------------------------------- | -------- |
| `postId`   | string | Unique id of the post whose likes are fetched. |          |
| `page`     | int    | Page number of paginated like data.            |          |
| `pageSize` | int    | Page size for paginated like data.             |          |

### GetPostLikesResponse

| Variable     | Type                                           | Description                           | Optional           |
| ------------ | ---------------------------------------------- | ------------------------------------- | ------------------ |
| `likes`      | List<[Like](../Models/like-model.md)>          | List of the likes on the post.        | :heavy_check_mark: |
| `totalCount` | int                                            | Total count of likes on the post.     | :heavy_check_mark: |
| `users`      | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |                    |
