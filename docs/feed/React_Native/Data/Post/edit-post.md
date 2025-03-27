---
sidebar_position: 3
title: Edit Post
slug: /react-native/data/post/edit-post
---

Enables users to modify and update the content of a previously published post, ensuring the accuracy and relevance of shared information.

:::note
**Community Managers** can edit other members posts as well.
:::

## Steps to edit a post

1. Use the `editPost()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `EditPostRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const attachments = [];
  const editPostRequest = EditPostRequest.builder()
    .setPostId("<ENTER_POST_ID>") // id of the post to be edited
    .setText("Updated post text") // updated text of the post
    .setAttachments(attachments) // updated attachments of the post
    .setHeading("Heading of the post") // heading of the post
    .setTopicIds("Updated Topic ids") // updated topic ids of the post
    .build();
  const response = await lmFeedClient.editPost(editPostRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

:::warning

You must send the `text`, `heading`, and `attachments` as it is if you don't want to update them, otherwise the `text`, `heading`, and `attachments` will be set to empty.

:::

## Additional Features

### Tag a User

To tag a user, use the [getTaggingList()](../Helper/tagging-member.md) function to fetch the list of users that can be tagged, and use the format `<<[user.name]|route://user_profile/[user.sdkClientInfo.uuid]>>` to embed it inside the text of the post.

### Decode URL

To decode a URL, use the [decodeUrl()](../Helper/decode-url.md) function to decode a URL and get its OGTags. Use those to add an attachment of type 4.

### Add a Topic

Topics are keywords related to a post, they can be considered having the same use case as hashtags. You can add a topic to the post by sending the `topicIds` list in the `EditPostRequest` with the topics you have fetched using the [getTopics()](../Topic/get-topics.md).

## Models

### EditPostRequest

| **VARIABLE**  | **TYPE**                                          | **DESCRIPTION**                                          | **OPTIONAL** |
| :------------ | :------------------------------------------------ | :------------------------------------------------------- | :----------: |
| `text`        | string                                            | Text content of the post                                 |      ✔       |
| `attachments` | [Attachment](../Models/post-model.md/#attachment) | List of attached medias in the post. Maximum size is 10. |      ✔       |
| `heading`     | string                                            | Heading of the post                                      |      ✔       |
| `topicIds`    | string[]                                          | List of Topics user want to add in the post              |      ✔       |

### EditPostResponse

| Variable | Type                                          | Description                           | Optional           |
| -------- | --------------------------------------------- | ------------------------------------- | ------------------ |
| `post`   | [Post](../Models/post-model.md)               | Object of the created post.           | :heavy_check_mark: |
| `users`  | Map<string,[User](../Models/user-model.md)>   | Map of user unique id to user object. |                    |
| `topics` | Map<string,[Topic](../Models/topic-model.md)> | Map of topic id to topic object.      | :heavy_check_mark: |
| `widget` | [IWidget](../Post/edit-post.md/#iwidget)      | Widget data for the post.             |                    |
