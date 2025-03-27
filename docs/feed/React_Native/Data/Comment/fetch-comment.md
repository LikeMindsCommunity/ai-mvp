---
sidebar_position: 2
title: Fetch Comment
slug: /react-native/data/comment/fetch-comment
---

# Fetch Comment

The LikeMinds ReactNative feed SDK provides feature to fetch Comment. Elevate user interaction in your ReactNative app with by integrate a powerful and customizable comment section that encourages dynamic conversations among users.

## Steps to fetch a comment

1. Use the `getComments()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetCommentsRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getCommentsRequest = GetCommentsRequest.builder()
    .setPostId("<ENTER_POST_ID>") // id of the post on which member has commented
    .setCommentId("<ENTER_COMMENT_ID>")
    .setPage(1)
    .setPageSize(10)
    .build();
  const response = await lmFeedClient.getComments(getCommentsRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::note
Same function can be used to fetch a reply as well. Just pass the id of the reply as comment id.
:::

## Models

### GetCommentRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                              | **OPTIONAL** |
| :----------- | :------- | :------------------------------------------- | :----------: |
| `postId`     | string   | Post ID of the comment fetched.              |              |
| `commentId`  | string   | ID of the comment fetched.                   |              |
| `page`       | int      | Page number of paginated replies on comment. |              |
| `pageSize`   | int      | Page size for paginated creplies on comment. |              |

### GetCommentResponse

| **VARIABLE** | **TYPE**                                       | **DESCRIPTION**                       | **OPTIONAL** |
| :----------- | :--------------------------------------------- | :------------------------------------ | :----------: |
| `comment`    | [Comment](../Models/comment-model.md)          | Object of the added comment.          |              |
| `users`      | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |              |
