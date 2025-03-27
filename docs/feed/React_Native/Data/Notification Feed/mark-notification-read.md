---
sidebar_position: 3
title: Mark Notification Read
slug: /react-native/data/notification-feed/mark-notification-read
---

You can use the following function from the LikeMinds SDK to mark the notifications that have been clicked by user in your application, as read.

## Steps to mark a notification as read

1. Use the `markReadNotification()` function provided by the `lmFeedClient` object created earlier.
2. Create an instance of `MarkReadNotificationRequest`, as shown in the snippet and pass it to the above method.
3. Use the response as per your requirement

```js
try {
  const markReadNotificationRequest = MarkReadNotificationRequest.builder()
    .setActivityId("<ENTER_ACTIVITY_ID>")
    .build();
  const response = await lmFeedClient.markReadNotification(
    markReadNotificationRequest
  );
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

### MarkReadNotificationRequest

| **VARIABLE** | **TYPE** | **DESCRIPTION**                                                | **OPTIONAL** |
| :----------- | :------- | :------------------------------------------------------------- | :----------: |
| `activityId` | string   | ID of the notification activity which is to be marked as read. |              |
