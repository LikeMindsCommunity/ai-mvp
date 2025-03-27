---
sidebar_position: 2
title: Fetch Unread Notification Count
slug: /react-native/data/notification-feed/fetch-unread-notification-count
---

Unread Notification count helps you to show the unread notification which you can use to nudge the user to check the notification feed. You can achieve the same with LikeMinds SDK, by following the steps given below.

## Steps to fetch unread notification count

1. Use the `getUnreadNotificationCount()` function provided by the `lmFeedClient` object created earlier.

```js
try {
  const response = await lmFeedClient.getUnreadNotificationCount();
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetUnreadNotificationCountResponse

| **VARIABLE** | **TYPE** | **DESCRIPTION**                | **OPTIONAL** |
| :----------- | :------- | :----------------------------- | :----------: |
| `count`      | int      | Count of unread notifications. |              |
