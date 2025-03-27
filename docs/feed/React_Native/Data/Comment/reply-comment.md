---
sidebar_position: 7
title: Reply Comment
slug: /react-native/data/comment/reply-comment
---

# Reply Comment

The LikeMinds ReactNative Feed SDK offers the ability to reply to comments, enabling users to engage in threaded discussions within the application. By leveraging this feature, users can respond directly to specific comments, facilitating more focused conversations and enhancing the overall interactivity and depth of discussions on the platform.

## Steps to reply on a comment

1. Use the `replyComment()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `ReplyCommentRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const replyCommentRequest = ReplyCommentRequest.builder()
    .setPostId("<ENTER_POST_ID>") // post id of the comment to be deleted
    .setCommentId("<ENTER_COMMENT_ID>") // id of the comment to be deleted
    .setText("Reply Text") // reason for deletion required when Community Manager deletes others comment
    .setTempId("<ENTER_TEMP_ID>") // reason for deletion required when Community Manager deletes others comment
    .build();
  const response = await lmFeedClient.replyComment(replyCommentRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### AddCommentReplyRequest

| Variable    | Type   | Description              | Optional |
| ----------- | ------ | ------------------------ | -------- |
| `commentId` | string | unique id of the post    |          |
| `postId`    | string | unique id of the post    |          |
| `text`      | string | text content of reply    |          |
| `tempId`    | string | Temporary ID for comment |          |

### AddCommentReplyResponse

| Variable  | Type                                           | Description                           | Optional |
| --------- | ---------------------------------------------- | ------------------------------------- | -------- |
| `comment` | [Comment](../Models/comment-model.md)          | Object of the added comment.          |          |
| `users`   | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |          |
