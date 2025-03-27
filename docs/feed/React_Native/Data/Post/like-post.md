---
sidebar_position: 5
title: Like Post
slug: /react-native/data/post/like-post
---

# Like Post

The LikeMinds ReactNative Feed SDK incorporates a "like" feature that enables users to express their appreciation for posts by other members. With just a simple tap, users can indicate their interest and support for specific content on their feed.

## Steps to like a post

1. Use the `likePost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `LikePostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const likePostRequest = LikePostRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .build();
  const response = await lmFeedClient.likePost(likePostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### LikePostRequest

| Variable | Type   | Description           | Optional |
| -------- | ------ | --------------------- | -------- |
| `postId` | string | Unique id of the post |          |
