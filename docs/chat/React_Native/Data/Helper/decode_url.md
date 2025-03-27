---
sidebar_position: 3
title: Decode URL
slug: /react-native/data/conversation/decode-url
---

# Decode URL

LikeMinds React Native Chat SDK allows you to conveniently decode a URL string, providing the original URL components such as protocol, host, path, and query parameters for further processing or display.

## Steps to decode URL

1. Create a `DecodeUrlRequest` object using `DecodeUrlRequestBuilder` class by passing all the required parameters.
2. For decoding an URL call `decodeUrl()` present in `LMChatClient`.
3. Process the response `DecodeUrlResponse` as per your requirement.

```ts
const payload: any = {
  url: "ENTER_URL",
};
const response = await lmChatClient?.decodeUrl(payload);

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```

### DecodeUrlRequest

List of parameters provided by `decodeUrl()`

| Variable | Type   | Description                   | Optional |
| -------- | ------ | ----------------------------- | -------- |
| `url`    | string | URL of the link to be decoded |          |

### DecodeUrlResponse

List of parameters in the response.

| Variable | Type                                               | Description                  |
| -------- | -------------------------------------------------- | ---------------------------- |
| `ogTags` | [LinkOGTags](../Models/conversation/#link-og-tags) | OG tags to show link preview |
