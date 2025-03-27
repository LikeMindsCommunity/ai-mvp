---
title: Decode URL
sidebar_position: 2
slug: /react-native/data/helper/decode-url
---

Parses and decodes a URL string, providing the original URL components such as protocol, host, path, and query parameters for further processing or display.

## Steps to Decode URL

1. Use the `decodeURL()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `DecodeURLRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const decodeUrlRequest = DecodeURLRequest.builder()
    .setURL("https://likeminds.community/") // url of the link to be decoded
    .build();
  const response = await lmFeedClient.decodeURL(decodeUrlRequest);
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### DecodeURLRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                | **OPTIONAL** |
| :----------- | :------- | :----------------------------- | :----------: |
| `url`        | string   | URL of the link to be decoded. |              |

### DecodeURLResponse

| **VARIABLE** | **TYPE**                                  | **DESCRIPTION**              | **OPTIONAL** |
| :----------- | :---------------------------------------- | :--------------------------- | :----------: |
| `ogTags`     | [OGTags](../Models/post-model.md/#ogtags) | OG tags to show link preview |              |
