---
sidebar_position: 6
title: Fetch Comment Likes
slug: /react-native/data/comment/fetch-comment-likes
---

# Fetch Comment Likes

The Fetch Comment Likes feature in the LikeMinds ReactNative Feed SDK enables users to retrieve information about the number of likes received by a specific comment. This functionality allows developers to display the total number of likes on a comment, providing users with social validation and engagement metrics.

## Steps to fetch likes on a comment

1. Use the `getCommentLikes()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetCommentLikesRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getCommentLikesRequest = GetCommentLikesRequest.builder()
    .setPostId(ENTER_POST_ID) // post id of comment whose likes are fetched
    .setCommentId(ENTER_COMMENT_ID) // id of comment whose likes are fetched
    .setPage(1) // page number for paginated data
    .setPageSize(20) // page size for paginated data
    .build();
  const response = await lmFeedClient.getCommentLikes(getCommentLikesRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetPostLikes

| Variable    | Type   | Description                                     | Optional |
| ----------- | ------ | ----------------------------------------------- | -------- |
| `postId`    | string | Post ID of the comment whose likes are fetched. |          |
| `commentId` | string | ID of the comment whose likes are fetched.      |          |
| `page`      | int    | Page number of paginated like data.             |          |
| `pageSize`  | int    | Page size for paginated like data.              |          |

### GetPostLikesResponse

| Variable     | Type                                           | Description                           | Optional           |
| ------------ | ---------------------------------------------- | ------------------------------------- | ------------------ |
| `likes`      | List<[Like](../Models/like-model.md)>          | List of the likes on the comment.     | :heavy_check_mark: |
| `totalCount` | int                                            | Total count of likes on the comment.  | :heavy_check_mark: |
| `users`      | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |                    |
