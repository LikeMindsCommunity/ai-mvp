---
sidebar_position: 4
title: Delete Post
slug: /react-native/data/post/delete-post
---

Users have the capability to delete their own posts, allowing them to easily remove any content they no longer wish to share.

:::note
**Community Managers** can also delete other members' posts, but a reason is required.
:::

### Follow these steps to delete a post

1. Use the `deletePost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `DeletePostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const deletePostRequest = DeletePostRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .setDeleteReason("Reason for post deletion")
    .build();
  const response = await lmFeedClient.deletePost(deletePostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### DeletePostRequest

| Variable       | Type   | Description                          | Optional           |
| -------------- | ------ | ------------------------------------ | ------------------ |
| `postId`       | string | Unique id of the post to be deleted. |                    |
| `deleteReason` | string | Reason for post deletion.            | :heavy_check_mark: |

:::note

Delete reason is only required when **Community Manager** deletes other members post.

:::
