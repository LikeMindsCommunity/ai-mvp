---
sidebar_position: 6
title: Save Post
slug: /react-native/data/post/save-post
---

The LikeMinds ReactNative feed SDK provides "Save Post" feature. You can integrate it in your ReactNative application to enhance user experience by allowing them to bookmark and revisit their favorite posts at their convenience. Enable seamless content curation, empowering users to organize and access valuable information with ease.

## Steps to save a post

1. Use the `savePost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `SavePostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const savePostRequest = SavePostRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .build();
  const response = await lmFeedClient.savePost(savePostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### SavePostRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**              | **OPTIONAL** |
| :----------- | :------- | :--------------------------- | :----------: |
| `postId`     | string   | Unique id of the post saved. |              |
