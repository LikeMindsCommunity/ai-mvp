---
sidebar_position: 5
title: Like Comment
slug: /react-native/data/comment/like-comment
---

# Like Comment

The LikeMinds ReactNative Feed SDK, provides the Like Comment functionality. This feature allows members to indicate their support or agreement with a particular comment in a simple and intuitive manner.

## Steps to like a comment

1. Use the `likeComment()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `LikeCommentRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const likeCommentRequest = LikeCommentRequest.builder()
    .setPostId("<ENTER_POST_ID>") // post id of the comment to be deleted
    .setCommentId("<ENTER_COMMENT_ID>") // id of the comment to be deleteddeletes others comment
    .build();
  const response = await lmFeedClient.likeComment(likeCommentRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::note
Same function can be used to like a reply as well. Just pass the id of the reply as comment id.
:::

## Models

### LikeCommentRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                 | **OPTIONAL** |
| :----------- | :------- | :------------------------------ | :----------: |
| `postId`     | string   | Post ID of the liked comment.   |              |
| `commentId`  | string   | Unique ID of the comment liked. |              |
