---
sidebar_position: 2
title: Fetch Post
slug: /react-native/data/post/fetch-post
---

# Fetch Post

Retrieves a specific post from the server, allowing users to view its content, comments, likes, and other associated information.

## Steps to fetch a post

1. Use the `getPost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `GetPostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const getPostRequest = GetPostRequest.builder()
    .setPostId("<ENTER_POST_ID>")
    .setPage(1)
    .setPageSize(10)
    .build();
  const response = await lmFeedClient.getPost(getPostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetPostRequest

| Variable   | Type   | Description                    | Optional           |
| ---------- | ------ | ------------------------------ | ------------------ |
| `postId`   | string | Unique id of the post fetched. |                    |
| `page`     | int    | page number                    | :heavy_check_mark: |
| `pageSize` | int    | number of items per page       | :heavy_check_mark: |

### GetPostResponse

| Variable | Type                                          | Description                           | Optional           |
| -------- | --------------------------------------------- | ------------------------------------- | ------------------ |
| `post`   | [Post](../Models/post-model.md)               | Object of the created post.           | :heavy_check_mark: |
| `users`  | Map<string,[User](../Models/user-model.md)>   | Map of user unique id to user object. |                    |
| `topics` | Map<string,[Topic](../Models/topic-model.md)> | Map of topic id to topic object.      | :heavy_check_mark: |
| `widget` | [IWidget](../Post/fetch-post.md/#iwidget)     | Widget data for the post.             |                    |
