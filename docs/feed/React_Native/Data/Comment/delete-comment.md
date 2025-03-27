---
sidebar_position: 4
title: Delete Comment
slug: /react-native/data/comment/delete-comment
---

# Delete Comment

In the LikeMinds ReactNative Feed SDK, users have the capability to delete their own comments. This functionality allows members to easily remove their comments from the discussion thread or post, providing them with control over their contributions and ensuring a clean and organized conversation environment. Deleting a comment is a straightforward process, giving users the ability to manage and curate their own content within the application.

:::note
**Community Managers** can also delete the comments of other members, but a reason is required.
:::

## Steps to delete a comment in a post

1. Use the `deleteComment()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `DeleteCommentRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const deleteCommentRequest = DeleteCommentRequest.builder()
    .setPostId("<ENTER_POST_ID>") // post id of the comment to be deleted
    .setCommentId("<ENTER_COMMENT_ID>") // id of the comment to be deleted
    .setReason("Reason for comment deletion") // reason for deletion required when Community Manager deletes others comment
    .build();
  const response = await lmFeedClient.deleteComment(deleteCommentRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::note
Same function can be used to delete a reply as well. Just pass the id of the reply as comment id.
:::

## Models

### DeleteCommentRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                         |    **OPTIONAL**    |
| :----------- | :------- | :-------------------------------------- | :----------------: |
| `postId`     | string   | Post id of the comment to be deleted    |                    |
| `commentId`  | string   | Unique id of the comment to be deleted. |                    |
| `reason`     | string   | Reason for comment deletion.            | :heavy_check_mark: |

:::note
`reason` is only required when **Community Manager** deletes other members comment.
:::
