---
sidebar_position: 3
title: Edit Comment
slug: /react-native/data/comment/edit-comment
---

# Edit Comment

The LikeMinds ReactNative Feed SDK, users can engage in interactive discussions by adding comments to posts. This feature enables users to express their thoughts, ask questions, and engage with other members in a dynamic and collaborative manner.

## Steps to edit a comment on post

1. Use the `editComment()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `EditCommentRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const editCommentRequest = EditCommentRequest.builder()
    .setPostId("<ENTER_POST_ID>") // Id of the post on which member has commented
    .setCommentId("<ENTER_COMMENT_ID>") // Enter comment id
    .setText("Update Text")
    .build();
  const response = await lmFeedClient.editComment(editCommentRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::note
Same function can be used to edit a reply as well. Just pass the id of the reply as comment id.
:::

:::caution note
You must send the `text` as it is if you don't want to update it, otherwise the `text` will be set to empty.
:::

## Models

### EditCommentRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                      | **OPTIONAL** |
| :----------- | :------- | :----------------------------------- | :----------: |
| `postId`     | string   | Post ID of the comment to be edited. |              |
| `commentId`  | string   | ID of the comment to be edited.      |              |
| `text`       | string   | Updated text content of the comment. |              |

### EditCommentResponse

| **VARIABLE** | **TYPE**                                       | **DESCRIPTION**                       | **OPTIONAL** |
| :----------- | :--------------------------------------------- | :------------------------------------ | :----------: |
| `comment`    | [Comment](../Models/comment-model.md)          | Object of the added comment.          |              |
| `users`      | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |              |
