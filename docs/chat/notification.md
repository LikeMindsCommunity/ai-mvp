---
sidebar_position: 10
title: Setup Notifications (Deprecated)
---

# Setup Notifications

:::warning

This method will be deprecated after 20th June 2024. Please check this guide to enable [notification](./notification-using-http-v1)

:::
We allow system notification for the chat related real time notifications to notify users about new chat and changes in the permission they have.

## Firebase Integration

LikeMind SDK requires your server key to send notification of messages or other things.

### Step 1: Generate Server Key for FCM

:::info
If you already have your server key, skip this step and go directly to `Step 2`
:::

1. Go to [Firebase Console](https://console.firebase.google.com/). If you don't have a Firebase project, please create a new project.

![FCM Server - Firebase Console](../static/img/fcm_server_key_1.png)

2. Select your project and move to **Project Overview**

3. Click on the settings icon and select **Project Settings**

![FCM Server - Project Settings](../static/img/fcm_server_key_2.png)

4. Go to **Cloud Messaging > Project credentials** and copy your server key.
   ![FCM Server - Server Key](../static/img/fcm_server_key_3.png)

### Step 2: Register Server key to LikeMinds Dashboard

1. Sign in to [dashboard](http://dashboard.likeminds.community/) and go to **Settings > General**

2. Add your server key in **Firebase Server Key**
   ![FCM Server - Server Key](../static/img/fcm_server_key_4.png)

## Frontend Side Integration

- To configure notifications for Android, head over to [this](./Android/push_notifications.md).
