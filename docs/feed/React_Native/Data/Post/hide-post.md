---
sidebar_position: 9
title: Hide Post
slug: /react-native/data/post/hide-post
---

# Hide Post

The `Hide Post` feature allows users to hide specific posts from their view within the application. This can be useful for managing the content they interact with.

## Steps to Hide a Post

1. Use the `hidePost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `HidePostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const hidePostRequest = HidePostRequest.builder()
    .setPostId("POST_ID") // Replace with the ID of the post to be hidden
    .build();
  const response = await lmFeedClient.hidePost(hidePostRequest);
  // The response will be an empty object
} catch (error) {
  // Handle the error as necessary
}
```

## Models

### HidePostRequest

| Variable | Type   | Description | Optional           |
| -------- | ------ | ----------- | ------------------ |
| `postId` | string | Id of post. | :heavy_check_mark: |
