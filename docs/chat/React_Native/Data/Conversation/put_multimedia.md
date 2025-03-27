---
sidebar_position: 7
title: Put Multimedia
slug: /react-native/data/conversation/put-multimedia
---

# Put Multimedia

LikeMinds React Native Chat SDK provides the Put Multimedia feature, allowing you to attach multimedia files to your conversations effortlessly. By utilizing this feature, you can enrich your conversations with various types of media, such as images, videos, documents, and more.

## Steps to Put Multimedia in a Conversation

1. Upload your multimedia file to any cloud service of your choice.
2. To add media to conversations use `putMultimedia()` method provided by the client you initialised.
3. Pass in the required parameters.
4. Process the response as per your requirement.

```ts
const payload: any = {
  conversationId: "ENTER_CONVERSATION_ID" ,
  filesCount: "ENTER_FILE_COUNT" , // number of files
  index: "ENTER_INDEX", // index at which you are uploading the file
  meta: {
    size: "ENTER_FILE_SIZE, //size of file
    duration: "ENTER_FILE_DURATION", // duration of file (only pass in case of video)
 },
  name: "ENTER_FILE_NAME" , // name of the file
  type: "ENTER_FILE_TYPE", //type of file `image`, `video` and `pdf`
  url: "ENTER_URL", // cloud service(e.g AWS) response url
}
const response = await lmChatClient?.putMultimedia(payload);

if(response.success){
    // your function to process the response data
   processResponse(response);
}else{
    // your function to process error message
   processError(response);
}
```

### Put Multimedia Payload

List of parameters provided by `putMultimedia()`.

| Variable         | Type   | Description                     | Optional           |
| ---------------- | ------ | ------------------------------- | ------------------ |
| `conversationId` | number | Conversation Id                 |                    |
| `url`            | string | URL of the multimedia           |                    |
| `filesCount`     | number | Count of attachments            |                    |
| `index`          | number | Index of the multimedia         |                    |
| `type`           | string | Type of the multimedia          |                    |
| `meta`           | object | Meta data of the multimedia     |                    |
| `name`           | string | name of the multimedia          |                    |
| `thumbnailUrl`   | string | Thumbnail URL of the multimedia | :heavy_check_mark: |

### Put Multimedia Response

List of parameters in the response.

| Variable       | Type                                   | Description                           |
| -------------- | -------------------------------------- | ------------------------------------- |
| `conversation` | [Conversation](../Models/conversation) | Updated conversation, after uploading |
