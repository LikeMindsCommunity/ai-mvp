---
sidebar_position: 1
title: Home Feed
slug: /react-native/data/home-feed
---

# Home Feed

The Home Feed is a vital component of many applications, providing users with a centralized hub to discover and engage with various content, including chatrooms, discussions, and other interactive features. In the context of the React Native SDK, the Home Feed serves as a customizable and dynamic feed that can be tailored to suit your application's needs.

This guide provide step-by-step instructions, code snippets, and best practices for integrating the Home Feed and fetching community chatrooms in your React Native app.

Let's dive into the world of Home Feed integration with the React Native SDK and unlock the potential for vibrant chatroom communities within your application.

## Steps to fetch explore tab counts

1. To fetch home feed in Group Chat, use the method `getExploreTabCount()` provided by the client you initialised.
2. Process the response as per your requirement.

```tsx
const response = await lmChatClient?.getExploreTabCount();
if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process the response data
  processResponse(response);
}
```

## Steps to fetch Group Chats

1. Call `getFilteredChatrooms()` function using the instance of lmChatClient, and pass false as parameter.
2. Process the response as per your requirement.

```tsx
const response = await lmChatClient?.getFilteredChatrooms(false); // false in true for home feed

if (response.success) {
  // your function to process the response data
  processResponse(response);
} else {
  // your function to process error message
  processError(response);
}
```
