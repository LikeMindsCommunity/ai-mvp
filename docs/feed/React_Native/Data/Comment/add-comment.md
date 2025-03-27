---
sidebar_position: 1
title: Add Comment
slug: /react-native/data/comment/add-comment
---

# Add Comment

The LikeMinds ReactNative Feed SDK, users can engage in interactive discussions by adding comments to posts. This feature enables users to express their thoughts, ask questions, and engage with other members in a dynamic and collaborative manner.

## Steps to add a comment on post

1. Use the `addComment()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `AddCommentRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const addCommentRequest = AddCommentRequest.builder()
    .setPostId("<ENTER_POST_ID>") // id of the post on which member has commented
    .setText("Comment text") // comment text
    .setTempId("<ENTER_TEMP_ID>")
    .build();
  const response = await lmFeedClient.addComment(addCommentRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Additional Features

### Tag a User

To tag a user, use the [getTaggingList()](../Helper/tagging-member.md) function to fetch the list of users that can be tagged, and use the format `<<[user.name]|route://user_profile/[user.sdkClientInfo.uuid]>>` to embed it inside the text of the comment.

## Models

### AddCommentRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                               | **OPTIONAL** |
| :----------- | :------- | :-------------------------------------------- | :----------: |
| `postId`     | string   | ID of the post on which member has commented. |              |
| `text`       | string   | Text content of the comment.                  |              |
| `tempId`     | string   | Temporary ID for Comment                      |              |

### AddCommentResponse

| **VARIABLE** | **TYPE**                                       | **DESCRIPTION**                       | **OPTIONAL** |
| :----------- | :--------------------------------------------- | :------------------------------------ | :----------: |
| `comment`    | [Comment](../Models/comment-model.md)          | Object of the added comment.          |              |
| `users`      | Record<string,[User](../Models/user-model.md)> | Map of user unique id to user object. |              |
