---
sidebar_position: 1
title: Create Post
slug: /react-native/data/post/create-post
---

# Create Post

Allows users to compose and publish new posts within the application, facilitating content creation and user-generated interactions.

## Steps to create a post

1. Use the `addPost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `AddPostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const attachmentArr = [];
  const topicIds = [];
  const isAnonymous = true;
  const addPostRequest = AddPostRequest.builder()
    .setHeading("Post heading")
    .setText("Post content")
    .setAttachments(attachmentArr)
    .setTopicIds(topicIds)
    .setTempId("TEMP_ID")
    .setIsAnonymous(isAnonymous ?? false)
    .build();
  const response = await lmFeedClient.addPost(addPostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Additional Features

### Tag a User

To tag a user, use the [getTaggingList()](../Helper/tagging-member.md) function to fetch the list of users that can be tagged, and use the format `<<[user.name]|route://user_profile/[user.sdkClientInfo.uuid]>>` to embed it inside the text of the post.

### Decode URL

To decode a URL, use the [decodeUrl()](../Helper/decode-url.md) function to decode a URL and get its OGTags. Use those to add an **attachment of type 4**.

### Add a Topic

Topics are keywords related to a post, they can be considered having the same use case as hashtags. You can add a topic to the post by sending the `topicIds` list in the `AddPostRequest` with the topics you have fetched using the [getTopics()](../Topic/get-topics.md).

## Models

### AddPostRequest

| Variable         | Type                                              | Description                                           | Optional           |
| ---------------- | ------------------------------------------------- | ----------------------------------------------------- | ------------------ |
| `text`           | string                                            | Text content of the post.                             | :heavy_check_mark: |
| `attachments`    | [Attachment](../Models/post-model.md/#attachment) | Attachments to be uploaded.                           | :heavy_check_mark: |
| `heading`        | string                                            | Heading of the post.                                  | :heavy_check_mark: |
| `tempId`         | string                                            | Temporary ID of post.                                 | :heavy_check_mark: |
| `topicIds`       | string[]                                          | List of topics user want to add in the post.          | :heavy_check_mark: |
| `onBehalfOfUUID` | string                                            | UUID of the user on whose behalf the post is created. | :heavy_check_mark: |
| `isAnonymous`    | boolean                                           | Indicates if the post should be anonymous.            |                    |

:::caution
Note You cannot create an empty post. Send data in at least one of these keys: text, heading, or attachments
:::

### AddPostResponse

| Variable | Type                                             | Description                           | Optional           |
| -------- | ------------------------------------------------ | ------------------------------------- | ------------------ |
| `post`   | [Post](../Models/post-model.md)                  | Object of the created post.           | :heavy_check_mark: |
| `users`  | Record<string,[User](../Models/user-model.md)>   | Map of user unique id to user object. |                    |
| `topics` | Record<string,[Topic](../Models/topic-model.md)> | Map of topic id to topic object.      | :heavy_check_mark: |
| `widget` | [Widget](../Models/post-model.md/#widget)        | Widget data for the post.             |                    |
