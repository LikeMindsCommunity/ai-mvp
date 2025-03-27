---
sidebar_position: 7
title: Pin Post
slug: /react-native/data/post/pin-post
---

# Pin Post

In the LikeMinds ReactNative Feed SDK, users can conveniently "pin" posts, granting them the ability to highlight and prioritize important content on their feed. This feature ensures that selected posts remain prominently displayed at the top of the feed for improved visibility and easy access.

## Steps to pin a post

1. Use the `pinPost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `PinPostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const pinPostRequest = PinPostRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .build();
  const response = await lmFeedClient.pinPost(pinPostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### PinPostRequest

| Variable | Type   | Description           | Optional |
| -------- | ------ | --------------------- | -------- |
| `postId` | string | Unique id of the post |          |
