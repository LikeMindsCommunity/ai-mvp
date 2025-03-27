---
sidebar_position: 9
title: Notification Item
slug: /react-native/core/notification-item
---

## Overview

`LMNotificationFeedItem` is used to display notification. It includes information such as the notification message, the time of the notification, user details, and an optional media image. The view highlights whether the notification has been read.

<img
src={require('../../../../static/img/iOS/components/notificationView.webp').default}
alt="LMFeedNotificationView"
style={{border: '2px solid #d6d6d6'}}
/>

## Customisation

Below is the list of properties accepted by the `LMNotificationFeedItem`

| Property   | Type                                              | Description                          |
| ---------- | ------------------------------------------------- | ------------------------------------ |
| `activity` | [`LMActivityUI`](../Models/LMActivityViewData.md) | Prop for notification activity data. |
| `onTap`    | `Function`                                        | Prop for onTap event.                |
