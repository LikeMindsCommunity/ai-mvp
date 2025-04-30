---
# SDK: likeminds-docs-feed-android

# Summary
Directory: document_ingest/private_repo/likeminds-docs-feed-android
Files analyzed: 79

Estimated tokens: 61.5k

# Tree
Directory structure:
└── likeminds-docs-feed-android/
    └── feed/
        └── Android/
            ├── Theming.md
            ├── _category_.json
            ├── getting-started.md
            └── Core/
                ├── _category_.json
                ├── analytics.md
                ├── push_notification.md
                ├── Guides/
                │   ├── _category_.json
                │   ├── how-to-enable-personalised-feed.md
                │   ├── how-to-start-feed-with-specific-post_ids.md
                │   └── how-to-render-custom-post-ui/
                │       ├── how-to-render-custom-post-ui.md
                │       └── video-feed-example.md
                ├── Screens/
                │   ├── LMFeedActivityFeedFragment.md
                │   ├── LMFeedAdminDeleteDialogFragment.md
                │   ├── LMFeedCreatePollFragment.md
                │   ├── LMFeedCreatePostFragment.md
                │   ├── LMFeedEditPostFragment.md
                │   ├── LMFeedLikesFragment.md
                │   ├── LMFeedPollResultsFragment.md
                │   ├── LMFeedPostDetailFragment.md
                │   ├── LMFeedPostMenuBottomSheetFragment.md
                │   ├── LMFeedQnAFeedFragment.md
                │   ├── LMFeedReportFragment.md
                │   ├── LMFeedSearchFragment.md
                │   ├── LMFeedSelfDeleteDialogFragment.md
                │   ├── LMFeedSocialFeedFragment.md
                │   ├── LMFeedTopicSelectionFragment.md
                │   ├── LMFeedVideoFeedFragment.md
                │   └── Screens.md
                └── Widgets/
                    ├── LMFeedActivityView.md
                    ├── LMFeedAlertDialogView.md
                    ├── LMFeedHeaderView.md
                    ├── LMFeedLabelIconContainerView.md
                    ├── LMFeedLabelImageContainerView.md
                    ├── LMFeedNoEntityLayoutView.md
                    ├── LMFeedOverflowMenu.md
                    ├── LMFeedPostingView.md
                    ├── LMFeedSearchBarView.md
                    ├── LMFeedSearchListView.md
                    ├── LMFeedSnackbarView.md
                    ├── LMFeedSocialFeedListView.md
                    ├── LMFeedTopicSelectorBarView.md
                    ├── LMFeedUserView.md
                    ├── LMFeedViewMoreView.md
                    ├── _category_.json
                    ├── Comment/
                    │   ├── LMFeedCommentComposerView.md
                    │   ├── LMFeedCommentView.md
                    │   └── _category_.json
                    ├── Fundamentals/
                    │   ├── LMFeedButton.md
                    │   ├── LMFeedChip.md
                    │   ├── LMFeedChipGroup.md
                    │   ├── LMFeedEditText.md
                    │   ├── LMFeedFAB.md
                    │   ├── LMFeedIcon.md
                    │   ├── LMFeedImageView.md
                    │   ├── LMFeedProgressBar.md
                    │   ├── LMFeedSwitch.md
                    │   ├── LMFeedTextView.md
                    │   ├── LMFeedVideoView.md
                    │   └── _category_.json
                    ├── Poll/
                    │   ├── LMFeedPollOptionView.md
                    │   ├── LMFeedPollOptionsListView.md
                    │   ├── LMFeedPostPollView.md
                    │   └── _category_.json
                    └── Post/
                        ├── LMFeedPostDetailListView.md
                        ├── LMFeedPostHeaderView.md
                        ├── LMFeedPostTopResponseView.md
                        ├── _category_.json
                        ├── Action/
                        │   ├── LMFeedPostActionHorizontalView.md
                        │   ├── LMFeedPostActionVerticalView.md
                        │   ├── LMFeedPostQnAActionHorizontalView.md
                        │   └── _category_.json
                        └── Media/
                            ├── LMFeedPostDocumentView.md
                            ├── LMFeedPostDocumentsMediaView.md
                            ├── LMFeedPostImageMediaView.md
                            ├── LMFeedPostLinkMediaView.md
                            ├── LMFeedPostMultipleMediaView.md
                            ├── LMFeedPostVerticalVideoMediaView.md
                            ├── LMFeedPostVideoMediaView.md
                            └── _category_.json


# Content
================================================
File: feed/Android/Theming.md
================================================
---
sidebar_position: 2
title: Theming
slug: /android/theming
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Getting Started with Theming

The LikeMinds Feed SDK simplifies the process of customizing the appearance of all UI views. The SDK allows you to change the appearance of components such as colors and fonts with the help of dedicated class for theming `LMFeedAppearance`.

With `LMFeedAppearance`, you can adjust various aspects of UI widgets by defining attributes through `LMFeedAppearanceRequest`. LikeMinds Feed uses a top-level configuration to apply theming information throughout your application. You can customize the appearance of all UI widgets provided by the LikeMinds Feed SDK by adjusting properties such as button color, text link color, fonts, character limit in post, notification icon through the `LMFeedAppearance` class. To implement your custom appearance, create an instance of `LMFeedAppearanceRequest` and pass it when initializing the SDK with `LMFeedCore.setup()`.

## Detailed Overview of `LMFeedAppearanceRequest`

The `LMFeedAppearanceRequest` class allows you to create a request to customize various aspects of the LikeMinds Feed SDK's UI using builder pattern. By passing properties in the `LMFeedAppearanceRequest` class, you can control the appearance of all UI widgets to ensure a consistent appearance throughout your application.

### Font-related Attributes:

- `fontResource`: Set the font for your app by providing `@FontRes`.
- `fontAssetsPath`: Set the font for your app by providing the path of the font assests.

:::note
Choose either `fontResource` or `fontAssetsPath`. `fontResource` is preferred.
:::

### Color-related Attributes:

- `textLinkColor`: Set the color of link text throughout your app by providing `@ColorRes`.
- `buttonColor`: Set the color of clickables throughout your app by providing `@ColorRes`

### Other Attributes:

- `postCharacterLimit`: Set the maximum number of characters allowed in a post before the content is truncated.
- `postHeadingLimit`: Set the maximum number of characters allowed in a post heading before the heading is truncated.
- `notificationIcon`: Set the icon to be shown in the notifications by providing `@DrawableRes`.

:::note
`@FontRes` is an annotation used to indicate that a parameter is expected to reference a font resource. <br/>
`@ColorRes` indicates a parameter is expected to reference a color resource. <br/>
`@DrawableRes` indicates a parameter is expected to reference a drawable resource.
:::

## Applying `LMFeedAppearance` in your Application

Here’s an example of how to apply `LMFeedAppearance` using `LMFeedAppearanceRequest` while setting up `LMFeedCore` in your application class.


<Tabs>
<TabItem value="MyApplication.class" label="MyApplication.class">

```kotlin
val appearanceRequest = LMFeedAppearanceRequest.Builder()
    .fontResource(R.font.roboto)
    .textLinkColor(R.color.text_link_color)
    .buttonColor(R.color.button_color)
    .postCharacterLimit(200)
    .postHeadingLimit(100)
    .notificationIcon(R.drawable.ic_notification)
    .build()

LMFeedCore.setup(
    application = this,
    theme = LMFeedTheme.SOCIAL_FEED,
    enablePushNotifications = true,
    deviceId = deviceId,
    domain = "https://www.samplefeed.com",  // Change this as per your shareable domain
    lmFeedAppearance = appearanceRequest,
    lmFeedCoreCallback = this
)
```

</TabItem>
<TabItem value="colors.xml" label="colors.xml">

```xml
<resources>
    <color name="text_link_color">#007AFF</color>
    <color name="text_link_color">#5046E5</color>
</resources>
```

</TabItem>
</Tabs>

In this example, `LMFeedAppearanceRequest` is configured using the `lmFeedAppearance` parameter in the `LMFeedCore.setup()` method, applying the custom appearance globally.


================================================
File: feed/Android/_category_.json
================================================
{
  "label": "Android",
  "position": 2,
  "link": {
    "type": "generated-index",
    "description": "Android side documentation for Feed SDK"
  }
}



================================================
File: feed/Android/getting-started.md
================================================
---
sidebar_position: 1
title: Getting Started
slug: /android/getting-started
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Getting Started

The LikeMinds Android Feed SDK empowers you to integrate personalized and engaging feeds into your Android application, enhancing user experiences and driving user engagement. This guide will walk you through the steps to get started with the LikeMinds Android Feed SDK and set up a dynamic feed in your application. Obtain the necessary API key from the [LikeMinds dashboard](https://dashboard.likeminds.community).

## Prerequisites

Before you begin, ensure that you have the following:

1. **Kotlin Version**: Your project's kotlin version should be greater than **1.6.0**.
2. **Minimun Android SDK Version**: `minSdk` should be atleast **21**.
3. **Dependency Resolution Management**: `mavenCentral()` and `jitpack.io` should be mentioned in `dependencyResolutionManagement`.

## Step-by-Step Integration Guide

Follow these steps to integrate the LikeMinds Feed SDK into your Android application using MavenCentral:

### Step 1 - Installation

Implement `likeminds-feed-core` project in your app level `build.gradle`.

```groovy
dependencies {
    ...
    implementation 'community.likeminds:likeminds-feed-core:1.8.0'
}
```

:::note
Set `dataBinding true` in your app level `build.gradle` if not done already.
:::

**Now, sync the gradle before moving to next step.**

### Step 2 - Setup LikeMinds Feed

Initiate `LMFeedCore` in `onCreate()` method of the Application class using the following code:

<Tabs groupId="language" queryString>
<TabItem value="kotlin" label="Kotlin">

```kotlin
val application = this
val theme = LMFeedTheme.SOCIAL_FEED
val enablePushNotifications = false
val deviceId = null
val domain = "ENTER YOUR DOMAIN HERE"
val lmFeedCoreCallback = null

LMFeedCore.setup(
    application = application,
    theme,
    enablePushNotifications = enablePushNotifications,
    deviceId = deviceId,
    domain = domain,
    lmFeedCoreCallback = lmFeedCoreCallback
)
```

</TabItem>
<TabItem value="java" label="Java">

```java
Application applicationInstance = this; // instance of your application
LMFeedTheme theme = LMFeedTheme.SOCIAL_FEED; // theme selected for your app
String domain = "ENTER YOUR DOMAIN HERE"; // your domain
boolean enablePushNotifications = false; // whether to enable push notifications or not
String deviceId = null; // id of the device
LMFeedAppearanceRequest appearanceRequest = new LMFeedAppearanceRequest.Builder().build(); // object of [LMFeedAppearanceRequest]
LMFeedCoreCallback coreCallback = null; // object of feed core callback

LMFeedCore.INSTANCE.setup(
    applicationInstance, // instance of the application
    theme,
    domain, // your domain
    enablePushNotifications, // enable push notifications
    deviceId, // device id
    appearanceRequest, // object of [LMFeedAppearanceRequest] to set appearance of Feed
    coreCallback // callback for various operations in SDK
);
```

</TabItem>
</Tabs>

| **VARIABLE**              | **TYPE**                | **DESCRIPTION**                                       | **OPTIONAL** |
| :------------------------ | :---------------------- | :---------------------------------------------------- | :----------: |
| `application`             | Application             | Instance of your application class.                   |              |
| `theme`                   | LMFeedTheme             | Theme selected for theme.                             |              |
| `domain`                  | String                  | Your domain url.                                      |      ✔       |
| `enablePushNotifications` | Boolean                 | Whether to enable push notifications or not           |      ✔       |
| `deviceId`                | String                  | Unique Id of the device, if notifications are enabled |      ✔       |
| `lmFeedAppearance`        | LMFeedAppearanceRequest | Request object to set appearance of the Feed.         |      ✔       |
| `lmFeedCoreCallback`      | LMFeedCoreCallback      | Callback for various operations in SDK .              |      ✔       |

### Step 3 - Initiate User Session

You have successfully initiated the `LMFeedCore`. Now, you have to initiate a user session. Provide API Key directly to LikeMinds Feed SDK, which will be used to initiate a user session by calling `LMFeedCore.showFeed()`.

<Tabs groupId="language" queryString>
<TabItem value="kotlin" label="Kotlin">

```kotlin
val apiKey = "Your generated API key" // api key generated from the dashboard
val userName = "ENTER USER NAME" // name of the user
val userId = "ENTER USER ID" // id of the user
val context = this // instance of context

val successCallback = { response : UserResponse? ->
    //user session initiated successfully, write your logic here
    Unit
} // callback triggered when the initiate user call is successful

val failureCallback = { errorMessage ->
  Log.e("Example", errorMessage)
  Unit
} // callback triggered when the initiate user call fails

LMFeedCore.showFeed(
    context = context,
    apiKey = apiKey,
    uuid = userId,
    userName = userName,
    success = successCallback,
    error = failureCallback
)
```

</TabItem>
<TabItem value="java" label="Java">

```java
String apiKey = "Your generated API key"; // api key generated from the dashboard
String userId = "ENTER USER ID"; // id of the user
String userName = "ENTER USER NAME"; // name of the user
Context context = this;

LMFeedCore.INSTANCE.showFeed(
    context,
    apiKey,
    userId,
    userName,
    (UserResponse response) -> {
        // callback triggered when the initiate user call is successful, write your logic here
        return null;
    },
    (String error) -> {
        // callback triggered when the initiate user call fails
        Log.e("Example", error);
        return null;
    }
);
```

</TabItem>
</Tabs>

:::tip
For enhanced security, you can use [**Server Side User Authentication**](../server-side-user-auth.md) to initiate user sessions through your own server.
:::

### Step 4 - Navigation to the feed

Once you have initiated the user session, you can navigate the user to your Feed in the above mentioned `successCallback` to be passed in `LMFeedCore.showFeed()`. LikeMinds provide various Feed Themes to which you can navigate with the help of following code:

<Tabs groupId="feed-theme" queryString>
<TabItem value="social-feed" label="Social Feed">

<Tabs groupId="language" queryString>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate social feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedSocialFeedFragment.getInstance()

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedSocialFeedFragment.getInstance(LMFeedType.UNIVERSAL_FEED))).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>

<TabItem value="video-feed" label="Video Feed">

<Tabs groupId="language" queryString>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate video feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedVideoFeedFragment.getInstance()

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedVideoFeedFragment.getInstance(LMFeedType.UNIVERSAL_FEED, null)).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>

<TabItem value="qna-feed" label="QnA Feed">

<Tabs groupId="language" queryString>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate qna feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedQnAFeedFragment.getInstance()

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedQnAFeedFragment.getInstance(LMFeedType.UNIVERSAL_FEED)).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>
</Tabs>

That's it! You have successfully integrated the LikeMinds Feed SDK into your Android application. The next step would be to explore additional customization options or configurations provided by the SDK to tailor the feed to your application's needs.



================================================
File: feed/Android/Core/_category_.json
================================================
{
  "label": "Core",
  "position": 3,
  "link": {
    "type": "generated-index",
    "description": "Android side documentation for Feed SDK"
  }
}



================================================
File: feed/Android/Core/analytics.md
================================================
---
sidebar_position: 5
title: Analytics
slug: /android/analytics
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Analytics

The LikeMinds SDK provides a set of predefined user events that you might want to track for your feed application.

Refer to [Analytics Events](../analytics_events) to see the list of events that are being tracked.

## Callback

To receive these analytics events and handle them according to your requirements implement `LMFeedCoreCallback`.

While setting up LikeMinds Feed SDK in `onCreate()` method of the Application class, extend `LMFeedCoreCallback` and pass the instance of the same in `LMFeedCore.setup()`.

```kotlin
interface LMFeedCoreCallback{
        fun trackEvent(eventName: String, eventProperties: Map<String, String?> = mapOf())  // will be triggered when an event is called.
}
```

- `eventName`: Name of the event triggered.
- `eventProperties` : All the properties associated with that particular event.

## Example Implementation

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
val application = this
val enablePushNotifications = false
val deviceId = null
val domain = "ENTER YOUR DOMAIN NAME HERE"

val lmFeedCoreCallback = object : LMFeedCoreCallback {
    override fun trackEvent(eventName: String, eventProperties: Map<String, String?>) {
        // your implementation for analytics
    }
}

LMFeedCore.setup(
    application = application,
    enablePushNotifications = enablePushNotifications,
    deviceId = deviceId,
    domain = domain,
    lmFeedCoreCallback = lmFeedCoreCallback
)
```

</TabItem>
<TabItem value="java" label="Java">

```java
Application application = this; // instance of the application
LMFeedSetThemeRequest feedTheme = null; // instance of the theme
String domain = "ENTER YOUR DOMAIN NAME"; // domain of the app
boolean enablePushNotifications = false; // enable or disable push notifications
String deviceId = null; // device id of the user

LMFeedCoreCallback lmFeedCoreCallback = new LMFeedCoreCallback() {
    @Override
    public void trackEvent(@NonNull String eventName, @NonNull Map<String, String> eventProperties) {
        // your implementation for analytics
    }
};


LMFeedCore.INSTANCE.setup(
    application,
    lmFeedCoreCallback,
    feedTheme,
    domain,
    enablePushNotifications,
    deviceId
);
```

</TabItem>
</Tabs>



================================================
File: feed/Android/Core/push_notification.md
================================================
---
sidebar_position: 4
title: Push Notification
slug: /android/push-notification
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Push Notifications

Push notifications allow you to engage users and deliver timely updates and alerts, even when your app is not running. This guide outlines the steps to integrate push notification functionality for LikeMinds Feed SDK in your app.

Refer to [Notification List](../../notification-list.md) to see the list of notifications triggered.

## Prerequisites

Before proceeding with the integration, make sure you have the following prerequisites in place:

- **FCM Service Account Keys**: Obtain the Firebase Cloud Messaging service account keys from the Firebase Console. [Here](../../notification-using-http-v1.md) is the guide to obtain the same.
  
## Implementation

### Step 1 - Enable Push Notification and Share Device Id

While setting up LikeMinds Feed SDK in `onCreate()` method of the Application class, send `enablePushNotifications` as `true` and user's `deviceId` in `LMFeedCore.setup()`

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
val application = this
val enablePushNotifications = false
val deviceId = "ENTER USER'S DEVICE ID"
val domain = "ENTER YOUR DOMAIN HERE"

val lmFeedCoreCallback = object : LMFeedCoreCallback {}

LMFeedCore.setup(
    application = application,
    enablePushNotifications = enablePushNotifications,
    deviceId = deviceId,
    domain = domain,
    lmFeedCoreCallback = lmFeedCoreCallback
)
```

</TabItem>
<TabItem value="java" label="Java">

```java
Application application = this; // instance of the application
LMFeedSetThemeRequest feedTheme = null; // instance of the theme
String domain = "ENTER YOUR DOMAIN"; // domain of the app
boolean enablePushNotifications = true; // enable or disable push notifications
String deviceId = "ENTER USER'S DEVICE ID"; // device id of the user

LMFeedCoreCallback lmFeedCoreCallback = new LMFeedCoreCallback() {};

LMFeedCore.INSTANCE.setup(
    application,
    lmFeedCoreCallback,
    feedTheme,
    domain,
    enablePushNotifications,
    deviceId
);
```
</TabItem>
</Tabs>

### Step 2 - Handle Notification in FirebaseMessagingService

1. Create a class which extends `FirebaseMessagingService` (if not already present) which will receive the triggered notification.

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
class MessagingService: FirebaseMessagingService() {
    override fun onCreate() {
        super.onCreate()
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public class MessagingService extends FirebaseMessagingService {
    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage message) {
        super.onMessageReceived(message);
    }
}

```
</TabItem>
</Tabs>

2. Create a instance of `LMFeedNotificationHandler` in the `onCreate()` method of the Service

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
class MessagingService: FirebaseMessagingService() {

    private lateinit var mNotificationHandler: LMFeedNotificationHandler

    override fun onCreate() {
        super.onCreate()
        mNotificationHandler = LMFeedNotificationHandler.getInstance()
        mNotificationHandler.create(this.application)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public class MessagingService extends FirebaseMessagingService {
    LMFeedNotificationHandler mNotificationHandler;

    @Override
    public void onCreate() {
        super.onCreate();
        mNotificationHandler = LMFeedNotificationHandler.getInstance();
        mNotificationHandler.create(this.getApplication());
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage message) {
        super.onMessageReceived(message);
    }
}

```
</TabItem>
</Tabs>

3. Add `handleNotification()` method in `onMessageReceived()` method and pass the data received in the same function.

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
class MessagingService: FirebaseMessagingService() {

    private lateinit var mNotificationHandler: LMFeedNotificationHandler

    override fun onCreate() {
        super.onCreate()
        mNotificationHandler = LMFeedNotificationHandler.getInstance()
        mNotificationHandler.create(this.application)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        mNotificationHandler.handleNotification(message.data)
    }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public class MessagingService extends FirebaseMessagingService {
    LMFeedNotificationHandler mNotificationHandler;

    @Override
    public void onCreate() {
        super.onCreate();
        mNotificationHandler = LMChatNotificationHandler.getInstance();
        mNotificationHandler.create(this.getApplication());
    }

    @Override
    public void onMessageReceived(@NonNull RemoteMessage message) {
        super.onMessageReceived(message);
        mNotificationHandler.handleNotification(message.getData());
    }
}
```
</TabItem>
</Tabs>


================================================
File: feed/Android/Core/Guides/_category_.json
================================================
{
  "label": "Guides",
  "position": 3,
  "link": {
    "type": "generated-index",
    "description": "Android side documentation for Feed SDK"
  }
}



================================================
File: feed/Android/Core/Guides/how-to-enable-personalised-feed.md
================================================
---
sidebar_position: 2
title: How to enable personalised feed?
slug: /android/core/guide/how-to-enable-personalised-feed
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# How to enable personalised feed?

## Introduction

In this guide, you'll learn how to enable and configure a personalized feed for users in your Android app using the LikeMinds Feed Android SDK. A personalized feed helps enhance user engagement by tailoring the content they see based on their preferences, interactions, and other metrics.

## Prerequisites

Before you begin, ensure the following

- **LikeMinds Feed Android SDK**: The SDK must be properly installed and initialized in your Android project. Refer to the [Installation Guide](../../getting-started.md).
- Basic knowledge of Postman or equivalent API testing tools.

## Steps to enable Personalised Feed

### Step 1: Enable Personalised Feed Setting

1. Open your [LikeMinds Admin Dashboard](https://dashboard.likeminds.community/home).
2. Navigate to [Feed Settings](https://dashboard.likeminds.community/feed/settings)
3. Enable "Personalised Feed" Settings.

![LikeMinds Dashboard](../../../../static/img/dashboard-enable-personalized-feed.png)

### Step 2: Set weigths for different metrics

Once, Personalized Feed is enabled, you can edit all the weights to the various metric to rank the feed as your user group and requirements.

![LikeMinds Dashboard](../../../../static/img/dashboard-add-weights.png)

### Step 3: Configure in Android Feed SDK

In the last step of [Getting Started Guide](../../getting-started.md#step-4---navigation-to-the-feed), send `feedType` as `LMFeedType.PERSONALISED_FEED` in `getInstance()` functions of the Fragments.

<Tabs>
<TabItem value="social-feed" label="Social Feed">

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate social feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedSocialFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED)

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedSocialFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED))).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>

<TabItem value="video-feed" label="Video Feed">

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate video feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedVideoFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED)

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedVideoFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED, null)).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>

<TabItem value="qna-feed" label="QnA Feed">

<Tabs>
<TabItem value="kotlin" label="Kotlin">

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate qna feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = LMFeedQnAFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED)

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

</TabItem>

<TabItem value="java" label="Java">

```java
// pass this callback to LMFeedCore.showFeed()
(UserResponse response) -> {
    // callback triggered when the initiate user call is successful
    try {
        getSupportFragmentManager().beginTransaction().replace(R.id.frame_layout, new LMFeedQnAFeedFragment.getInstance(LMFeedType.PERSONALISED_FEED)).commit();
    } catch (Exception e) {
        throw new RuntimeException(e);
    }
    // callback triggered when the initiate user call is successful, write your logic here
    return null;
}
```

</TabItem>
</Tabs>

</TabItem>
</Tabs>



================================================
File: feed/Android/Core/Guides/how-to-start-feed-with-specific-post_ids.md
================================================
---
sidebar_position: 3
title: How to start video feed with specific posts?
slug: /android/core/guide/how-to-start-feed-with-specific-posts
---

# How to Start Feed with Specific Posts?

Starting the feed from a specific post improves content discovery, especially when users land via shared links or post thumbnails. This guide shows how to use the LikeMinds Feed Android SDK to launch a feed that begins from a defined list of posts—ideal for video feed experiences.

## Prerequisites

Before you begin, ensure the following:

- **LikeMinds Feed Android SDK**: The SDK must be properly installed and initialized in your Android project. Refer to the [installation guide](../../getting-started.md) if needed.
- **Basic Understanding of Android**: Familiarity with Android Fragments and concepts of **Object-Oriented Programming (OOPS)**
- **Post ID(s)**: You must have the post ids of the specific posts you want to start the feed with.

## Steps to start the feed with specific post

### Step 1: Create instance of Video Feed Screen

1. Create an instance of [`LMFeedVideoFeedProps`](../Screens/LMFeedVideoFeedFragment.md#props) and pass the `postIds` you want to start the feed in `startFeedWithPostIds()`
2. Pass the created instance of [`LMFeedVideoFeedProps`](../Screens/LMFeedVideoFeedFragment.md#props) in `getInstance()` function to create an instance of the [**Video Feed Screen**](../Screens/LMFeedVideoFeedFragment.md).

```kotlin
val props = LMFeedVideoFeedProps.Builder()
        .startFeedWithPostIds(listOf(startFeedWithPostId))
        .build()

val fragment = LMFeedVideoFeedFragment.getInstance(
        feedType = LMFeedType.UNIVERSAL_FEED, // change to LMFeedType.PERSONALIZED_FEED based on your preference
        props = props
    )
```

### Step 2: Use the created instance to render the feed

Use the instance of fragment created in above step in `successCallback`, as mentioned in the last step of [Getting Started Guide](../../getting-started.md#step-4---navigation-to-the-feed).

```kotlin
// pass this successCallback to LMFeedCore.showFeed()
val successCallback = { response : UserResponse? ->
  // inflate video feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful
```

You can pass one or multiple post ids depending on your requirement. The feed will start from the first post in the list and flow naturally afterward.



================================================
File: feed/Android/Core/Guides/how-to-render-custom-post-ui/how-to-render-custom-post-ui.md
================================================
---
sidebar_position: 1
title: How to render Custom Post UI?
slug: /android/core/guide/how-to-render-custom-post-ui
---

# How to render Custom Post UI?

## Overview

The LikeMinds Feed SDK provides developers with the ability to render custom post UI. To use your own custom Post UI:

### 1. Create a custom xml layout as per your requirements

Create a new `layout` file as per your design requirements. While creating the layout file, make note of the following:

1. Wrap the whole layout within `<layout>` tags to enable `dataBinding` for the layout

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <!--    Rest of the layout-->

</layout>
```

2. Add `<data>` tags and add two variables as `position` and `postViewData` as below:

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">
    <data>

        <variable
            name="position"
            type="int" />

        <variable
            name="postViewData"
            type="com.likeminds.feed.android.core.socialfeed.model.LMFeedPostViewData" />
    </data>

    <!--    Rest of the layout-->

</layout>
```

| **VARIABLE**   | **TYPE**     | **DESCRIPTION**                                       | **OPTIONAL** |
| :------------- | :----------- | :---------------------------------------------------- | :----------: |
| `position`     | Int          | Position of the current item view                     |              |
| `postViewData` | PostViewData | Instance of the post to be inflated in the item view. |              |

### 2. Extend class `PostViewDataBinder` to create your own custom `ViewDataBinder`

After creating the `xml` layout, create a custom view data binder by extending `PostViewDataBinder`. While extending the same, pass the following:

1. Instance of `LMFeedPostAdapterListener`: for click listeners callbacks
2. Instance of `binding`: binding of the layout created in above step
3. Type of post through `viewType`

| **VIEW TYPE**                    | **POST TYPE**                                   |
| :------------------------------- | :---------------------------------------------- |
| `ITEM_POST_TEXT_ONLY`            | Post with text and no attachments               |
| `ITEM_POST_SINGLE_IMAGE`         | Post with text and a single image as attachment |
| `ITEM_POST_SINGLE_VIDEO`         | Post with text and a single video as attachment |
| `ITEM_POST_DOCUMENTS`            | Post with text and documents as attachment      |
| `ITEM_POST_LINK`                 | Post with text and link as attachment           |
| `ITEM_POST_MULTIPLE_MEDIA`       | Post with text and multiple attachments         |
| `ITEM_POST_POLL`                 | Post with text and poll as attachments          |
| `ITEM_POST_VIDEO_FEED`           | Post with text and reel as attachment           |
| `ITEM_POST_CUSTOM_WIDGET`        | Post with text and custom JSON object           |
| `ITEM_POST_VIDEO_FEED_CAUGHT_UP` | View when all the reels are viewed              |

```kotlin
class CustomViewDataBinder(private val postAdapterListener: LMFeedPostAdapterListener) :
    PostItemViewDataBinder<CreatedCustomBinding>(postAdapterListener) {
    override val viewType: Int
        get() = //add the view type from above table

    override fun createBinder(parent: ViewGroup): CreatedCustomBinding {
        //return the instance of the binding and add click listeners
    }

    override fun bindData(
        binding: CreatedCustomBinding,
        data: LMFeedPostViewData,
        position: Int
    ) {
        //bind the data with the layout and data variables
        binding.position = position
        binding.postViewData = data

        //Rest of the logic
    }
}
```

### 3. Replace the default post view witth custom post view

After creation of the custom view data binder, replace the default view data binder with the custom view data binder created above by extending relevant predefined theme fragment and override the `customize<Theme>ListView()` function as per the predefined theme used. And calling `replaceViewDataBinder()` of the adapter provided, in this function pass the `viewType` which is used in above step and the instance of the `CustomViewDataBinder`.      

```kotlin
class CustomFragment : ThemeFragment(), LMFeedPostAdapterListener  {

    override fun customize<Theme>ListView() {
        val customViewDataBinder = CustomViewDataBinder(this)
        <theme>Adapter.replaceViewDataBinder(viewType, customViewDataBinder)
    }
}
```

### 4. Inflate the Custom Fragment

Transact the custom fragment `CustomFragment()` created above in the `successCallback` of `LMFeedCore.showFeed()` which was used in the [Getting Started](../../../getting-started.md)

```kotlin
val successCallback = { response : UserResponse? ->
  // inflate universal feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = CustomFragment() //custom fragment created

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful

val failureCallback = { errorMessage ->
  Log.e("Example", errorMessage)
  Unit
} // callback triggered when the initiate user call fails

LMFeedCore.showFeed(
    context = context,
    apiKey = apiKey,
    uuid = userId,
    userName = userName,
    success = successCallback,
    error = failureCallback
)
```

## Example Implementation

For example implementations, continue on the next documents.


================================================
File: feed/Android/Core/Guides/how-to-render-custom-post-ui/video-feed-example.md
================================================
---
sidebar_position: 1
title: Example Implementation on Video Feed
slug: /android/core/guide/how-to-render-custom-post-ui/video-feed
---

Let's consider an example, on **Video Feed Theme**, where you want to add a CTA button for redirection to different above the link icon like this, using views and logic provided by LikeMinds Feed SDK.

<p align="center">
    <img
        src="/img/custom_widget_android_water.jpeg"
        alt="LMFeedLikeListScreen"
        width="180"
        />
</p>

## Create Custom Layout

To display the above layout, Create an `xml` file in `layout` folder as `item_custom_video_theme_view.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>

        <variable
            name="position"
            type="int" />

        <variable
            name="postViewData"
            type="com.likeminds.feed.android.core.socialfeed.model.LMFeedPostViewData" />
    </data>

    <androidx.constraintlayout.widget.ConstraintLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">

        <com.likeminds.feed.android.core.ui.widgets.post.postmedia.view.LMFeedPostVerticalVideoMediaView
            android:id="@+id/post_video_view"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent" />

        <com.likeminds.feed.android.core.ui.widgets.post.postheaderview.view.LMFeedPostHeaderView
            android:id="@+id/post_header"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginHorizontal="@dimen/lm_feed_large_margin"
            android:layout_marginBottom="@dimen/lm_feed_regular_margin"
            app:layout_constraintBottom_toTopOf="@id/tv_post_content"
            app:layout_constraintEnd_toStartOf="@id/post_action_view"
            app:layout_constraintStart_toStartOf="parent" />

        <com.likeminds.feed.android.core.ui.base.views.LMFeedChipGroup
            android:id="@+id/post_topics_group"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="@dimen/lm_feed_regular_margin"
            android:visibility="gone"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@id/post_header" />

        <com.likeminds.feed.android.core.ui.base.views.LMFeedTextView
            android:id="@+id/tv_post_content"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginStart="@dimen/lm_feed_large_margin"
            android:layout_marginEnd="@dimen/lm_feed_extra_extra_large_margin"
            android:layout_marginBottom="@dimen/lm_feed_large_margin"
            android:lineSpacingExtra="@dimen/lm_feed_line_spacing_extra_extra_small"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintEnd_toStartOf="@id/post_action_view"
            app:layout_constraintStart_toStartOf="parent"
            tools:fontFamily="@font/lm_feed_roboto"
            tools:textColor="@color/lm_feed_grey"
            tools:textSize="@dimen/lm_feed_text_large" />

        <androidx.constraintlayout.widget.ConstraintLayout
            android:id="@+id/post_action_view"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginEnd="@dimen/lm_feed_large_margin"
            android:layout_marginBottom="@dimen/lm_feed_vertical_post_action_bottom_margin"
            android:padding="@dimen/lm_feed_small_padding"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintEnd_toEndOf="parent"
            tools:background="?android:attr/selectableItemBackground">

            <com.likeminds.feed.android.core.ui.base.views.LMFeedIcon
                android:id="@+id/iv_cta"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="16dp"
                android:padding="@dimen/lm_feed_small_padding"
                android:scaleType="fitCenter"
                android:tint="@color/white"
                android:visibility="visible"
                app:layout_constraintBottom_toTopOf="@id/iv_like"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                app:srcCompat="@drawable/ic_video_feed_invest"
                tools:ignore="ContentDescription"
                tools:visibility="visible" />

            <com.likeminds.feed.android.core.ui.base.views.LMFeedIcon
                android:id="@+id/iv_like"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:padding="@dimen/lm_feed_small_padding"
                android:scaleType="fitCenter"
                android:visibility="visible"
                app:layout_constraintBottom_toTopOf="@id/tv_likes_count"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                tools:ignore="ContentDescription"
                tools:srcCompat="@drawable/lm_feed_ic_like_filled"
                tools:visibility="visible" />

            <com.likeminds.feed.android.core.ui.base.views.LMFeedTextView
                android:id="@+id/tv_likes_count"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="@dimen/lm_feed_medium_margin"
                android:foreground="?selectableItemBackground"
                android:textStyle="normal"
                android:visibility="visible"
                app:layout_constraintBottom_toTopOf="@id/iv_comment"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                tools:fontFamily="@font/lm_feed_roboto"
                tools:ignore="UnusedAttribute"
                tools:text="31k"
                tools:textColor="@color/lm_feed_grey"
                tools:textSize="@dimen/lm_feed_text_medium" />

            <com.likeminds.feed.android.core.ui.base.views.LMFeedIcon
                android:id="@+id/iv_post_menu"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:padding="@dimen/lm_feed_small_padding"
                android:scaleType="fitCenter"
                android:visibility="visible"
                app:layout_constraintBottom_toBottomOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintStart_toStartOf="parent"
                tools:ignore="ContentDescription,UnusedAttribute"
                tools:src="@drawable/lm_feed_ic_overflow_menu"
                tools:visibility="visible" />
        </androidx.constraintlayout.widget.ConstraintLayout>
    </androidx.constraintlayout.widget.ConstraintLayout>
</layout>
```

## Extend `PostViewDataBinder`

Once, layout file is created. Now create a `CustomVideoThemeViewDataBinder` which will extend `PostViewDataBinder` to get some default functionality and get `PostViewData` which will have all the data related to that post.

```kotlin
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import com.likeminds.feed.android.core.R
import com.likeminds.feed.android.core.socialfeed.adapter.LMFeedPostAdapterListener
import com.likeminds.feed.android.core.socialfeed.model.LMFeedPostViewData
import com.likeminds.feed.android.core.socialfeed.util.LMFeedPostBinderUtils
import com.likeminds.feed.android.core.utils.LMFeedStyleTransformer
import com.likeminds.feed.android.core.utils.LMFeedValueUtils.getFormatedNumber
import com.likeminds.feed.android.core.utils.base.PostItemViewDataBinder
import com.likeminds.feed.android.core.utils.base.model.ITEM_POST_VIDEO_FEED
import com.likeminds.feedvideo.databinding.ItemCustomReelsViewDataBinderBinding

class CustomVideoThemeViewDataBinder(
    private val postAdapterListener: LMFeedPostAdapterListener
) : PostItemViewDataBinder<ItemCustomVideoThemeViewBinding>(postAdapterListener) {

    override val viewType: Int
        get() = ITEM_POST_VIDEO_FEED

    override fun createBinder(parent: ViewGroup): ItemCustomVideoThemeViewBinding {
        val binding = ItemCustomVideoThemeViewBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )

        binding.apply {
            LMFeedPostBinderUtils.customizePostHeaderView(postHeader)

            LMFeedPostBinderUtils.customizePostContentView(tvPostContent)

            //set video media style to post video view
            val postVerticalVideoMediaStyle =
                LMFeedStyleTransformer.postViewStyle.postMediaViewStyle.postVerticalVideoMediaStyle
                    ?: return@apply

            postVideoView.setStyle(postVerticalVideoMediaStyle)

            LMFeedStyleTransformer.postViewStyle.postActionViewStyle.menuIconStyle?.let {
                ivPostMenu.setStyle(
                    it
                )
            }

            setClickListeners(this)
        }

        return binding
    }

    override fun bindData(
        binding: ItemCustomVideoThemeViewBinding,
        data: LMFeedPostViewData,
        position: Int
    ) {
        binding.apply {
            this.position = position
            postViewData = data

            val iconStyle = LMFeedStyleTransformer.postViewStyle.postActionViewStyle.likeIconStyle

            val likeIcon = if (data.actionViewData.isLiked) {
                iconStyle.activeSrc
            } else {
                iconStyle.inActiveSrc
            }

            if (likeIcon != null) {
                binding.ivLike.setImageDrawable(
                    ContextCompat.getDrawable(
                        root.context,
                        likeIcon
                    )
                )
            }

            val likesCount = data.actionViewData.likesCount

            val likesCountText = if (likesCount == 0) {
                root.context.getString(R.string.lm_feed_like)
            } else {
                likesCount.toLong().getFormatedNumber()
            }

            tvLikesCount.text = likesCountText

            // checks whether to bind complete data or not and execute corresponding lambda function
            LMFeedPostBinderUtils.setPostBindData(
                postHeader,
                tvPostContent,
                data,
                position,
                postTopicsGroup,
                postAdapterListener,
                returnBinder = {
                    return@setPostBindData
                }, executeBinder = {}
            )
        }
    }

    private fun setClickListeners(binding: ItemCustomVideoThemeViewBinding) {
        binding.apply {
            postHeader.setAuthorFrameClickListener {
                val post = this.postViewData ?: return@setAuthorFrameClickListener
                postAdapterListener.onPostAuthorHeaderClicked(position, post)
            }

            ivLike.setOnClickListener {
                val post = this.postViewData ?: return@setOnClickListener
                val updatedPost = LMFeedPostBinderUtils.updatePostForLike(post)
                postAdapterListener.onPostLikeClicked(position, updatedPost)
            }

            ivPostMenu.setOnClickListener {
                val post = this.postViewData ?: return@setOnClickListener
                postAdapterListener.onPostActionMenuClicked(position, post)
            }
        }
    }
}
```

## Replace Default Post View

Now, create a custom fragment to replace the default video theme view databinder and override `customizeVideoFeedListView()` and `replaceVideoView()`

```kotlin
import androidx.core.view.get
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import com.likeminds.feed.android.core.socialfeed.model.LMFeedPostViewData
import com.likeminds.feed.android.core.ui.widgets.post.postmedia.view.LMFeedPostVerticalVideoMediaView
import com.likeminds.feed.android.core.utils.base.LMFeedDataBoundViewHolder
import com.likeminds.feed.android.core.utils.base.model.ITEM_POST_VIDEO_FEED
import com.likeminds.feed.android.core.videofeed.adapter.LMFeedVideoFeedAdapter
import com.likeminds.feed.android.core.videofeed.view.LMFeedVideoFeedFragment
import com.likeminds.feedvideo.databinding.ItemCustomReelsViewDataBinderBinding

class CustomVideoFeedFragment : LMFeedVideoFeedFragment() {

    override fun customizeVideoFeedListView(
        vp2VideoFeed: ViewPager2,
        videoFeedAdapter: LMFeedVideoFeedAdapter
    ) {
        val customVideoThemeViewDataBinder = CustomVideoThemeViewDataBinder(this)
        videoFeedAdapter.replaceViewDataBinder(ITEM_POST_VIDEO_FEED, customVideoThemeViewDataBinder)
    }

    override fun replaceVideoView(position: Int): LMFeedPostVerticalVideoMediaView? {
        //get the video feed binding to play the view in [postVideoView]
        val videoFeedBinding =
            ((binding.vp2VideoFeed[0] as? RecyclerView)?.findViewHolderForAdapterPosition(position) as? LMFeedDataBoundViewHolder<*>)
                ?.binding as? ItemCustomReelsViewDataBinderBinding ?: return null

        return (videoFeedBinding.postVideoView)
    }
}
```

## Inflate the `CustomVideoFeedFragment`

Transact the custom fragment `CustomVideoFeedFragment()` created above in the `successCallback` of `LMFeedCore.showFeed()` which was used in the [Getting Started](../../../getting-started.md)

```kotlin
val successCallback = { response : UserResponse? ->
  // inflate universal feed fragment in your activity
  val containerViewId = R.id.frame_layout
  val fragment = CustomVideoFeedFragment() //custom fragment created

  val transaction = supportFragmentManager.beginTransaction()
  transaction.replace(containerViewId, fragment, containerViewId.toString())
  transaction.commit()
  Unit
} // callback triggered when the initiate user call is successful

val failureCallback = { errorMessage ->
  Log.e("Example", errorMessage)
  Unit
} // callback triggered when the initiate user call fails

LMFeedCore.showFeed(
    context = context,
    apiKey = apiKey,
    uuid = userId,
    userName = userName,
    success = successCallback,
    error = failureCallback
)
```



================================================
File: feed/Android/Core/Screens/LMFeedActivityFeedFragment.md
================================================
---
sidebar_position: 2
title: Activity Feed Screen
slug: /android/core/screens/activity-feed-screen
---

# Screen: LMFeedActivityFeedFragment

The `LMFeedActivityFeedFragment` is a core component of the LikeMinds feed system, responsible for displaying activity feeds within the app. It enables users to view and interact with activity feed items while supporting customization and interaction handling.

**GitHub File**: [LMFeedActivityFeedFragment.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/activityfeed/view/LMFeedActivityFeedFragment.kt)

---

## View Style: LMFeedActivityFeedFragmentViewStyle

The `LMFeedActivityFeedFragmentViewStyle` defines the visual style and structure of the `LMFeedActivityFeedFragment`, including headers, activity views, and layout styling.

**GitHub File**: [LMFeedActivityFeedFragmentViewStyle.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/activityfeed/style/LMFeedActivityFeedFragmentViewStyle.kt)

| Field                        | Description                                          | Type                                   |
|------------------------------|------------------------------------------------------|----------------------------------------|
| `headerViewStyle`            | Style attributes for the header view.               | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md) |
| `activityViewStyle`          | Defines the style for activity views.               | [LMFeedActivityViewStyle](../Widgets/LMFeedActivityView.md) |
| `noActivityLayoutViewStyle`  | Style for the "No Activity" layout.                 | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md) |
| `backgroundColor`            | Background color for the fragment.                  | `Color` |

---

## Customization Available in LMFeedActivityFeedFragment

The fragment provides the following customization methods:

### Header Customizations
- **customizeActivityFeedHeaderView(headerView: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):**  
  Customize the appearance and functionality of the header view in the activity feed.

### Layout Customizations
- **customizeNoTopicsLayout(layoutNoTopics: [LMFeedNoEntityLayoutView](../Widgets/LMFeedNoEntityLayoutView.md)):**  
  Customize the layout displayed when there are no topics available in the activity feed.

---

## Interactions Available in LMFeedActivityFeedFragment

The fragment supports the following interaction methods:

### Item Click Interactions
- **`onActivityFeedItemClicked(position: Int, activityFeedItem: LMFeedActivityViewData)`**  
  Handles click events for individual activity feed items, allowing developers to respond to user interactions.

---





================================================
File: feed/Android/Core/Screens/LMFeedAdminDeleteDialogFragment.md
================================================
---
sidebar_position: 3
title: Admin Delete Dialog
slug: /android/core/screens/admin-delete-dialog
---

# Screen: LMFeedAdminDeleteDialogFragment

The `LMFeedAdminDeleteDialogFragment` handles the administrative delete dialog in the LikeMinds feed system. It enables administrators to confirm or cancel delete operations within the feed, providing a flexible and customizable user experience.

**GitHub File**: [LMFeedAdminDeleteDialogFragment.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/delete/view/LMFeedAdminDeleteDialogFragment.kt)

---

## View Style: LMFeedAdminDeleteDialogFragmentStyle

The `LMFeedAdminDeleteDialogFragmentStyle` defines the visual style and structure of the `LMFeedAdminDeleteDialogFragment`. It provides various customization options for the dialog and its components.

**GitHub File**: [LMFeedAdminDeleteDialogFragmentStyle.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/delete/style/LMFeedAdminDeleteDialogFragmentStyle.kt)

| Field                 | Description                                          | Type                                   |
|-----------------------|------------------------------------------------------|----------------------------------------|
| `adminDeleteDialogStyle` | Style attributes for the admin delete dialog.      | [LMFeedAlertDialogViewStyle](../Widgets/LMFeedAlertDialogView.md)             |
| `selectorIconStyle`      | Defines the style for selector icons.              | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md)                        |
| `reasonTextStyle`        | Style for the text displaying reasons in the dialog.| [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                        |

---

## Customization Available in LMFeedAdminDeleteDialogFragment

The fragment provides the following customization methods:

### Dialog Customizations
- **customizeAdminDeleteDialog(dialog: [LMFeedAlertDialogView](../Widgets/LMFeedAlertDialogView.md)):**  
  Customize the appearance and behavior of the admin delete dialog, including its layout and components.

---

## Interactions Available in LMFeedAdminDeleteDialogFragment

The fragment supports the following interaction methods:

### Selector Click Interactions
- **`onAdminDeleteAlertSelectorClicked()`**  
  Handles clicks on selector options within the delete dialog.

### Button Click Interactions
- **`onAdminDeleteAlertPositiveButtonClicked()`**  
  Handles the confirmation of a delete operation when the positive button is clicked.

- **`onAdminDeleteAlertNegativeButtonClicked()`**  
  Handles the cancellation of a delete operation when the negative button is clicked.




================================================
File: feed/Android/Core/Screens/LMFeedCreatePollFragment.md
================================================
---
sidebar_position: 6
title: Create Poll Screen
slug: /android/core/screens/feed-create-poll-screen
---

# Screen: LMFeedCreatePollFragment

`LMFeedCreatePollFragment` allows users to create polls within the LikeMinds feed system. It provides an interface for adding poll questions, options, and configuring advanced settings like expiration time and anonymous voting.  
[GitHub Link to LMFeedCreatePollFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/poll/create/view/LMFeedCreatePollFragment.kt)

---

## View Style: LMFeedCreatePollFragmentViewStyle

`LMFeedCreatePollFragmentViewStyle` defines the visual style and structure of the LMFeedCreatePollFragment. The following fields are available for customization:

| **Field Name**                     | **Description**                                              | **Type**                      |
|------------------------------------|--------------------------------------------------------------|-------------------------------|
| `headerViewStyle`                  | Style for the header of the create poll screen.              | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)       |
| `authorViewStyle`                  | Defines the style for the author view.                       | [LMFeedPostHeaderViewStyle](../Widgets/Post/LMFeedPostHeaderView.md)   |
| `pollQuestionTitleViewStyle`       | Style for the poll question title.                           | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollQuestionViewStyle`            | Style for the poll question input field.                     | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)         |
| `pollOptionsTitleViewStyle`        | Style for the poll options title.                            | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollAddOptionViewStyle`           | Style for the "add poll option" button.                      | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollExpiryTimeTitleViewStyle`     | Style for the poll expiry time title.                        | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollExpiryTimeViewStyle`          | Style for the poll expiry time selector.                     | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollAdvanceOptionViewStyle`       | Style for advanced options section.                          | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `pollAdvanceOptionSwitchViewStyle` | Style for the advanced option toggle switches.               | [LMFeedSwitchStyle](../Widgets/Fundamentals/LMFeedSwitch.md)           |
| `pollOptionsViewStyle`             | Style for the list of poll options.                          | [LMFeedCreatePollOptionViewStyle](../Widgets/Poll/LMFeedPollOptionView.md) |
| `pollDropdownViewStyle`            | Style for dropdown menus in the poll creation screen.        | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |

[GitHub Link to LMFeedCreatePollFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/poll/create/style/LMFeedCreatePollFragmentViewStyle.kt)

---

## Customization available in LMFeedCreatePollFragment

### Header Customizations  
- **customizeCreatePollHeader(headerView: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** 
    Allows customization of the poll creation header.

### Author View Customizations  
- **customizeAuthorView(authorView: [LMFeedPostHeaderView](../Widgets/Post/LMFeedPostHeaderView.md)):** 
    Customizes the appearance of the author view.

### Poll Content Customizations  
- **customizePollQuestion(tvPollQuestionTitle: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md), etPollQuestion: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md)):** 
    Customizes the input field for the poll question.  
- **customizePollOptions(tvPollOptionsTitle: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md), tvAddOption: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** 
    Customizes the poll options layout.  
- **customizePollExpiryTime(tvPollExpiryTitle: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md), tvPollExpiryTime: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** 
    Customizes the poll expiry time selector.

### Advanced Options Customizations  
- **customizeAdvancedOptionTitle(tvAdvancedOptions: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** 
    Customizes the title for advanced options.  
- **customizeAdvanceOptionSwitchOptions(switchAnonymousPoll: [LMFeedSwitch](../Widgets/Fundamentals/LMFeedSwitch.md), switchLiveResults: [LMFeedSwitch](../Widgets/Fundamentals/LMFeedSwitch.md), switchAddNewOptions: [LMFeedSwitch](../Widgets/Fundamentals/LMFeedSwitch.md)):** 
    Customizes the toggle switches for advanced options.

---

## Interactions available in LMFeedCreatePollFragment

### Navigation Interactions  
- `onNavigationIconClicked()`: Handles clicks on the navigation icon.

### Poll Option Interactions  
- `onAddPollOptionClicked()`: Handles adding a new poll option.

### Poll Settings Interactions  
- `onPollExpiryTimeClicked()`: Handles the selection of poll expiry time.  
- `onAdvancedSettingsClicked()`: Handles clicks on the advanced settings button.  

### Submission Interactions  
- `onPollSubmitClicked()`: Handles the submission of the created poll.





================================================
File: feed/Android/Core/Screens/LMFeedCreatePostFragment.md
================================================
---
sidebar_position: 8
title: Create Post Screen
slug: /android/core/screens/feed-create-post-screen
---

# Screen: LMFeedCreatePostFragment

`LMFeedCreatePostFragment` provides the interface for creating new posts in the LikeMinds feed system. It supports various post types, including text, images, videos, documents, and polls, allowing users to compose rich content with advanced customization options.  
[GitHub Link to LMFeedCreatePostFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/create/view/LMFeedCreatePostFragment.kt)

---

## View Style: LMFeedCreatePostFragmentViewStyle

`LMFeedCreatePostFragmentViewStyle` defines the visual style and structure of the LMFeedCreatePostFragment. The following fields are available for customization:

| **Field Name**              | **Description**                                              | **Type**                     |
|-----------------------------|--------------------------------------------------------------|------------------------------|
| `headerViewStyle`           | Style for the header of the create post screen.              | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)      |
| `authorViewStyle`           | Defines the style for the author view.                       | [LMFeedPostHeaderViewStyle](../Widgets/Post/LMFeedPostHeaderView.md)  |
| `selectTopicsChipStyle`     | Style for the topic selection chip.                          | [LMFeedChipStyle](../Widgets/Fundamentals/LMFeedChip.md)            |
| `editChipStyle`             | Style for the edit chip in the post composer.                | [LMFeedChipStyle](../Widgets/Fundamentals/LMFeedChip.md)            |
| `postComposerStyle`         | Style for the main post composer.                            | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)        |
| `postHeadingComposerStyle`  | Style for the heading composer in posts.                     | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)        |
| `postHeadingLimitTextStyle` | Style for the heading character limit display.               | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)            |
| `addMoreButtonStyle`        | Style for the "Add More" button.                             | [LMFeedButtonStyle](../Widgets/Fundamentals/LMFeedButton.md)          |
| `backgroundColor`           | Background color for the create post fragment.               | `Int`                        |

[GitHub Link to LMFeedCreatePostFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/create/viewstyle/LMFeedCreatePostFragmentViewStyle.kt)

---

## Customization available in LMFeedCreatePostFragment

### Header Customizations  
- **customizeCreatePostHeaderView(headerViewCreatePost: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** Allows customization of the header view in the create post fragment.

### Author and Topics Customizations  
- **customizeAuthorView(authorView: [LMFeedPostHeaderView](..//Widgets/Post/LMFeedPostHeaderView.md)):** Customizes the author view in the post composer.  
- **customizeTopicsGroup(topicsGroup: [LMFeedChipGroup](../Widgets/Fundamentals/LMFeedChipGroup.md)):** Customizes the topics group in the post composer.

### Post Content Customizations  
- **customizePostComposer(etPostComposer: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md)):** Customizes the main post composer for text content.  
- **customizePostHeadingComposer(etPostHeadingComposer: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md)):** Customizes the heading composer.  
- **customizePostHeadingLimit(tvPostHeadingLimitTextView: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** Customizes the display of character limits for post headings.

### Attachments Customizations  
- **customizePostImageAttachment(imageMediaView: [LMFeedPostImageMediaView](../Widgets/Post/Media/LMFeedPostImageMediaView.md)):** Customizes the image attachment section.  
- **customizePostVideoAttachment(videoMediaView: [LMFeedPostVideoMediaView](../Widgets/Post/Media/LMFeedPostVideoMediaView.md)):** Customizes the video attachment section.  
- **customizePostLinkViewAttachment(linkMediaView: [LMFeedPostLinkMediaView](../Widgets/Post/Media/LMFeedPostLinkMediaView.md)):** Customizes the link view attachment section.  
- **customizePostDocumentsAttachment(documentsMediaView: [LMFeedPostDocumentsMediaView](../Widgets/Post/Media/LMFeedPostDocumentsMediaView.md)):** Customizes the document attachment section.  
- **customizePostPollAttachment(pollView: [LMFeedPostPollView](../Widgets/Poll/LMFeedPostPollView.md)):** Customizes the poll attachment section.  
- **customizePostMultipleMedia(multipleMediaView: [LMFeedPostMultipleMediaView](../Widgets/Post/Media/LMFeedPostMultipleMediaView.md)):** Customizes the display of multiple media attachments.  
- **customizeAddMoreButton(btnAddMoreMedia: [LMFeedButton](../Widgets/Fundamentals/LMFeedButton.md)):** Customizes the "Add More" button for additional attachments.

---

## Interactions available in LMFeedCreatePostFragment

### Media Attachments Interactions  
- **onAttachImageClicked():** Handles clicks for attaching images.  
- **onAttachVideoClicked():** Handles clicks for attaching videos.  
- **onAttachDocumentClicked():** Handles clicks for attaching documents.  

### Poll Attachments Interactions  
- **onAddPollClicked():** Handles adding a new poll to the post.  
- **onPollAttachmentEditClicked():** Handles editing the poll attachment.

### Media and Document Interactions  
- **onPostDocumentMediaClicked(position: Int, parentPosition: Int, attachmentViewData: LMFeedAttachmentViewData):** Handles clicks on document or media attachments in the post.  
- **onMediaRemovedClicked(position: Int, mediaType: String):** Handles removal of media attachments.




================================================
File: feed/Android/Core/Screens/LMFeedEditPostFragment.md
================================================
---
sidebar_position: 10
title: Post Edit Screen
slug: /android/core/screens/post-edit-screen
---

# Screen: LMFeedEditPostFragment

`LMFeedEditPostFragment` provides an interface for editing existing posts in the LikeMinds feed system. It supports modifying text, images, videos, documents, and polls within a post.  
[GitHub Link to LMFeedEditPostFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/edit/view/LMFeedEditPostFragment.kt)

---

## View Style: LMFeedEditPostFragmentViewStyle

`LMFeedEditPostFragmentViewStyle` defines the visual style and structure of the LMFeedEditPostFragment. The following fields are available for customization:

| **Field Name**                  | **Description**                                              | **Type**                      |
|---------------------------------|--------------------------------------------------------------|-------------------------------|
| `headerViewStyle`               | Style for the header of the edit post screen.                | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)       |
| `postHeaderViewStyle`           | Style for the post header view.                              | [LMFeedPostHeaderViewStyle](../Widgets/Post/LMFeedPostHeaderView.md)   |
| `postComposerStyle`             | Style for the main post composer.                            | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)         |
| `postHeadingComposerStyle`      | Style for the heading composer in posts.                     | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)         |
| `postHeadingLimitTextStyle`     | Style for the heading character limit display.               | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)             |
| `progressBarStyle`              | Style for the progress bar used during edits.                | [LMFeedProgressBarStyle](../Widgets/Fundamentals/LMFeedProgressBar.md)      |
| `selectTopicsChipStyle`         | Style for the topic selection chip.                          | [LMFeedChipStyle](../Widgets/Fundamentals/LMFeedChip.md)             |
| `editTopicsChipStyle`           | Style for the edit topics chip.                              | [LMFeedChipStyle](../Widgets/Fundamentals/LMFeedChip.md)             |
| `disabledTopicsAlertDialogStyle`| Style for the alert dialog when topics are disabled.         | [LMFeedAlertDialogViewStyle](../Widgets/LMFeedAlertDialogView.md)  |

[GitHub Link to LMFeedEditPostFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/edit/style/LMFeedEditPostFragmentViewStyle.kt)

---

## Customization available in LMFeedEditPostFragment

### Header Customizations  
- **customizeEditPostHeaderView(headerViewEditPost: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** Allows customization of the edit post header.

### Post Content Customizations  
- **customizePostHeaderView(postHeader: [LMFeedPostHeaderView](../Widgets/Post/LMFeedPostHeaderView.md)):** Customizes the post header.  
- **customizePostComposer(etPostComposer: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md)):** Customizes the post composer for text content.  
- **customizePostHeadingComposer(etPostHeadingComposer: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md)):** Customizes the heading composer in the post.  
- **customizePostHeadingLimit(tvPostHeadingLimitTextView: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** Customizes the character limit display for the heading.

### Attachments Customizations  
- **customizePostImageAttachment(postSingleImageView: [LMFeedPostImageMediaView](../Widgets/Post/Media/LMFeedPostImageMediaView.md)):** Customizes the image attachment section.  
- **customizePostVideoAttachment(postSingleVideoView: [LMFeedPostVideoMediaView](../Widgets/Post/Media/LMFeedPostVideoMediaView.md)):** Customizes the video attachment section.  
- **customizePostLinkViewAttachment(linkMediaView: [LMFeedPostLinkMediaView](../Widgets/Post/Media/LMFeedPostLinkMediaView.md)):** Customizes the link view attachment section.  
- **customizePostDocumentsAttachment(postDocumentsView: [LMFeedPostDocumentsMediaView](../Widgets/Post/Media/LMFeedPostDocumentsMediaView.md)):** Customizes the document attachment section.  
- **customizePostMultipleMedia(postMultipleMediaView: [LMFeedPostMultipleMediaView](../Widgets/Post/Media/LMFeedPostMultipleMediaView.md)):** Customizes the display of multiple media attachments.  
- **customizePostPollAttachmentView(pollView: [LMFeedPostPollView](../Widgets/Poll/LMFeedPostPollView.md)):** Customizes the poll attachment section.

### Progress Bar Customization  
- **customizeEditPostProgressbar(progressBar: [LMFeedProgressBar](../Widgets/Fundamentals/LMFeedProgressBar.md)):** Customizes the progress bar shown during post edits.

---

## Interactions available in LMFeedEditPostFragment

### Post Actions  
- **onSavePostClicked():** Handles the save action for the edited post.

### Media and Document Interactions  
- **onPostDocumentMediaClicked(position: Int, parentPosition: Int, attachmentViewData: LMFeedAttachmentViewData):** Handles clicks on document or media attachments within the post.




================================================
File: feed/Android/Core/Screens/LMFeedLikesFragment.md
================================================
---
sidebar_position: 5
title: Likes Screen
slug: /android/core/screens/feed-likes-screen
---

# Screen: LMFeedLikesFragment

`LMFeedLikesFragment` is responsible for displaying the list of users who have liked a specific post or content within the LikeMinds feed system. It provides options for viewing user profiles and interacting with the list of likes.  
[GitHub Link to LMFeedLikesFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/likes/view/LMFeedLikesFragment.kt)

---

## View Style: LMFeedLikesFragmentViewStyle

`LMFeedLikesFragmentViewStyle` defines the visual style and structure of the LMFeedLikesFragment. The following fields are available for customization:

| **Field Name**          | **Description**                                    | **Type**                 |
|-------------------------|----------------------------------------------------|--------------------------|
| `headerViewStyle`       | Style attributes for the header view.              | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)  |
| `userViewStyle`         | Defines the style for displaying user views.       | [LMFeedUserViewStyle](../Widgets/LMFeedUserView.md)    |
| `backgroundColor`       | Background color for the likes fragment.           | `Int`                    |

[GitHub Link to LMFeedLikesFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/likes/style/LMFeedLikesFragmentViewStyle.kt)

---

## Customization available in LMFeedLikesFragment

### Header Customizations  
- **customizeLikesFragmentHeaderView(headerViewLikes: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** Allows customization of the header view in the likes fragment.

---

## Interactions available in LMFeedLikesFragment

### Item Click Interactions  
- **onUserLikeItemClicked(position: Int, likesViewData: LMFeedLikeViewData):** Handles clicks on individual user items within the likes list.




================================================
File: feed/Android/Core/Screens/LMFeedPollResultsFragment.md
================================================
---
sidebar_position: 7
title: Poll Result Screen
slug: /android/core/screens/feed-poll-result-screen
---

# Screen: LMFeedPollResultsFragment

`LMFeedPollResultsFragment` displays the results of a poll within the LikeMinds feed system. It allows users to view detailed results, including poll options, votes, and participant information.  
[GitHub Link to LMFeedPollResultsFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/poll/result/view/LMFeedPollResultsFragment.kt)

---

## View Style: LMFeedPollResultsFragmentViewStyle

`LMFeedPollResultsFragmentViewStyle` defines the visual style and structure of the LMFeedPollResultsFragment. The following fields are available for customization:

| **Field Name**                 | **Description**                                              | **Type**                           |
|--------------------------------|--------------------------------------------------------------|------------------------------------|
| `headerViewStyle`              | Style for the header of the poll results screen.             | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)           |
| `pollResultsTabElevation`      | Elevation style for the poll results tabs.                   | `Int`                             |
| `noResultsLayoutViewStyle`     | Style for the "no results" layout.                           | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md)   |
| `selectedPollResultsTabColor`  | Color for the selected poll results tab.                     | `Int`                             |
| `unselectedPollResultsTabColor`| Color for unselected poll results tabs.                      | `Int`                             |
| `pollResultsTabTextViewStyle`  | Style for the text view in poll results tabs.                | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                 |
| `userViewStyle`                | Defines the style for user views in the poll results.        | [LMFeedUserViewStyle](../Widgets/LMFeedUserView.md)             |
| `backgroundColor`              | Background color for the poll results fragment.              | `Int`                             |

[GitHub Link to LMFeedPollResultsFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/poll/result/style/LMFeedPollResultsFragmentViewStyle.kt)

---

## Customization available in LMFeedPollResultsFragment

### Header Customizations  
- **customizePollResultsHeaderView(headerViewPollResults: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** Allows customization of the header view in the poll results fragment.

### Tab Customizations  
- **customizePollResultsTabTextView(tvPollOptionCount: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md), tvPollOptionText: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md)):** Customizes the text view style for poll results tabs.

---

## Interactions available in LMFeedPollResultsFragment

_No interaction methods were found in this fragment._




================================================
File: feed/Android/Core/Screens/LMFeedPostDetailFragment.md
================================================
---
sidebar_position: 9
title: Post Detail Screen
slug: /android/core/screens/post-detail-screen
---

# **Screen: LMFeedPostDetailFragment**

The `LMFeedPostDetailFragment` provides a detailed view of a post. It includes the post's content, comments, likes, and interaction options, enabling users to interact with posts in various ways.

[GitHub Link to LMFeedPostDetailFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/detail/view/LMFeedPostDetailFragment.kt)

---

## **View Style: LMFeedPostDetailFragmentViewStyle**

The `LMFeedPostDetailFragmentViewStyle` defines the visual presentation of the fragment. Below are the customizable fields:

| **Field Name**           | **Description**                                       | **Type**                             |
|--------------------------|-------------------------------------------------------|--------------------------------------|
| `headerViewStyle`        | Style for the header of the post detail screen.       | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)             |
| `commentsCountViewStyle` | Style for the comments count view.                    | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                   |
| `commentViewStyle`       | Style for individual comments.                        | [LMFeedCommentViewStyle](../Widgets/Comment/LMFeedCommentView.md)            |
| `replyViewStyle`         | Style for replies to comments.                        | [LMFeedCommentViewStyle](../Widgets/Comment/LMFeedCommentView.md)            |
| `noCommentsFoundViewStyle` | Style for the "no comments found" message.          | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md)     |
| `commentComposerStyle`   | Style for the comment composer area.                  | [LMFeedCommentComposerViewStyle](../Widgets/Comment/LMFeedCommentComposerView.md)    |
| `viewMoreReplyStyle`     | Style for the "view more replies" button.             | [LMFeedViewMoreViewStyle](../Widgets/LMFeedViewMoreView.md)           |

[GitHub Link to LMFeedPostDetailFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/detail/style/LMFeedPostDetailFragmentViewStyle.kt)

---

## **Customization Available in LMFeedPostDetailFragment**

### Header Customizations
- **customizePostDetailHeaderView(headerViewPostDetail: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md))**  
  Customizes the header view of the post detail screen.

### Comment Composer Customizations
- **customizeCommentComposer(commentComposer: [LMFeedCommentComposerView](../Widgets/Comment/LMFeedCommentComposerView.md))**  
  Customizes the composer for creating comments.

### List View Customizations
- **customizePostDetailListView(rvPostDetailListView: [LMFeedPostDetailListView](../Widgets/Post/LMFeedPostDetailListView.md))**  
  Customizes the list view that displays posts and comments.

---

## **Interactions Available in LMFeedPostDetailFragment**

### Post Interactions
- `onPostCommentsCountClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the comments count is clicked.
- `onPostLikeClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the like button is clicked.
- `onPostLikesCountClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the likes count is clicked.
- `onPostSaveClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the save button is clicked.
- `onPostContentSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when "See More" on post content is clicked.
- `onPostTaggedMemberClicked(position: Int, uuid: String)`  
  Triggered when a tagged member in the post is clicked.

### Comment Interactions
- `onCommentContentLinkClicked(url: String)`  
  Triggered when a link in a comment is clicked.
- `onCommentContentSeeMoreClicked(position: Int, comment: LMFeedCommentViewData)`  
  Triggered when "See More" in a comment is clicked.
- `onCommentLikesCountClicked(position: Int, comment: LMFeedCommentViewData)`  
  Triggered when the likes count of a comment is clicked.
- `onCommentReplyClicked(position: Int, comment: LMFeedCommentViewData)`  
  Triggered when a reply button on a comment is clicked.
- `onCommentReplyCountClicked(position: Int, comment: LMFeedCommentViewData)`  
  Triggered when the reply count for a comment is clicked.
- `onCommentMenuIconClicked(position: Int, comment: LMFeedCommentViewData)`  
  Opens the comment menu.
- `onCommentMenuItemClicked(position: Int, action: String)`  
  Handles actions from the comment menu.

### Poll Interactions
- `onPollOptionClicked(position: Int, optionId: String)`  
  Triggered when a poll option is clicked.
- `onPollOptionVoteCountClicked(position: Int, optionId: String)`  
  Shows the vote count for a poll option.
- `onPostAddPollOptionClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a new poll option is added.
- `onPostSubmitPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a poll vote is submitted.
- `onPostEditPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a poll vote is edited.

### User Interactions
- `onCommenterHeaderClicked(position: Int, commentViewData: LMFeedCommentViewData)`  
  Triggered when a commenter's profile header is clicked.
- `onReplierHeaderClicked(position: Int, replyViewData: LMFeedCommentViewData)`  
  Triggered when a replier's profile header is clicked.
- `onReplyTaggedMemberClicked(position: Int, uuid: String)`  
  Triggered when a tagged member in a reply is clicked.

### Menu Interactions
- `onPostMenuIconClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Opens the post menu.
- `onPostMenuItemClicked(position: Int, action: String)`  
  Handles actions from the post menu.
- `onReplyMenuIconClicked(position: Int, replyViewData: LMFeedCommentViewData)`  
  Opens the reply menu.
- `onReplyMenuItemClicked(position: Int, action: String)`  
  Handles actions from the reply menu.
- `onDeletePostMenuClicked(position: Int)`  
  Deletes a post.
- `onEditPostMenuClicked(position: Int)`  
  Edits a post.
- `onPinPostMenuClicked(position: Int)`  
  Pins a post.
- `onUnpinPostMenuClicked(position: Int)`  
  Unpins a post.
- `onReportPostMenuClicked(position: Int)`  
  Reports a post.

### Additional Interactions
- `onPostLinkMediaClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a media link in a post is clicked.
- `onPostDocumentMediaClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a document in a post is clicked.
- `onPostShareClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a post is shared.
- `onPostHeadingSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when "See More" in the post heading is clicked.
- `onViewMoreRepliesClicked(position: Int, comment: LMFeedCommentViewData)`  
  Triggered when "View More Replies" is clicked.

---




================================================
File: feed/Android/Core/Screens/LMFeedPostMenuBottomSheetFragment.md
================================================
---
sidebar_position: 11
title: Post Menu Bottom Sheet
slug: /android/core/screens/post-menu-bottom-sheet
---

# Screen: LMFeedPostMenuBottomSheetFragment

`LMFeedPostMenuBottomSheetFragment` provides a bottom sheet menu for performing various actions on a post. It enables users to access functionalities like editing, deleting, sharing, and reporting posts.  
[GitHub Link to LMFeedPostMenuBottomSheetFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/postmenu/view/LMFeedPostMenuBottomSheetFragment.kt)

---

## View Style: 

_No view style found in this fragment._

---

## Interactions available in LMFeedPostMenuBottomSheetFragment

### Menu Item Interactions  
- **onPostMenuItemClicked(position: Int, menuItem: LMFeedPostMenuItemViewData)**: Handles clicks on individual menu items in the post menu.



================================================
File: feed/Android/Core/Screens/LMFeedQnAFeedFragment.md
================================================
---
sidebar_position: 12
title: QnA Feed Screen
slug: /android/core/screens/qna-feed-screen
---

# **Screen: LMFeedQnAFeedFragment**

The `LMFeedQnAFeedFragment` displays a Q&A feed within the LikeMinds feed system. It allows users to interact with posts, view top responses, and participate in discussions. Key features include creating new posts, filtering topics, and exploring detailed post content.

[GitHub Link to LMFeedQnAFeedFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/qnafeed/view/LMFeedQnAFeedFragment.kt)

---

## **View Style: LMFeedQnAFeedFragmentViewStyle**

The `LMFeedQnAFeedFragmentViewStyle` defines the visual style and layout of the fragment. Below are the customizable fields:

| **Field Name**                  | **Description**                                              | **Type**                             |
|---------------------------------|-------------------------------------------------------------|--------------------------------------|
| `headerViewStyle`               | Style for the header of the Q&A feed screen.                | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)             |
| `createNewPostButtonViewStyle`  | Style for the "Create New Post" button.                     | [LMFeedButtonViewStyle](../Widgets/Fundamentals/LMFeedButton.md)             |
| `noPostLayoutViewStyle`         | Style for the "no posts available" layout.                  | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md)     |
| `postingViewStyle`              | Style for the "posting in progress" layout.                 | [LMFeedPostingViewStyle](../Widgets/LMFeedPostingView.md)      |
| `topicSelectorBarStyle`         | Style for the topic selector bar.                           | [LMFeedTopicSelectorBarViewStyle](../Widgets/LMFeedTopicSelectorBarView.md)   |

[GitHub Link to LMFeedQnAFeedFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/qnafeed/style/LMFeedQnAFeedFragmentViewStyle.kt)

---

## **Customization Available in LMFeedQnAFeedFragment**

### Header and Button Customizations
- **customizeCreateNewPostButton(fabNewPost: [LMFeedFAB](../Widgets/Fundamentals/LMFeedFAB.md))**  
  Customizes the "Create New Post" button.
- **customizeQnAFeedHeaderView(headerViewQnA: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md))**  
  Customizes the header of the Q&A feed.

### Post Customizations
- **customizePostHeaderView()**  
  Customizes the header for individual posts.
- **customizePostContentView()**  
  Customizes the content view for posts.
- **customizePostHeadingView()**  
  Customizes the heading view for posts.
- **customizePostTopResponseView()**  
  Customizes the top response section in posts.
- **customizePostActionView()**  
  Customizes the action bar (likes, comments, shares).
- **customizePostAnswerPrompt()**  
  Customizes the answer prompt for Q&A posts.

### Layout Customizations
- **customizeNoPostLayout(layoutNoPost: [LMFeedNoEntityLayoutView](../Widgets/LMFeedNoEntityLayoutView.md))**  
  Customizes the layout shown when no posts are available.
- **customizePostingLayout(layoutPosting: [LMFeedPostingView](../Widgets/LMFeedPostingView.md))**  
  Customizes the layout shown during posting.
- **customizeTopicSelectorBar(topicSelectorBar: [LMFeedTopicSelectorBarView](../Widgets/LMFeedTopicSelectorBarView.md))**  
  Customizes the topic selector bar.

---

## **Interactions Available in LMFeedQnAFeedFragment**

### General Interactions
- **onRetryUploadClicked(temporaryId: Long?, attachmentCount: Int)**  
  Retry a failed post upload.
- **onUserProfileClicked(userViewData: LMFeedUserViewData)**  
  Open a user's profile.
- **onNotificationIconClicked()**  
  Open notifications.
- **onSearchIconClicked()**  
  Open the search interface.
- **onAllTopicsClicked()**  
  Display all available topics.

### Post Interactions
- **onPostContentClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Open a post's content.
- **onPostLikeClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Like a post.
- **onPostLikesCountClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Show the likes count for a post.
- **onPostCommentsCountClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Show the comments count for a post.
- **onPostSaveClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Save a post.
- **onPostShareClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Share a post.
- **onPostContentSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Expand the post's content.
- **onPostContentLinkClicked(url: String)**  
  Handles clicks on links within the post content.

### Media Interactions
- **onPostImageMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  View image media.
- **onPostVideoMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  View video media.
- **onPostLinkMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  View linked media.

### Poll Interactions
- **onPostPollTitleClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Open poll details.
- **onPostAddPollOptionClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Add a new poll option.
- **onPostMemberVotedCountClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Show members who voted.
- **onPostSubmitPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Submit a poll vote.
- **onPostEditPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Edit a submitted poll vote.

### Top Response Interactions
- **onPostTopResponseClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Open the top response for a post.
- **onPostTopResponseSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Expand the top response content.
- **onPostTopResponseTaggedMemberClicked(position: Int, uuid: String)**  
  Handle clicks on tagged members in the top response.
- **onPostTopResponseContentClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Open the full content of the top response.

### Additional Interactions
- **onPostAuthorHeaderClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Open the post author's profile.
- **onPostHeadingClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Interact with the post heading.
- **onPostHeadingSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Expand the post heading content.
- **onPostAnswerPromptClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Interact with the answer prompt for a post.

---



================================================
File: feed/Android/Core/Screens/LMFeedReportFragment.md
================================================
---
sidebar_position: 13
title: Report Screen
slug: /android/core/screens/report-screen
---

# **Screen: LMFeedReportFragment**

The `LMFeedReportFragment` provides an interface for reporting inappropriate content within the LikeMinds feed system. Users can select or input a reason for reporting and submit it for review.

[GitHub Link to LMFeedReportFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/report/view/LMFeedReportFragment.kt)

---

## **View Style: LMFeedReportFragmentViewStyle**

The `LMFeedReportFragmentViewStyle` defines the visual style and structure of the fragment. Below are the available customization fields:

| **Field Name**                       | **Description**                                              | **Type**                              |
|--------------------------------------|--------------------------------------------------------------|---------------------------------------|
| `headerViewStyle`                    | Style for the header of the report screen.                   | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)              |
| `reportHeaderStyle`                  | Style for the main header text in the report fragment.        | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                    |
| `reportSubHeaderStyle`               | Style for the sub-header text.                               | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                    |
| `reportReasonInputStyle`             | Style for the reason input field.                            | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md)                |
| `reportButtonStyle`                  | Style for the submit report button.                          | [LMFeedButtonStyle](../Widgets/Fundamentals/LMFeedButton.md)                  |
| `reportTagStyle`                     | Style for report tags (quick reasons).                       | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                    |
| `selectedReportTagColor`             | Color for selected report tags.                              | Int                                |
| `reportSuccessDialogFragmentStyle`   | Style for the success dialog shown after reporting.          | [LMFeedAlertDialogViewStyle](../Widgets/LMFeedAlertDialogView.md)         |
| `backgroundColor`                    | Background color for the report fragment.                    | `Int`                                |

[GitHub Link to LMFeedReportFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/report/style/LMFeedReportFragmentViewStyle.kt)

---

## **Customization Available in LMFeedReportFragment**

### Header and Text Customizations  
- **customizeReportFragmentHeaderView(headerViewReport: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md))**  
  Customizes the header view of the report fragment.
- **customizeReportHeaderText(tvReportHeader: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md))**  
  Customizes the main header text in the report screen.
- **customizeReportSubHeaderText(tvReportSubHeader: [LMFeedTextView](../Widgets/Fundamentals/LMFeedTextView.md))**  
  Customizes the sub-header text in the report screen.

### Input and Button Customizations  
- **customizeReportReasonInput(etReason: [LMFeedEditText](../Widgets/Fundamentals/LMFeedEditText.md))**  
  Customizes the input field for entering a report reason.
- **customizeReportButton(btnPostReport: [LMFeedButton](../Widgets/Fundamentals/LMFeedButton.md))**  
  Customizes the appearance of the submit report button.

---

## **Interactions Available in LMFeedReportFragment**

No interaction methods were found for this fragment.

---




================================================
File: feed/Android/Core/Screens/LMFeedSearchFragment.md
================================================
---
sidebar_position: 14
title: Search Screen
slug: /android/core/screens/search-screen
---

# **Screen: LMFeedSearchFragment**

The `LMFeedSearchFragment` provides an interface for searching posts within the LikeMinds feed system. It enables users to search for specific content and interact with the search results, such as liking, saving, or sharing posts.

[GitHub Link to LMFeedSearchFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/search/view/LMFeedSearchFragment.kt)

---

## **View Style: LMFeedSearchFragmentViewStyle**

The `LMFeedSearchFragmentViewStyle` defines the visual style and structure of the fragment. Below are the customizable fields:

| **Field Name**                    | **Description**                                              | **Type**                              |
|-----------------------------------|--------------------------------------------------------------|---------------------------------------|
| `feedSearchBarViewStyle`          | Style for the search bar in the feed search screen.          | [LMFeedSearchBarViewStyle](../Widgets/LMFeedSearchBarView.md)           |
| `noSearchResultLayoutViewStyle`   | Style for the "no search results" layout.                    | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md)      |
| `backgroundColor`                 | Background color for the search fragment.                    | `Int`                                |

[GitHub Link to LMFeedSearchFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/search/style/LMFeedSearchFragmentViewStyle.kt)

---

## **Customization Available in LMFeedSearchFragment**

### Search Bar and Layout Customizations  
- **customizeFeedSearchBarView(searchBarView: [LMFeedSearchBarView](../Widgets/LMFeedSearchBarView.md))**  
  Customizes the search bar in the feed search fragment.
- **customizeNoSearchResultLayout(layoutNoResult: [LMFeedNoEntityLayoutView](../Widgets/LMFeedNoEntityLayoutView.md))**  
  Customizes the layout shown when no search results are found.
- **customizeSearchListView(rvSearchListView: [LMFeedSearchListView](../Widgets/LMFeedSearchListView.md))**  
  Customizes the list view displaying search results.

---

## **Interactions Available in LMFeedSearchFragment**

### Post Content Interactions  
- **onPostContentClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens the post content.
- **onPostLikeClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Likes a post.
- **onPostLikesCountClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Displays the likes count on a post.
- **onPostCommentsCountClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Displays the comments count on a post.
- **onPostSaveClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Saves a post.
- **onPostShareClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Shares a post.
- **onPostContentLinkClicked(url: String)**  
  Handles clicks on links within the post content.

### Media Interactions  
- **onPostImageMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens image media in the post.
- **onPostVideoMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens video media in the post.
- **onPostLinkMediaClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens linked media in the post.

### Poll Interactions  
- **onPostPollTitleClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens the poll title for details.
- **onPostAddPollOptionClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Adds a new poll option.
- **onPostSubmitPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Submits a poll vote.
- **onPostEditPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Edits a submitted poll vote.
- **onPostAnswerPromptClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Interacts with the answer prompt for a post.

### Post Management Interactions  
- **onPostHeadingClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Opens the post heading for detailed view.
- **onPostHeadingSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)**  
  Expands the full heading content.

---





================================================
File: feed/Android/Core/Screens/LMFeedSelfDeleteDialogFragment.md
================================================
---
sidebar_position: 4
title: Self Delete Dialog
slug: /android/core/screens/self-delete-dialog
---

# **Screen: LMFeedSelfDeleteDialogFragment**

The `LMFeedSelfDeleteDialogFragment` is a dialog fragment that provides users with options to confirm or cancel the deletion of their own posts. It displays a customizable alert dialog with positive and negative actions.

[GitHub Link to LMFeedSelfDeleteDialogFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/delete/view/LMFeedSelfDeleteDialogFragment.kt)

---

## **View Style: LMFeedSelfDeleteDialogFragmentStyle**

The `LMFeedSelfDeleteDialogFragmentStyle` defines the visual style for the dialog fragment. Below are the customizable fields:

| **Field Name**           | **Description**                                  | **Type**                        |
|--------------------------|--------------------------------------------------|----------------------------------|
| `selfDeleteDialogStyle`  | Style for the self-delete alert dialog.          | [LMFeedAlertDialogViewStyle](../Widgets/LMFeedAlertDialogView.md)    |

[GitHub Link to LMFeedSelfDeleteDialogFragmentStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/delete/style/LMFeedSelfDeleteDialogFragmentStyle.kt)

---

## **Customization Available in LMFeedSelfDeleteDialogFragment**

### Dialog Customizations  
- **customizeSelfDeleteDialog(alertDialogDelete: [LMFeedAlertDialogView](../Widgets/LMFeedAlertDialogView.md))**  
  Customizes the self-delete alert dialog view.

---

## **Interactions Available in LMFeedSelfDeleteDialogFragment**

### Alert Dialog Interactions  
- **onSelfDeleteAlertPositiveButtonClicked()**  
  Triggered when the positive button in the self-delete alert dialog is clicked.
- **onSelfDeleteAlertNegativeButtonClicked()**  
  Triggered when the negative button in the self-delete alert dialog is clicked.

---





================================================
File: feed/Android/Core/Screens/LMFeedSocialFeedFragment.md
================================================
---
sidebar_position: 1
title: Social Feed Screen
slug: /android/core/screens/social-feed-screen
---

# Screen: LMFeedSocialFeedFragment

The `LMFeedSocialFeedFragment` serves as a core fragment in the LikeMinds Feed Android module, responsible for displaying and managing the social feed interface. It enables users to interact with various posts, including viewing, liking, commenting, sharing, and more.

**GitHub File**: [LMFeedSocialFeedFragment.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/view/LMFeedSocialFeedFragment.kt)

---

## View Style: LMFeedSocialFeedFragmentViewStyle

The `LMFeedSocialFeedFragmentViewStyle` defines the style and layout properties for components used within the `LMFeedSocialFeedFragment`. This includes configurations for headers, buttons, and other layout elements.

**GitHub File**: [LMFeedSocialFeedFragmentViewStyle.kt](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/style/LMFeedSocialFeedFragmentViewStyle.kt)

| Field                           | Description                                       | Type                                   |
|---------------------------------|---------------------------------------------------|----------------------------------------|
| `headerViewStyle`               | Style configuration for the header view.          | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)   |
| `createNewPostButtonViewStyle`  | Style for the floating action button for new posts.| [LMFeedFABStyle](../Widgets/Fundamentals/LMFeedFAB.md)          |
| `noPostLayoutViewStyle`         | Style for the "No Posts" layout.                 | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md) |
| `postingViewStyle`              | Style configuration for the posting view.         | [LMFeedPostingViewStyle](../Widgets/LMFeedPostingView.md)  |
| `topicSelectorBarStyle`         | Style for the topic selector bar.                | [LMFeedTopicSelectorBarStyle](../Widgets/LMFeedTopicSelectorBarView.md) |

---

## Customization Available in LMFeedSocialFeedFragment

The fragment provides several methods to customize its components:

- **Create New Post Button**  
  - **customizeCreateNewPostButton(fabNewPost: [LMFeedFAB](../Widgets/Fundamentals/LMFeedFAB.md)):**  
    Customize the appearance and behavior of the floating action button for creating new posts.

- **Header View**  
  - **customizeSocialFeedHeaderView(headerViewSocial: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md)):** 
    Modify the social feed header view's appearance and functionality.

- **Social Feed List View**  
  - **customizeSocialFeedListView(rvUniversal: [LMFeedSocialFeedListView](../Widgets/LMFeedSocialFeedListView.md)):**  
    Customize the recycler view that displays the list of social feed posts.

- **No Post Layout**  
  - **customizeNoPostLayout(layoutNoPost: [LMFeedNoEntityLayoutView](../Widgets/LMFeedNoEntityLayoutView.md):)**  
    Adjust the layout shown when there are no posts to display.

- **Posting Layout**  
  - **customizePostingLayout(layoutPosting: [LMFeedPostingView](../Widgets/LMFeedPostingView.md)):**  
    Modify the posting layout where users can draft and post content.

- **Topic Selector Bar**  
  - **customizeTopicSelectorBar(topicSelectorBar: [LMFeedTopicSelectorBarView](../Widgets/LMFeedTopicSelectorBarView.md)):**  
    Customize the topic selector bar, which allows users to filter posts by topics.

---

## Interactions Available in LMFeedSocialFeedFragment

The fragment also provides numerous methods to handle user interactions, categorized as follows:

### Post Content Interactions

- `onPostContentClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the main content of a post is clicked.

- `onPostContentSeeMoreClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Handles "See More" clicks within post content.

- `onPostContentLinkClicked(url: String)`  
  Fires when a hyperlink in the post content is clicked.

### Post Actions

- `onPostLikeClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a user likes a post.

- `onPostLikesCountClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Handles clicks on the likes count of a post.

- `onPostCommentsCountClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Fires when the comments count is clicked, typically opening the comments section.

- `onPostSaveClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Fires when a user saves a post.

- `onPostShareClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a user shares a post.

### Post Media Interactions

- `onPostImageMediaClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when an image in a post is clicked.

- `onPostVideoMediaClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Handles clicks on video media in a post.

- `onPostLinkMediaClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when a link-type media is clicked.

- `onPostDocumentMediaClicked(parentPosition: Int, attachmentViewData: LMFeedAttachmentViewData)`  
  Handles clicks on document media.

- `onPostMultipleMediaImageClicked(parentPosition: Int, attachmentViewData: LMFeedAttachmentViewData)`  
  Fired when an image in a carousel or multiple media post is clicked.

- `onPostMultipleMediaVideoClicked(parentPosition: Int, attachmentViewData: LMFeedAttachmentViewData)`  
  Fires when a video in a carousel or multiple media post is clicked.

### Poll Interactions

- `onPostPollTitleClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the title of a poll post is clicked.

- `onPostAddPollOptionClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Allows the user to add a poll option.

- `onPostMemberVotedCountClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Fires when the number of members who voted is clicked.

- `onPostSubmitPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Submits a vote in a poll.

- `onPostEditPollVoteClicked(position: Int, postViewData: LMFeedPostViewData)`  
  Triggered when the user wants to edit their vote on a poll.

- `onPollOptionClicked(pollPosition: Int, pollOptionPosition: Int, pollOptionViewData: LMFeedPollOptionViewData)`  
  Fires when a user selects a specific poll option.

- `onPollOptionVoteCountClicked(pollPosition: Int, pollOptionPosition: Int, pollOptionViewData: LMFeedPollOptionViewData)`  
  Triggered when the vote count for a poll option is clicked.

### Menu and Navigation

- `onPostMenuIconClicked(position: Int, anchorView: View, postViewData: LMFeedPostViewData)`  
  Opens a context menu for post actions like editing or deleting.

- `onPostMenuItemClicked(position: Int, menuId: Int, postViewData: LMFeedPostViewData)`  
  Handles specific menu item clicks for posts.

- `onEditPostMenuClicked(position: Int, menuId: Int, post: LMFeedPostViewData)`  
  Triggered when the "Edit Post" option is clicked.

- `onDeletePostMenuClicked(position: Int, menuId: Int, post: LMFeedPostViewData)`  
  Fires when the "Delete Post" option is clicked.

- `onReportPostMenuClicked(position: Int, menuId: Int, post: LMFeedPostViewData)`  
  Allows reporting a post.

- `onPinPostMenuClicked(position: Int, menuId: Int, post: LMFeedPostViewData)`  
  Triggered to pin a post to the top.

- `onUnpinPostMenuClicked(position: Int, menuId: Int, post: LMFeedPostViewData)`  
  Handles unpinning a post.

- `onUserProfileClicked(userViewData: LMFeedUserViewData)`  
  Navigates to the user's profile when their name or avatar is clicked.

- `onNotificationIconClicked()`  
  Handles clicks on the notification icon.

- `onSearchIconClicked()`  
  Triggered when the search icon is clicked.

- `onRetryUploadClicked(temporaryId: Long?, attachmentCount: Int)`  
  Allows retrying an upload after a failure.

- `onAllTopicsClicked()`  
  Fired when the "All Topics" button is clicked.

---



================================================
File: feed/Android/Core/Screens/LMFeedTopicSelectionFragment.md
================================================
---
sidebar_position: 15
title: Topic Selection Screen
slug: /android/core/screens/topic-selection-screen
---

# **Screen: LMFeedTopicSelectionFragment**

The `LMFeedTopicSelectionFragment` allows users to select topics of interest. It features a customizable header, a list of topics, and a search bar to filter topics. Users can submit their selected topics using a floating action button (FAB).

[GitHub Link to LMFeedTopicSelectionFragment](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/topicselection/view/LMFeedTopicSelectionFragment.kt)

---

## **View Style: LMFeedTopicSelectionFragmentViewStyle**

The `LMFeedTopicSelectionFragmentViewStyle` defines the visual style and layout of the fragment. Below are the available customization fields:

| **Field Name**                   | **Description**                                              | **Type**                              |
|----------------------------------|-------------------------------------------------------------|---------------------------------------|
| `headerViewStyle`                | Style for the header of the topic selection screen.          | [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md)              |
| `topicItemStyle`                 | Style for individual topic items.                           | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)                    |
| `noTopicsLayoutViewStyle`        | Style for the "no topics available" layout.                 | [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md)      |
| `submitSelectedTopicsFABStyle`   | Style for the floating action button used to submit topics. | [LMFeedFABStyle](../Widgets/Fundamentals/LMFeedFAB.md)                     |
| `topicSearchBarViewStyle`        | Style for the search bar used to filter topics.             | [LMFeedSearchBarViewStyle](../Widgets/LMFeedSearchBarView.md)           |
| `backgroundColor`                | Background color for the topic selection fragment.          | `Int`                                |

[GitHub Link to LMFeedTopicSelectionFragmentViewStyle](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/topicselection/style/LMFeedTopicSelectionFragmentViewStyle.kt)

---

## **Customization Available in LMFeedTopicSelectionFragment**

### Header and Layout Customizations  
- **customizeTopicSelectionHeaderView(headerViewTopicSelection: [LMFeedHeaderView](../Widgets/LMFeedHeaderView.md))**  
  Customizes the header view for the topic selection fragment.
- **customizeNoTopicsLayout(layoutNoTopics: [LMFeedNoEntityLayoutView](..//Widgets/LMFeedNoEntityLayoutView.md))**  
  Customizes the layout shown when no topics are available.
- **customizeSubmitTopicsFab(fabSubmitSelectedTopics: [LMFeedFAB](../Widgets/Fundamentals/LMFeedFAB.md))**  
  Customizes the floating action button for submitting selected topics.
- **customizeSearchBar(searchBar: [LMFeedSearchBarView](../Widgets/LMFeedSearchBarView.md))**  
  Customizes the search bar for filtering topics.

---

## **Interactions Available in LMFeedTopicSelectionFragment**

### General Interactions  
- **onSearchIconClicked()**  
  Triggered when the search icon is clicked.
- **onNavigationIconClicked()**  
  Triggered when the navigation icon in the header is clicked.
- **onSubmitFABClicked()**  
  Triggered when the floating action button for submitting topics is clicked.

---




================================================
File: feed/Android/Core/Screens/LMFeedVideoFeedFragment.md
================================================
---
sidebar_position: 16
title: Video Feed Screen
slug: /android/core/screens/video-feed-screen
---

The `LMFeedVideoFeedFragment` is a component responsible for managing and displaying video feeds in the LikeMinds feed. It handles the user interface and interactions associated with video content.

[View on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/videofeed/view/LMFeedVideoFeedFragment.kt)

---

## View Style: LMFeedVideoFeedFragmentViewStyle

The `LMFeedVideoFeedFragmentViewStyle` defines the styling and layout options for the video feed fragment.

[View on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/videofeed/viewstyle/LMFeedVideoFeedFragmentViewStyle.kt)

---

## Customization

### General Customizations

- `customizeVideoFeedListView(vp2VideoFeed, videoFeedAdapter)`: Customize the video feed list view with a [`ViewPager2`](#) and a video feed adapter [`LMFeedVideoFeedAdapter`](#).

---

## Configuration

The `LMFeedVideoFeedConfig` defines few configs options for the video feed fragment.

| Config                        | Type | Description                                     | Default Value |
| ----------------------------- | ---- | ----------------------------------------------- | ------------- |
| `reelViewedAnalyticThreshold` | Int  | threshold for sending reel viewed event in secs | 2             |

[View on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/videofeed/model/LMFeedVideoFeedConfig.kt)

---

## Props

The `LMFeedVideoFeedProps` defines few extra properties which can be shared to the video feed fragment to complete certain requirements

| Props                  | Type               | Description                              | Default Value |
| ---------------------- | ------------------ | ---------------------------------------- | ------------- |
| `startFeedWithPostIds` | List&lt;String&gt; | specific post ids to start the feed from | `null`        |

---

## Interactions

### Post Interactions

- `onPostLikeClicked(position, postViewData)`: Triggered when a post is liked, with `position` and `postViewData` as inputs.
- `onPostContentSeeMoreClicked(position, postViewData)`: Triggered when "see more" is clicked for post content.
- `onPostContentLinkClicked(url)`: Triggered when a URL link in post content is clicked.
- `onPostVideoFeedCaughtUpClicked()`: Triggered when the user catches up on video feed posts.

### Post Actions

- `onPostActionMenuClicked(position, postViewData)`: Triggered when the action menu for a post is clicked.
- `onPostMenuItemClicked(postId, menuItem)`: Triggered when a menu item for a post is clicked.

### Author and Tag Interactions

- `onPostAuthorHeaderClicked(position, postViewData)`: Triggered when the author's header is clicked.
- `onPostTaggedMemberClicked(position, uuid)`: Triggered when a tagged member in a post is clicked.

### Post Menu Interactions

- `onEditPostMenuClicked(position, menuId, post)`: Triggered when the "edit post" menu item is clicked.
- `onDeletePostMenuClicked(position, menuId, post)`: Triggered when the "delete post" menu item is clicked.
- `onReportPostMenuClicked(position, menuId, post)`: Triggered when the "report post" menu item is clicked.

---



================================================
File: feed/Android/Core/Screens/Screens.md
================================================
---
sidebar_position: 1
title: Screens
slug: /android/core/screens
---

# Introduction to Screens in Android

The **LikeMinds Feed Android SDK** provides several core screens for implementing feed functionality. This document outlines the main screens, their purposes, and how to customize them using the SDK's customization mechanism; enabling developers to understand and leverage the SDK's customization capabilities effectively.

## Prerequisites

- **LikeMinds Feed Android SDK** installed and default feed is running in your project. Using the [Guide here](../../getting-started.md).

## Screens

The LikeMinds Feed SDK comes with a suite of pre-built screens (provided as Fragments) covering common social feed functionality. You can use these out-of-the-box to implement a full feed experience, or navigate to specific ones based on user actions.

- [Social Feed Screen](./LMFeedSocialFeedFragment.md)
- [Post Detail Screen](./LMFeedPostDetailFragment.md)
- [QnA Feed Screen](./LMFeedQnAFeedFragment.md)
- [Video Feed Screen](./LMFeedVideoFeedFragment.md)
- [Create Post Screen](./LMFeedCreatePostFragment.md)
- [Post Edit Screen](./LMFeedEditPostFragment.md)
- [Activity Feed Screen](./LMFeedActivityFeedFragment.md)
- [Admin Delete Dialog](./LMFeedAdminDeleteDialogFragment.md)
- [Self Delete Dialog](./LMFeedSelfDeleteDialogFragment.md)
- [Likes Screen](./LMFeedLikesFragment.md)
- [Create Poll Screen](./LMFeedCreatePollFragment.md)
- [Poll Result Screen](./LMFeedPollResultsFragment.md)
- [Post Menu Bottom Sheet](./LMFeedPostMenuBottomSheetFragment.md)
- [Report Screen](./LMFeedReportFragment.md)
- [Search Screen](./LMFeedSearchFragment.md)
- [Topic Selection Screen](./LMFeedTopicSelectionFragment.md)

Each of these screens is built-in and ready to use. They are implemented as fragments that you can directly launch or navigate to. Under the hood, these screens utilize the LikeMinds Feed SDK’s UI components and data layer to provide a consistent experience.

### Key Components

Each screen comprises for certain key components to customize different parts and navigation of the screen.

#### View Style Classes

- Each screen comes with a corresponding `ViewStyle` class that encapsulates the stylistic properties of that screen’s UI components.
- For instance, the [Social Feed Screen](./LMFeedSocialFeedFragment.md) has [`LMFeedSocialFeedFragmentViewStyle`](./LMFeedSocialFeedFragment.md#view-style-lmfeedsocialfeedfragmentviewstyle) which contains style fields for the header, the "create post" FAB, empty-state layouts, etc.

:::info
All the **default UI styling** properties in respective `ViewStyle` classes are already defined in the [`LMFeedStyleTransformer`](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/utils/LMFeedStyleTransformer.kt) class.
:::

#### Customization Methods

- The SDK’s fragments provide override-able methods that act as hooks for you to inject custom UI or logic.
- For example, [Social Feed Screen](./LMFeedSocialFeedFragment.md) has methods like `customizeCreateNewPostButton()`, `customizeSocialFeedHeaderView()`, `customizeSocialFeedListView()` etc.​

#### Interaction Callbacks

- Apart from UI appearance, you might want to customize behavior when users interact with the feed. The SDK provides callback methods for various user interactions on each screen.
- These are typically methods you can override in a subclass to intercept events.
- For example, in [Social Feed Screen](./LMFeedSocialFeedFragment.md) following functions are available to override
  - `onPostContentClicked(...)` when a post is tapped
  - `onPostLikeClicked(...)` when the like button is pressed
  - `onPostShareClicked(...)` when share is tapped

#### Custom Entry Point

- In Getting Started Guide's [Step 4](../../getting-started.md#step-4---navigation-to-the-feed), we have shown the default way to navigate to [Social Feed Screen](./LMFeedSocialFeedFragment.md), [QnA Feed Screen](./LMFeedQnAFeedFragment.md), and [Video Feed Screen](./LMFeedVideoFeedFragment.md) but if you want to change the default navigation and navigate to a custom screen then you should pass the extras object with respective values while getting it's instance.
- For example, to start the feed from [Post Detail Screen](./LMFeedPostDetailFragment.md), you can pass the `postId` in the `LMFeedPostDetailExtras` object and then pass the fragment instance in the `LMFeedCore.showFeed()` method.

```kotlin
val apiKey = "Your generated API key" // api key generated from the dashboard
val userName = "ENTER USER NAME" // name of the user
val userId = "ENTER USER ID" // id of the user
val context = this // instance of context

val successCallback = { response : UserResponse? ->
    val containerViewId = R.id.frame_layout

    // Create the extras for the Post Detail Screen
    val postDetailExtras =  LMFeedPostDetailExtras.Builder()
        .postId("<Enter postId>")
        .build()

    // Create the fragment instance
    val fragment = LMFeedPostDetailFragment.getInstance(postDetailExtras)

    // Replace the fragment in the container view
    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(containerViewId, fragment, containerViewId.toString())
    transaction.commit()
} // callback triggered when the initiate user call is successful

val failureCallback = { errorMessage ->
  Log.e("Example", errorMessage)
  Unit
} // callback triggered when the initiate user call fails

LMFeedCore.showFeed(
    context = context,
    apiKey = apiKey,
    uuid = userId,
    userName = userName,
    success = successCallback,
    error = failureCallback
)
```

## How to Customize Screens

To illustrate the customization process, let’s customize the [Social Feed Screen](./LMFeedSocialFeedFragment.md) as an example. Let's do the following changes

- Change the title of the app bar
- Change the background color of the "New Post" button and changes it text to "Create Post"
- Handle the click on a post and show a toast with the message "Post Content Clicked"

### Step 1: Create a Custom Screen extending the Social Feed Screen

First, create a class extending `LMFeedSocialFeedFragment` in your project. In this subclass, override its delegate methods to tweak the UI components:

- `customizeSocialFeedHeaderView()` gives us the fragment’s header view (`LMFeedHeaderView`) so we can modify it – we changed the title text in this example.
- `customizeCreateNewPostButton()` provides the Floating Action Button (`LMFeedFAB`) used for creating a new post – we replaced its icon and color. (The LMFeedFAB is a custom view class for the FAB in the SDK.)
- `onPostContentClicked()` is an example of intercepting an interaction. In this case, we’re currently calling super to retain default behavior (which likely opens the Post Detail screen), but you could replace that with a custom navigation (e.g., open a different activity or fragment).

```kotlin
class CustomSocialFeedFragment : LMFeedSocialFeedFragment(LMFeedType.UNIVERSAL_FEED) {

    override fun customizeSocialFeedHeaderView(headerViewSocial: LMFeedHeaderView) {
        super.customizeSocialFeedHeaderView(headerViewSocial)
        // Customize the feed header (app bar) - set a custom title
        headerViewSocial.setTitleText("My Community Feed")
    }

    override fun customizeCreateNewPostButton(fabNewPost: LMFeedFAB) {
        // Customize the create new post button - set a background color
        // Update the header view style
        val socialFeedFragmentViewStyle = LMFeedStyleTransformer.socialFeedFragmentViewStyle
        val createNewPostButtonStyle = socialFeedFragmentViewStyle.createNewPostButtonViewStyle
        val updatedCreateNewPostButtonStyle = createNewPostButtonStyle.toBuilder()
            .backgroundColor(R.color.white)
            .build()
        val updatedSocialFeedFragmentViewStyle = socialFeedFragmentViewStyle.toBuilder()
            .createNewPostButtonViewStyle(updatedCreateNewPostButtonStyle)
            .build()

        // Update the style transformer
        LMFeedStyleTransformer.socialFeedFragmentViewStyle = updatedSocialFeedFragmentViewStyle

        // Set the updated header view style
        super.customizeCreateNewPostButton(fabNewPost)

        // Customize the create new post button - set a custom title
        fabNewPost.text = "Create Post"
    }

    override fun onPostContentClicked(position: Int, postViewData: LMFeedPostViewData) {
        // Handle the post content click event
        Toast.makeText(requireContext(),"Post Content Clicked",Toast.LENGTH_SHORT).show()
        super.onPostContentClicked(position, postViewData)
    }
```
:::info
To customise screen or change it's view style, follow the order inside it's respective "customize" override method:
- Get respective view style from [`LMFeedStyleTransformer`](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/utils/LMFeedStyleTransformer.kt) and use builder pattern to set up a new view style then update the respective view style by updating `LMFeedStyleTransformer`.
- Call `super` of the respective "customize" method inside the override method to display the updated view style.
- For any content or data changes w.r.t the view object being passed as param inside override method, do it after calling `super` of the respective "customize" method.
:::

:::info
Only override what you need, for any method you don’t override, the SDK’s default implementation will be used.
:::

### Step 2: Use the Custom Fragment

The custom screen created can be used anywhere but for now, we will use the custom screen and change default navigation way:

```kotlin
val apiKey = "Your generated API key" // api key generated from the dashboard
val userName = "ENTER USER NAME" // name of the user
val userId = "ENTER USER ID" // id of the user
val context = this // instance of context

val successCallback = { response : UserResponse? ->
    //user session initiated successfully, write your logic here
    val containerViewId = R.id.frame_layout
    val fragment = CustomSocialFeedFragment()

    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(containerViewId, fragment, containerViewId.toString())
    transaction.commit()
} // callback triggered when the initiate user call is successful

val failureCallback = { errorMessage ->
  Log.e("Example", errorMessage)
  Unit
} // callback triggered when the initiate user call fails

LMFeedCore.showFeed(
    context = context,
    apiKey = apiKey,
    uuid = userId,
    userName = userName,
    success = successCallback,
    error = failureCallback
)
```

With everything set up, run your app and navigate to the feed. The Social Feed screen should now appear with your customizations in place as per our example:

- The app bar (header) now shows "My Community Feed" as the title (our custom text).
- The "New Post" FAB is styled to have a white background color and the text is changed to "Create Post".
- The click on a post triggers a toast with the message "Post Content Clicked".
- All other aspects of the feed remain default (since we didn’t override other parts or styles).

## Conclusion

By mixing and matching these approaches (theme configuration, subclassing with overrides, and callback handling), you can deeply customize the feed experience while still leveraging the robust pre-built functionality of the LikeMinds Feed SDK.



================================================
File: feed/Android/Core/Widgets/LMFeedActivityView.md
================================================
---
sidebar_position: 2
title: Feed Activity
slug: /android/core/widgets/activity-feed
---

# LMFeedActivityView

## Widget: LMFeedActivityView

The `LMFeedActivityView` is a customizable view for displaying activity feed entries, supporting features like user images, activity content, timestamps, and badges with configurable styles.

| Method                                                                                                                                                                                                                                                | Description                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| setStyle(activityViewStyle: [LMFeedActivityViewStyle](#view-style-lmfeedactivityviewstyle))                                                                                                                                                           | Applies the given style to the activity view.                            |
| setActivityContent(activityContent: String)                                                                                                                                                                                                           | Sets the content of the activity.                                        |
| setTimestamp(createdAtTimeStamp: Long)                                                                                                                                                                                                                | Sets the timestamp of the activity.                                      |
| setActivityRead(isRead: Boolean)                                                                                                                                                                                                                      | Marks the activity as read or unread.                                    |
| setUserImage(user: [LMFeedUserViewData](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/utils/user/LMFeedUserViewData.kt))                         | Sets the user's image.                                                   |
| setPostTypeBadge(@[LMFeedAttachmentType](https://github.com/LikeMindsCommunity/likeminds-feed-android/blob/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/model/LMFeedAttachmentType.kt) attachmentType: Int?) | Sets the badge indicating the type of post associated with the activity. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/acitivityfeed/view/LMFeedActivityView.kt)

## View Style: LMFeedActivityViewStyle

The `LMFeedActivityViewStyle` defines the appearance and layout properties for the `LMFeedActivityView`, including configurations for user images, activity content, and badges.

| Field                           | Description                                             | Type                                                           |
| ------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------- |
| `userImageViewStyle`            | Configures the style for the user image.                | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| `activityTextStyle`             | Configures the text style for the activity description. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)   |
| `postTypeBadgeStyle`            | Configures the style for the post type badge.           | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| `timestampTextStyle`            | Configures the text style for the timestamp.            | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md)   |
| `readActivityBackgroundColor`   | Specifies the background color for read activities.     | Int                                                            |
| `unreadActivityBackgroundColor` | Specifies the background color for unread activities.   | Int                                                            |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/acitivityfeed/style/LMFeedActivityViewStyle.kt)



================================================
File: feed/Android/Core/Widgets/LMFeedAlertDialogView.md
================================================
---
sidebar_position: 3
title: Alert Dialog
slug: /android/core/widgets/alert-dialog
---

# **Widget Documentation: LMFeedAlertDialogView**

## **Widget: LMFeedAlertDialogView**
The `LMFeedAlertDialogView` is a customizable dialog view for presenting alerts, supporting elements like titles, subtitles, buttons, input fields, and configurable styles.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(alertDialogStyle: [LMFeedAlertDialogViewStyle](../Widgets/LMFeedAlertDialogView.md))**                             | Applies the given style to the alert dialog view.                                          |
| **setAlertTitle(title: [String](https://docs.likeminds.community/))**                                                      | Sets the title of the alert dialog.                                                        |
| **setAlertSubtitle(subtitle: [String](https://docs.likeminds.community/))**                                                | Sets the subtitle of the alert dialog.                                                     |
| **setAlertSelectorText(selector: [String](https://docs.likeminds.community/))**                                            | Sets the text for the selector in the alert dialog.                                        |
| **setAlertPositiveButtonText(positiveButtonText: [String](https://docs.likeminds.community/))**                            | Sets the text for the positive button in the alert dialog.                                 |
| **setAlertNegativeButtonText(negativeButtonText: [String](https://docs.likeminds.community/))**                            | Sets the text for the negative button in the alert dialog.                                 |
| **setAlertInputReasonVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                 | Toggles the visibility of the input reason field.                                          |
| **setAlertInputHint(hint: [String](https://docs.likeminds.community/))**                                                   | Sets the hint text for the input field.                                                    |
| **setAlertSelectorClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                    | Registers a click listener for the selector.                                               |
| **setPositiveButtonClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                   | Registers a click listener for the positive button.                                        |
| **setNegativeButtonClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                   | Registers a click listener for the negative button.                                        |
| **setPositiveButtonEnabled(isEnabled: [Boolean](https://docs.likeminds.community/))**                                      | Toggles the enabled state of the positive button.                                          |
| **getAlertInputReason(): [String](https://docs.likeminds.community/)}**                                                    | Retrieves the text inputted in the reason field.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/alertdialog/view/LMFeedAlertDialogView.kt)

## **View Style: LMFeedAlertDialogViewStyle**
The `LMFeedAlertDialogViewStyle` defines the appearance and layout properties for the `LMFeedAlertDialogView`, including configurations for text, buttons, and the dialog box.

| Field                           | Description                                      | Type              |
|---------------------------------|--------------------------------------------------|-------------------|
| **alertTitleText**              | Configures the text style for the alert title.   | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **alertSubtitleText**           | Configures the text style for the alert subtitle.| [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **alertNegativeButtonStyle**    | Configures the text style for the negative button.| [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **alertPositiveButtonStyle**    | Configures the text style for the positive button.| [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **alertSelectorStyle**          | Configures the text style for the selector.      | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **alertInputStyle**             | Configures the style for the input field.        | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md) |
| **alertActivePositiveButtonColor** | Specifies the color for the active positive button. | [Int](https://docs.likeminds.community/)           |
| **alertBoxElevation**           | Specifies the elevation of the alert dialog box. | [Int](https://docs.likeminds.community/)           |
| **alertBoxCornerRadius**        | Specifies the corner radius of the alert dialog box. | [Int](https://docs.likeminds.community/)           |
| **backgroundColor**             | Specifies the background color of the alert dialog box. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/alertdialog/style/LMFeedAlertDialogViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedHeaderView.md
================================================
---
sidebar_position: 5
title: Header
slug: /android/core/widgets/header
---

# **Widget Documentation: LMFeedHeaderView**

## **Widget: LMFeedHeaderView**
The `LMFeedHeaderView` is a customizable header component, supporting elements like titles, subtitles, navigation icons, notification icons, and user profile images with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(headerViewStyle: [LMFeedHeaderViewStyle](../Widgets/LMFeedHeaderView.md))**                                   | Applies the given style to the header view.                                                |
| **setTitleText(title: [String](https://docs.likeminds.community/))**                                                       | Sets the title text in the header.                                                         |
| **setSubTitleText(subtitle: [String](https://docs.likeminds.community/))**                                                 | Sets the subtitle text in the header.                                                     |
| **setNavigationIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                   | Registers a click listener for the navigation icon.                                        |
| **setSubmitText(submitText: [String](https://docs.likeminds.community/))**                                                 | Sets the text for the submit button.                                                       |
| **setSubmitButtonEnabled(isEnabled: [Boolean](https://docs.likeminds.community/), showProgress: [Boolean](https://docs.likeminds.community/) = false)**     | Toggles the enabled state of the submit button and optionally shows a progress indicator.  |
| **setNotificationCountText(count: [Int](https://docs.likeminds.community/))**                                              | Sets the text for the notification count.                                                  |
| **setNotificationIconVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                 | Toggles the visibility of the notification icon.                                           |
| **setUserProfileImage(user: [LMFeedUserViewData](https://docs.likeminds.community/))**                                     | Sets the user's profile image in the header.                                              |
| **setSearchIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the search icon.                                            |
| **setSubmitButtonClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                     | Registers a click listener for the submit button.                                          |
| **setUserProfileClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the user profile icon.                                      |
| **setNotificationIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                | Registers a click listener for the notification icon.                                      |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/headerview/view/LMFeedHeaderView.kt)

## **View Style: LMFeedHeaderViewStyle**
The `LMFeedHeaderViewStyle` defines the appearance and layout properties for the `LMFeedHeaderView`, including configurations for text styles, icons, and colors.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **titleTextStyle**           | Configures the text style for the title.         | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **subtitleTextStyle**        | Configures the text style for the subtitle.      | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **backgroundColor**          | Specifies the background color of the header view. | [Int](https://docs.likeminds.community/)           |
| **elevation**                | Specifies the elevation of the header view.      | [Int](https://docs.likeminds.community/)           |
| **submitTextStyle**          | Configures the text style for the submit button. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **activeSubmitColor**        | Specifies the color for the active submit button.| [Int](https://docs.likeminds.community/)           |
| **navigationIconStyle**      | Configures the style for the navigation icon.    | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **searchIconStyle**          | Configures the style for the search icon.        | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **userProfileStyle**         | Configures the style for the user profile image. | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **notificationIconStyle**    | Configures the style for the notification icon.  | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **notificationCountTextStyle** | Configures the text style for the notification count. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/headerview/style/LMFeedHeaderViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedLabelIconContainerView.md
================================================
---
sidebar_position: 6
title: Label Icon Container
slug: /android/core/widgets/label-icon-container
---

# **Widget Documentation: LMFeedLabelIconContainerView**

## **Widget: LMFeedLabelIconContainerView**
The `LMFeedLabelIconContainerView` is a customizable container view that includes an icon and a label, supporting configurable styles and content.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(labelIconContainerViewStyle: [LMFeedLabelIconContainerViewStyle](../Widgets/LMFeedLabelIconContainerView.md))**           | Applies the given style to the label and icon container view.                              |
| **setContainerIcon(@DrawableRes icon: [Int](https://docs.likeminds.community/))**                                           | Sets the icon for the container.                                                           |
| **setContainerLabel(labelText: [String](https://docs.likeminds.community/))**                                               | Sets the label text for the container.                                                     |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/labeliconcontainer/view/LMFeedLabelIconContainerView.kt)

## **View Style: LMFeedLabelIconContainerViewStyle**
The `LMFeedLabelIconContainerViewStyle` defines the appearance and layout properties for the `LMFeedLabelIconContainerView`, including configurations for the icon and label.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **containerIconStyle**       | Configures the style for the container's icon.   | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **containerLabelStyle**      | Configures the text style for the container's label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **backgroundColor**          | Specifies the background color of the container view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/labeliconcontainer/style/LMFeedLabelIconContainerViewStyle.kt)





================================================
File: feed/Android/Core/Widgets/LMFeedLabelImageContainerView.md
================================================
---
sidebar_position: 6
title: Label Image Container
slug: /android/core/widgets/label-image-container
---

# **Widget Documentation: LMFeedLabelImageContainerView**

## **Widget: LMFeedLabelImageContainerView**
The `LMFeedLabelImageContainerView` is a customizable container view that includes an image and a label, supporting configurable styles and content.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(labelImageContainerViewStyle: [LMFeedLabelImageContainerViewStyle](../Widgets/LMFeedLabelImageContainerView.md))**         | Applies the given style to the label and image container view.                             |
| **setContainerImage(imageSrc: [Any](https://docs.likeminds.community/))**                                                   | Sets the image for the container.                                                          |
| **setContainerLabel(labelText: [String](https://docs.likeminds.community/))**                                               | Sets the label text for the container.                                                     |
| **setContainerClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the container.                                              |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/labelimagecontainer/view/LMFeedLabelImageContainerView.kt)

## **View Style: LMFeedLabelImageContainerViewStyle**
The `LMFeedLabelImageContainerViewStyle` defines the appearance and layout properties for the `LMFeedLabelImageContainerView`, including configurations for the image and label.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **containerImageStyle**      | Configures the style for the container's image.  | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **containerLabelStyle**      | Configures the text style for the container's label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **backgroundColor**          | Specifies the background color of the container view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/labelimagecontainer/style/LMFeedLabelImageContainerViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedNoEntityLayoutView.md
================================================
---
sidebar_position: 7
title: No Entity Layout
slug: /android/core/widgets/no-entity-layout
---

# **Widget Documentation: LMFeedNoEntityLayoutView**

## **Widget: LMFeedNoEntityLayoutView**
The `LMFeedNoEntityLayoutView` is a customizable layout designed to display a message or action when no entities are available, with support for a title, subtitle, image, and a floating action button (FAB).

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setTitleText(title: [String](https://docs.likeminds.community/))**                                                       | Sets the title text for the layout.                                                        |
| **setSubtitleText(subtitle: [String](https://docs.likeminds.community/))**                                                 | Sets the subtitle text for the layout.                                                     |
| **setActionCTAText(ctaAction: [String](https://docs.likeminds.community/))**                                               | Sets the text for the action call-to-action (CTA).                                         |
| **setActionFABColor(@ColorRes fabColor: [Int](https://docs.likeminds.community/))**                                        | Sets the color for the floating action button (FAB).                                       |
| **setActionFABClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the FAB.                                                    |
| **setStyle(noEntityLayoutViewStyle: [LMFeedNoEntityLayoutViewStyle](../Widgets/LMFeedNoEntityLayoutView.md))**                  | Applies the given style to the no-entity layout view.                                      |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/noentitylayout/view/LMFeedNoEntityLayoutView.kt)

## **View Style: LMFeedNoEntityLayoutViewStyle**
The `LMFeedNoEntityLayoutViewStyle` defines the appearance and layout properties for the `LMFeedNoEntityLayoutView`, including configurations for text, images, and the floating action button.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **imageStyle**               | Configures the style for the image.              | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **titleStyle**               | Configures the text style for the title.         | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **subtitleStyle**            | Configures the text style for the subtitle.      | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **actionStyle**              | Configures the style for the floating action button. | [LMFeedFABStyle](../Widgets/Fundamentals/LMFeedFAB.md) |
| **backgroundColor**          | Specifies the background color of the layout view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/noentitylayout/style/LMFeedNoEntityLayoutViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedOverflowMenu.md
================================================
---
sidebar_position: 8
title: Overflow Menu
slug: /android/core/widgets/overflow-menu
---

# **Widget Documentation: LMFeedOverflowMenu**

## **Widget: LMFeedOverflowMenu**
The `LMFeedOverflowMenu` is a customizable menu component for displaying a list of actions or options in an overflow menu style.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setMenuItemClickListener(listener: [LMFeedMenuItemClickListener](https://docs.likeminds.community/))**                   | Registers a click listener for menu items.                                                 |
| **addMenuItems(menuItems: [List]([LMFeedMenuItemData](https://docs.likeminds.community/)))**                                | Adds menu items to the overflow menu.                                                      |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/overflowmenu/view/LMFeedOverflowMenu.kt)



================================================
File: feed/Android/Core/Widgets/LMFeedPostingView.md
================================================
---
sidebar_position: 15
title: Posting 
slug: /android/core/widgets/posting
---

# **Widget Documentation: LMFeedPostingView**

## **Widget: LMFeedPostingView**
The `LMFeedPostingView` is a customizable view for displaying the status of a posting operation, including progress, retry options, and success indicators with configurable styles.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setPostingText(title: [String](https://docs.likeminds.community/))**                                                     | Sets the posting title text.                                                               |
| **setProgress(progress: [Int](https://docs.likeminds.community/))**                                                        | Updates the progress of the posting operation.                                             |
| **setProgressVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                         | Toggles the visibility of the progress bar.                                                |
| **setRetryCTAText(retryCTAText: [String](https://docs.likeminds.community/))**                                             | Sets the text for the retry call-to-action (CTA).                                          |
| **setRetryVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                            | Toggles the visibility of the retry option.                                                |
| **setPostSuccessfulVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                   | Toggles the visibility of the success message or indicator.                                |
| **setRetryCTAClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for the retry CTA.                                              |
| **setAttachmentThumbnail(uri: [Uri](https://docs.likeminds.community/))**                                                 | Sets the thumbnail for the attachment.                                                    |
| **setStyle(postingViewStyle: [LMFeedPostingViewStyle](../Widgets/LMFeedPostingView.md))**                                | Applies the given style to the posting view.                                               |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/view/LMFeedPostingView.kt)

## **View Style: LMFeedPostingViewStyle**
The `LMFeedPostingViewStyle` defines the appearance and layout properties for the `LMFeedPostingView`, including configurations for text, images, and progress indicators.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **attachmentThumbnailImageStyle** | Configures the style for the attachment thumbnail image. | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **postingHeadingTextStyle**  | Configures the text style for the posting title. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **progressStyle**            | Configures the style for the progress bar.       | [LMFeedProgressBarStyle](../Widgets/Fundamentals/LMFeedProgressBar.md) |
| **retryButtonTextStyle**     | Configures the text style for the retry button.  | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **postingDoneImageStyle**    | Configures the style for the success indicator image. | [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **backgroundColor**          | Specifies the background color of the posting view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/style/LMFeedPostingViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedSearchBarView.md
================================================
---
sidebar_position: 11
title: Search Bar
slug: /android/core/widgets/search-bar
---

# **Widget Documentation: LMFeedSearchBarView**

## **Widget: LMFeedSearchBarView**
The `LMFeedSearchBarView` is a customizable search bar widget designed for handling search input and events, with configurable styles for icons, input fields, and layout.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **initialize(lifecycleScope: [LifecycleCoroutineScope](https://docs.likeminds.community/))**                               | Initializes the search bar with a lifecycle scope.                                         |
| **setSearchViewListener(mSearchViewListener: [LMFeedSearchBarListener](https://docs.likeminds.community/))**               | Sets the listener for search bar events.                                                  |
| **closeSearch()**                                                                          | Closes the search bar view.                                                               |
| **setStyle(searchBarViewStyle: [LMFeedSearchBarViewStyle](../Widgets/LMFeedSearchBarView.md))**                            | Applies the given style to the search bar view.                                           |
| **openSearch()**                                                                          | Opens the search bar view.                                                                |
| **observeSearchView(debounce: [Boolean](https://docs.likeminds.community/) = true)**                                       | Observes the text changes in the search bar with an optional debounce.                   |
| **onSearchViewOpened()**                                                                  | Callback when the search bar is opened.                                                   |
| **onSearchViewClosed()**                                                                  | Callback when the search bar is closed.                                                   |
| **onSearchCrossed()**                                                                     | Callback when the search bar's cross button is clicked.                                   |
| **onKeywordEntered(keyword: [String](https://docs.likeminds.community/))**                                                 | Callback when a keyword is entered in the search bar.                                     |
| **onEmptyKeywordEntered()**                                                               | Callback when an empty keyword is entered in the search bar.                              |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/searchbar/view/LMFeedSearchBarView.kt)

## **View Style: LMFeedSearchBarViewStyle**
The `LMFeedSearchBarViewStyle` defines the appearance and layout properties for the `LMFeedSearchBarView`, including configurations for text input, icons, and background.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **searchInputStyle**         | Configures the style for the search input field. | [LMFeedEditTextStyle](../Widgets/Fundamentals/LMFeedEditText.md) |
| **searchBackIconStyle**      | Configures the style for the back icon.          | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **searchCloseIconStyle**     | Configures the style for the close icon.         | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **backgroundColor**          | Specifies the background color of the search bar view. | [Int](https://docs.likeminds.community/)           |
| **elevation**                | Specifies the elevation of the search bar view.  | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/searchbar/style/LMFeedSearchBarViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedSearchListView.md
================================================
---
sidebar_position: 18
title: Feed Search List View  
slug: /android/core/widgets/feed-search-list-view
---

# **Widget Documentation: LMFeedSearchListView**

## **Widget: LMFeedSearchListView**
The `LMFeedSearchListView` is a customizable list view for displaying search results, supporting features like video auto-play, pagination, and dynamic post management.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **initiateVideoAutoPlayer()**                                                              | Initiates the video auto-player functionality.                                             |
| **refreshVideoAutoPlayer()**                                                              | Refreshes the video auto-player functionality.                                             |
| **destroyVideoAutoPlayer()**                                                              | Destroys the video auto-player functionality.                                              |
| **initAdapterAndSetListener(listener: [LMFeedPostAdapterListener](https://docs.likeminds.community/))**                     | Initializes the adapter and sets a listener for post actions.                              |
| **setAdapter()**                                                                          | Sets the adapter for the list view.                                                        |
| **setPaginationScrollListener(scrollListener: [LMFeedEndlessRecyclerViewScrollListener](https://docs.likeminds.community/))** | Sets the pagination scroll listener.                                                      |
| **resetScrollListenerData()**                                                             | Resets the scroll listener's data.                                                         |
| **allPosts(): [List]([LMFeedBaseViewType](https://docs.likeminds.community/))**                                             | Retrieves all posts from the list.                                                         |
| **replacePosts(posts: [List]([LMFeedPostViewData](https://docs.likeminds.community/)))**                                    | Replaces the current list of posts with a new list.                                        |
| **addPosts(posts: [List]([LMFeedPostViewData](https://docs.likeminds.community/)))**                                        | Adds a list of posts to the current list.                                                  |
| **removePostAtIndex(index: [Int](https://docs.likeminds.community/))**                                                     | Removes a post at the specified index.                                                     |
| **clearPostsAndNotify()**                                                                 | Clears all posts and notifies the adapter.                                                 |
| **getIndexAndPostFromAdapter(postId: [String](https://docs.likeminds.community/)): [Pair]([Int](https://docs.likeminds.community/), [LMFeedPostViewData](https://docs.likeminds.community/))** | Retrieves the index and post data from the adapter based on the post ID.                  |
| **getPostFromAdapter(position: [Int](https://docs.likeminds.community/)): [LMFeedPostViewData](https://docs.likeminds.community/)**                         | Retrieves the post data from the adapter based on its position.                            |
| **updatePostWithoutNotifying(position: [Int](https://docs.likeminds.community/), postItem: [LMFeedPostViewData](https://docs.likeminds.community/))**       | Updates a post item at the specified position without notifying the adapter.               |
| **updatePostItem(position: [Int](https://docs.likeminds.community/), updatedPostItem: [LMFeedPostViewData](https://docs.likeminds.community/))**            | Updates a post item at the specified position and notifies the adapter.                    |
| **scrollToPositionWithOffset(position: [Int](https://docs.likeminds.community/))**                                         | Scrolls to the specified position with an offset.                                          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/search/view/LMFeedSearchListView.kt)



================================================
File: feed/Android/Core/Widgets/LMFeedSnackbarView.md
================================================
---
sidebar_position: 12
title: Snackbar
slug: /android/core/widgets/snackbar
---

# **Widget Documentation: LMFeedSnackbarView**

## **Widget: LMFeedSnackbarView**
The `LMFeedSnackbarView` is a customizable snackbar component for displaying transient messages with animation support for content transitions.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **animateContentIn(delay: [Int](https://docs.likeminds.community/), duration: [Int](https://docs.likeminds.community/))**                                    | Animates the content of the snackbar view into the screen with a specified delay and duration. |
| **animateContentOut(delay: [Int](https://docs.likeminds.community/), duration: [Int](https://docs.likeminds.community/))**                                   | Animates the content of the snackbar view out of the screen with a specified delay and duration. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/snackbar/view/LMFeedSnackbarView.kt)





================================================
File: feed/Android/Core/Widgets/LMFeedSocialFeedListView.md
================================================
---
sidebar_position: 17
title: Feed List  
slug: /android/core/widgets/feed-list
---

# **Widget Documentation: LMFeedSocialFeedListView**

## **Widget: LMFeedSocialFeedListView**
The `LMFeedSocialFeedListView` is a customizable list view for displaying social feed posts, supporting features like video auto-play, pagination, and dynamic post management.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **initiateVideoAutoPlayer()**                                                              | Initiates the video auto-player functionality.                                             |
| **refreshVideoAutoPlayer()**                                                              | Refreshes the video auto-player functionality.                                             |
| **destroyVideoAutoPlayer()**                                                              | Destroys the video auto-player functionality.                                              |
| **initAdapterAndSetListener(listener: [LMFeedPostAdapterListener](https://docs.likeminds.community/))**                     | Initializes the adapter and sets a listener for post actions.                              |
| **setAdapter()**                                                                          | Sets the adapter for the list view.                                                        |
| **setPaginationScrollListener(scrollListener: [LMFeedEndlessRecyclerViewScrollListener](https://docs.likeminds.community/))** | Sets the pagination scroll listener.                                                      |
| **resetScrollListenerData()**                                                             | Resets the scroll listener's data.                                                         |
| **allPosts(): [List]([LMFeedBaseViewType](https://docs.likeminds.community/))**                                             | Retrieves all posts from the list.                                                         |
| **replacePosts(posts: [List]([LMFeedPostViewData](https://docs.likeminds.community/)))**                                    | Replaces the current list of posts with a new list.                                        |
| **addPosts(posts: [List]([LMFeedPostViewData](https://docs.likeminds.community/)))**                                        | Adds a list of posts to the current list.                                                  |
| **removePostAtIndex(index: [Int](https://docs.likeminds.community/))**                                                     | Removes a post at the specified index.                                                     |
| **clearPostsAndNotify()**                                                                 | Clears all posts and notifies the adapter.                                                 |
| **getIndexAndPostFromAdapter(postId: [String](https://docs.likeminds.community/)): [Pair]([Int](https://docs.likeminds.community/), [LMFeedPostViewData](https://docs.likeminds.community/))** | Retrieves the index and post data from the adapter based on the post ID.                  |
| **updatePostWithoutNotifying(position: [Int](https://docs.likeminds.community/), postItem: [LMFeedPostViewData](https://docs.likeminds.community/))**       | Updates a post item at the specified position without notifying the adapter.               |
| **updatePostItem(position: [Int](https://docs.likeminds.community/), updatedPostItem: [LMFeedPostViewData](https://docs.likeminds.community/))**            | Updates a post item at the specified position and notifies the adapter.                    |
| **scrollToPositionWithOffset(position: [Int](https://docs.likeminds.community/))**                                         | Scrolls to the specified position with an offset.                                          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/view/LMFeedSocialFeedListView.kt)



================================================
File: feed/Android/Core/Widgets/LMFeedTopicSelectorBarView.md
================================================
---
sidebar_position: 16
title: Topic Selection Bar 
slug: /android/core/widgets/topic-selection-bar
---

# **Widget Documentation: LMFeedTopicSelectorBarView**

## **Widget: LMFeedTopicSelectorBarView**
The `LMFeedTopicSelectorBarView` is a customizable bar widget for topic selection, supporting features like managing selected topics, clear options, and click listeners, with configurable styles.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(topicSelectorBarStyle: [LMFeedTopicSelectorBarViewStyle](../Widgets/LMFeedTopicSelectorBarView.md))**                   | Applies the given style to the topic selector bar.                                          |
| **setAllTopicsText(allTopicsText: [String](https://docs.likeminds.community/))**                                            | Sets the text for the "All Topics" label.                                                  |
| **setClearTopicsText(clearTopicsText: [String](https://docs.likeminds.community/))**                                        | Sets the text for the "Clear Topics" label.                                                |
| **setAllTopicsClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the "All Topics" label.                                     |
| **setClearSelectedTopicsClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**              | Registers a click listener for the "Clear Topics" label.                                   |
| **setAllTopicsTextVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                                     | Toggles the visibility of the "All Topics" label.                                          |
| **setSelectedTopicFilterVisibility(isVisible: [Boolean](https://docs.likeminds.community/))**                              | Toggles the visibility of the selected topic filter.                                       |
| **setSelectedTopicAdapter(listener: [LMFeedSelectedTopicAdapterListener](https://docs.likeminds.community/))**             | Sets the adapter for the selected topics.                                                  |
| **getAllSelectedTopics(): [List]([LMFeedBaseViewType](https://docs.likeminds.community/))**                                 | Retrieves all selected topics.                                                             |
| **replaceSelectedTopics(selectedTopics: [List]([LMFeedTopicViewData](https://docs.likeminds.community/)))**                | Replaces the current list of selected topics with a new list.                              |
| **clearSelectedTopicsAndNotify()**                                                        | Clears all selected topics and notifies the adapter.                                       |
| **removeTopicAndNotify(position: [Int](https://docs.likeminds.community/))**                                               | Removes a topic at the specified position and notifies the adapter.                        |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/view/LMFeedTopicSelectorBarView.kt)

## **View Style: LMFeedTopicSelectorBarViewStyle**
The `LMFeedTopicSelectorBarViewStyle` defines the appearance and layout properties for the `LMFeedTopicSelectorBarView`, including configurations for text, icons, and background.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **allTopicsSelectorStyle**   | Configures the text style for the "All Topics" label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **clearTopicFilterStyle**    | Configures the text style for the "Clear Topics" label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **selectedTopicTextStyle**   | Configures the text style for the selected topics. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **removeSelectedTopicIconStyle** | Configures the style for the remove icon on selected topics. | [LMFeedIconStyle](../Widgets/Fundamentals/LMFeedIcon.md) |
| **backgroundColor**          | Specifies the background color of the topic selector bar. | [Int](https://docs.likeminds.community/)           |
| **elevation**                | Specifies the elevation of the topic selector bar. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/socialfeed/style/LMFeedTopicSelectorBarViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedUserView.md
================================================
---
sidebar_position: 13
title: User
slug: /android/core/widgets/user
---

# **Widget Documentation: LMFeedUserView**

## **Widget: LMFeedUserView**
The `LMFeedUserView` is a customizable widget for displaying user information, including profile image, name, and title, with configurable styles.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(userViewStyle: [LMFeedUserViewStyle](../Widgets/LMFeedUserView.md))**                                       | Applies the given style to the user view.                                                  |
| **setUserImage(user: [LMFeedUserViewData](https://docs.likeminds.community/))**                                             | Sets the user's profile image.                                                             |
| **setUserName(userName: [String](https://docs.likeminds.community/))**                                                     | Sets the user's name.                                                                      |
| **setUserTitle(userTitle: [String](https://docs.likeminds.community/)?)**                                                  | Sets the user's title (optional).                                                         |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/user/view/LMFeedUserView.kt)

## **View Style: LMFeedUserViewStyle**
The `LMFeedUserViewStyle` defines the appearance and layout properties for the `LMFeedUserView`, including configurations for the profile image, name, and title.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **userImageViewStyle**       | Configures the style for the user's profile image.| [LMFeedImageStyle](../Widgets/Fundamentals/LMFeedImageView.md) |
| **userNameViewStyle**        | Configures the text style for the user's name.   | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **userTitleViewStyle**       | Configures the text style for the user's title.  | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/user/style/LMFeedUserViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/LMFeedViewMoreView.md
================================================
---
sidebar_position: 14
title: View More
slug: /android/core/widgets/view-more
---

# **Widget Documentation: LMFeedViewMoreView**

## **Widget: LMFeedViewMoreView**
The `LMFeedViewMoreView` is a customizable component for displaying a "View More" option with visible count details, supporting configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(viewMoreStyle: [LMFeedViewMoreViewStyle](../Widgets/LMFeedViewMoreView.md))**                                   | Applies the given style to the "View More" component.                                       |
| **setViewMoreText(viewMoreText: [String](https://docs.likeminds.community/))**                                              | Sets the text for the "View More" label.                                                   |
| **setVisibleCount(visibleCountText: [String](https://docs.likeminds.community/))**                                          | Sets the text for the visible count label.                                                 |
| **setViewMoreClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for the "View More" label.                                      |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/viewmore/view/LMFeedViewMoreView.kt)

## **View Style: LMFeedViewMoreViewStyle**
The `LMFeedViewMoreViewStyle` defines the appearance and layout properties for the `LMFeedViewMoreView`, including configurations for text styles and background color.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **viewMoreTextStyle**        | Configures the text style for the "View More" label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **visibleCountTextStyle**    | Configures the text style for the visible count label. | [LMFeedTextStyle](../Widgets/Fundamentals/LMFeedTextView.md) |
| **backgroundColor**          | Specifies the background color of the "View More" component. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/viewmore/style/LMFeedViewMoreViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/_category_.json
================================================
{
  "label": "Widgets",
  "position": 2,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Comment/LMFeedCommentComposerView.md
================================================
---
sidebar_position: 1
title: Comment Composer
slug: /android/core/widgets/fundamentals/comment-composer
---

# **Widget Documentation: LMFeedCommentComposerView**

## **Widget: LMFeedCommentComposerView**
`LMFeedCommentComposerView` is a customizable comment composer widget designed for Android applications. It allows users to input, manage, and send comments in a structured way, offering rich styling and functionality options.

| Method                                                                                     | Description                        |
|--------------------------------------------------------------------------------------------|------------------------------------|
| **setStyle(commentComposerStyle: [LMFeedCommentComposerViewStyle](../Comment/LMFeedCommentComposerView.md))**                        | Sets the overall style of the comment composer. |
| **configureCommentInput(commentInputStyle: [LMFeedEditTextStyle](../Fundamentals/LMFeedEditText.md))**                          | Configures the appearance of the comment input box. |
| **configureCommentSend(commentSendStyle: [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md))**                                | Configures the style of the send button. |
| **configureCommentRestricted(commentRestrictedStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                   | Configures the style for restricted comments. |
| **configureReplyingTo(replyingToStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md)**                                 | Configures the appearance of the "replying to" view. |
| **configureRemoveReplyingTo(removeReplyingToStyle: [LMFeedIconStyle?](../Fundamentals/LMFeedIcon.md))**                     | Configures the style of the "remove replying to" icon. |
| **setCommentInputBoxHint(hint: String)**                                                  | Sets the placeholder text for the input box. |
| **setCommentSendButton(isEnabled: Boolean = false)**                                       | Enables or disables the send button. |
| **setCommentSendClickListener(listener: LMFeedOnClickListener)**                          | Sets a listener for the send button click event. |
| **setRemoveReplyingToClickListener(listener: LMFeedOnClickListener)**                     | Sets a listener for the "remove replying to" icon click event. |
| **setReplyingView(replyingTo: String)**                                                   | Updates the view when replying to a comment. |
| **setCommentRights(hasCommentRights: Boolean)**                                           | Updates the state based on the user's comment rights. |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/comment/commentcomposer/view/LMFeedCommentComposerView.kt).

---

## **View Style: LMFeedCommentComposerViewStyle**
`LMFeedCommentComposerViewStyle` provides flexible customization options for styling the `LMFeedCommentComposerView`.

| Field                  | Description                                     | Type |
|------------------------|-------------------------------------------------|------|
| **commentInputStyle**  | Defines the style for the comment input field.  | [LMFeedEditTextStyle](../Fundamentals/LMFeedEditText.md) |
| **commentSendStyle**   | Defines the style for the send button.          | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **commentRestrictedStyle** | Defines the style for restricted comments.     | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **replyingToStyle**    | Defines the style for the "replying to" text.   | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **removeReplyingToStyle** | Defines the style for the "remove replying to" icon. | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **elevation**          | Defines the elevation of the composer.          | `Int` |
| **backgroundColor**    | Defines the background color of the composer.   | `Int` |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/comment/commentcomposer/style/LMFeedCommentComposerViewStyle.kt).




================================================
File: feed/Android/Core/Widgets/Comment/LMFeedCommentView.md
================================================
---
sidebar_position: 2
title: Comment View
slug: /android/core/widgets/fundamentals/comment-view
---

# **Widget Documentation: LMFeedCommentView**

## **Widget: LMFeedCommentView**
`LMFeedCommentView` is a customizable widget for displaying user comments in a structured and visually appealing way. It supports features like user interaction, styling, and event handling.

| Method                                                                                     | Description                        |
|--------------------------------------------------------------------------------------------|------------------------------------|
| **setStyle(commentViewStyle: [LMFeedCommentViewStyle](../Comment/LMFeedCommentView.md))**                                     | Sets the overall style of the comment view. |
| **configureCommenterImage(commenterImageViewStyle: [LMFeedImageStyle?](../Fundamentals/LMFeedImageView.md))**                   | Configures the style of the commenter's image. |
| **configureCommenterName(commenterNameTextStyle: [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md))**                        | Configures the style of the commenter's name. |
| **configureCommentContent(commentContentStyle: [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md))**                         | Configures the style of the comment content. |
| **configureMenuIcon(menuIconStyle: [LMFeedIconStyle?](../Fundamentals/LMFeedIcon.md))**                                    | Configures the style of the menu icon. |
| **configureLikeIcon(likeIconStyle: [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md))**                                      | Configures the style of the like icon. |
| **configureLikeText(likeTextStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                                    | Configures the style of the like text. |
| **configureReplyText(replyTextStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                                  | Configures the style of the reply text. |
| **configureReplyCountText(replyCountTextStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                        | Configures the style of the reply count text. |
| **configureTimestampText(timestampTextStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                         | Configures the style of the timestamp text. |
| **configureCommentEditedText(commentEditedTextStyle: [LMFeedTextStyle?](../Fundamentals/LMFeedTextView.md))**                 | Configures the style of the "comment edited" text. |
| **setCommentCreatorImage(user: [LMFeedUserViewData](../LMFeedUserView.md))**                                      | Sets the image for the comment creator. |
| **setCommentCreatorName(commenterName: String)**                                          | Sets the name of the comment creator. |
| **onClick(view: View)**                                                                   | Handles click events on the view. |
| **updateDrawState(textPaint: TextPaint)**                                                 | Updates the text appearance for the comment. |
| **setTimestamp(createdAtTimeStamp: Long)**                                               | Sets the timestamp of the comment. |
| **setCommentEdited(isEdited: Boolean)**                                                  | Updates the view when a comment is edited. |
| **setCommentLikesIcon(isLiked: Boolean = false)**                                         | Updates the like icon state. |
| **setLikesCount(likesCount: String)**                                                    | Updates the like count text. |
| **setReplyText(replyText: String)**                                                      | Updates the reply text. |
| **setRepliesCount(repliesCount: String)**                                                | Updates the reply count text. |
| **setLikesCountClickListener(listener: LMFeedOnClickListener)**                          | Sets a listener for the like count click event. |
| **setLikeIconClickListener(listener: LMFeedOnClickListener)**                            | Sets a listener for the like icon click event. |
| **setReplyClickListener(listener: LMFeedOnClickListener)**                               | Sets a listener for the reply click event. |
| **setReplyCountClickListener(listener: LMFeedOnClickListener)**                          | Sets a listener for the reply count click event. |
| **setMenuIconClickListener(listener: LMFeedOnClickListener)**                            | Sets a listener for the menu icon click event. |
| **setCommenterHeaderClickListener(listener: LMFeedOnClickListener)**                     | Sets a listener for the commenter's header click event. |
| **linkifyCommentContent(linkClickListener: LMFeedOnLinkClickListener)**                  | Converts URLs in the comment content to clickable links. |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/comment/commentlayout/style/LMFeedCommentView.kt).

---

## **View Style: LMFeedCommentViewStyle**
`LMFeedCommentViewStyle` provides flexible styling options for the `LMFeedCommentView`, allowing customization of its various elements.

| Field                  | Description                                     | Type |
|------------------------|-------------------------------------------------|------|
| **commenterImageViewStyle** | Defines the style of the commenter's image.   | [LMFeedImageStyle](../Fundamentals/LMFeedImageView.md) |
| **commenterNameTextStyle**  | Defines the style of the commenter's name.    | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **commentContentStyle**     | Defines the style of the comment content.     | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **menuIconStyle**           | Defines the style of the menu icon.           | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **likeIconStyle**           | Defines the style of the like icon.           | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **likeTextStyle**           | Defines the style of the like text.           | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **replyTextStyle**          | Defines the style of the reply text.          | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **replyCountTextStyle**     | Defines the style of the reply count text.    | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **timestampTextStyle**      | Defines the style of the timestamp text.      | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **commentEditedTextStyle**  | Defines the style of the "comment edited" text.| [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **backgroundColor**         | Defines the background color of the comment view.| `Int` |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/comment/commentlayout/view/LMFeedCommentViewStyle.kt).



================================================
File: feed/Android/Core/Widgets/Comment/_category_.json
================================================
{
  "label": "Comment",
  "position": 4,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Comment Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedButton.md
================================================
---
sidebar_position: 1
title: Button
slug: /android/core/widgets/fundamentals/button
---

# **Widget Documentation: LMFeedButton**

## **Widget: LMFeedButton**
`LMFeedButton` is a customizable button widget designed for use in Android applications. It allows developers to implement buttons with a wide range of styling options, including text styles, icons, and background properties.

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedButton.kt).

---

## **View Style: LMFeedButtonStyle**
`LMFeedButtonStyle` provides flexible customization options for styling the `LMFeedButton`. It allows developers to define properties such as text appearance, background color, and icon configurations.

| Field                  | Description                                     | Type |
|------------------------|-------------------------------------------------|------|
| **textStyle**          | Defines the text style for the button.          | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **backgroundColor**    | Sets the background color of the button.        | `Int` |
| **strokeColor**        | Sets the color of the button's stroke.          | `Int` |
| **strokeWidth**        | Defines the width of the button's stroke.       | `Int` |
| **elevation**          | Defines the elevation of the button.            | `Int` |
| **icon**               | Specifies the resource ID for the button's icon.| `Int` |
| **iconTint**           | Defines the tint color for the icon.            | `Int` |
| **iconSize**           | Sets the size of the icon.                      | `Int` |
| **iconGravity**        | Defines the icon's gravity within the button.   | `Int` |
| **iconPadding**        | Sets the padding around the icon.               | `Int` |
| **cornerRadius**       | Defines the corner radius of the button.        | `Int` |
| **disabledButtonColor**| Sets the color of the button when disabled.     | `Int` |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedButtonStyle.kt).




================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedChip.md
================================================
---
sidebar_position: 2
title: Chip
slug: /android/core/widgets/fundamentals/chip
---

# **Widget Documentation: LMFeedChip**

## **Widget: LMFeedChip**
`LMFeedChip` is a customizable chip widget designed for use in Android applications. It allows developers to create interactive and visually appealing chips with flexible styling options.

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedChip.kt).

---

## **View Style: LMFeedChipStyle**
`LMFeedChipStyle` provides a wide range of customization options for styling the `LMFeedChip`. Developers can define properties such as background color, stroke color, text size, and more.

| Field                  | Description                                     | Type |
|------------------------|-------------------------------------------------|------|
| **chipBackgroundColor** | Defines the background color of the chip.       | `Int` |
| **chipStrokeColor**    | Sets the stroke color of the chip.              | `Int` |
| **chipTextColor**      | Specifies the text color of the chip.           | `Int` |
| **chipStrokeWidth**    | Defines the width of the chip's stroke.         | `Int` |
| **chipMinHeight**      | Sets the minimum height for the chip.           | `Int` |
| **chipStartPadding**   | Defines the start padding for the chip.         | `Int` |
| **chipEndPadding**     | Defines the end padding for the chip.           | `Int` |
| **chipCornerRadius**   | Specifies the corner radius of the chip.        | `Int` |
| **chipTextSize**       | Defines the size of the chip's text.            | `Int` |
| **chipIcon**           | Sets the resource ID for the chip's icon.       | `Int` |
| **chipIconSize**       | Defines the size of the chip's icon.            | `Int` |
| **chipIconTint**       | Specifies the tint color for the chip's icon.   | `Int` |

View the source code on [GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedChipStyle.kt).



 


================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedChipGroup.md
================================================
---
sidebar_position: 3
title: Chip Group
slug: /android/core/widgets/fundamentals/chip-group
---

# **Widget Documentation: LMFeedChipGroup**

## **Widget: LMFeedChipGroup**
The `LMFeedChipGroup` is a custom UI component designed to manage and display a group of chips in a structured layout, providing features like single-line mode and customizable spacing.

| Method                | Description                                   |
|-----------------------|-----------------------------------------------|
| **removeAllChips()** | Clears all the chips currently present in the group. |
| **addChip(chipText: [String](https://docs.likeminds.community/)? = null, chipStyle: [LMFeedChipStyle](../Fundamentals/LMFeedChip.md), chipClickListener: [LMFeedOnClickListener](https://docs.likeminds.community/)? = null)** | Adds a new chip to the group with optional text, style, and a click listener. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedChipGroup.kt)

## **View Style: LMFeedChipGroupStyle**
The `LMFeedChipGroupStyle` defines the appearance and layout properties for the `LMFeedChipGroup`, enabling customization for spacing and orientation.

| Field                        | Description                                       | Type   |
|------------------------------|---------------------------------------------------|--------|
| **isSingleLine**             | Indicates whether the chip group is displayed in a single line. | [Boolean](https://docs.likeminds.community/) |
| **chipGroupHorizontalSpacing** | Specifies the horizontal spacing between chips. | [Int](https://docs.likeminds.community/) |
| **chipGroupVerticalSpacing** | Specifies the vertical spacing between chips.    | [Int](https://docs.likeminds.community/) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedChipGroupStyle.kt)




================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedEditText.md
================================================
---
sidebar_position: 4
title: Edit Text
slug: /android/core/widgets/fundamentals/edit-text
---

# **Widget Documentation: LMFeedEditText**

## **Widget: LMFeedEditText**
The `LMFeedEditText` is a custom `EditText` widget providing advanced capabilities such as handling focus changes and dynamic keyboard interactions.

| Method                                             | Description                                               |
|----------------------------------------------------|-----------------------------------------------------------|
| **onWindowFocusChanged(hasWindowFocus: [Boolean](https://docs.likeminds.community/))** | Handles changes in window focus.                         |
| **focusAndShowKeyboard()**                        | Focuses the `EditText` and displays the keyboard.         |
| **maybeShowKeyboard()**                           | Conditionally shows the keyboard based on the current state. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedEditText.kt)

## **View Style: LMFeedEditTextStyle**
The `LMFeedEditTextStyle` defines the appearance and layout properties for the `LMFeedEditText`, enabling customization of its text, colors, and elevation.

| Field                | Description                                   | Type             |
|----------------------|-----------------------------------------------|------------------|
| **inputTextStyle**   | Specifies the style of the input text.        | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **hintTextColor**    | Defines the color of the hint text.           | [Int](https://docs.likeminds.community/)          |
| **elevation**        | Sets the elevation of the `EditText`.         | [Int](https://docs.likeminds.community/)          |
| **backgroundColor**  | Specifies the background color.               | [Int](https://docs.likeminds.community/)          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedEditTextStyle.kt)












================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedFAB.md
================================================
---
sidebar_position: 10
title: FAB
slug: /android/core/widgets/fundamentals/fab
---

# **Widget Documentation: LMFeedFAB**

## **Widget: LMFeedFAB**
The `LMFeedFAB` is a custom Floating Action Button (FAB) designed for enhanced functionality and customization, including support for extended mode, icons, and text styles.

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedFAB.kt)

## **View Style: LMFeedFABStyle**
The `LMFeedFABStyle` defines the appearance and layout properties for the `LMFeedFAB`, allowing customization for background color, stroke, icon, and text styling.

| Field               | Description                                         | Type             |
|---------------------|-----------------------------------------------------|------------------|
| **isExtended**      | Indicates whether the FAB is in extended mode.      | [Boolean](https://docs.likeminds.community/)      |
| **backgroundColor** | Specifies the background color of the FAB.          | [Int](https://docs.likeminds.community/)          |
| **strokeColor**     | Defines the stroke color of the FAB.                | [Int](https://docs.likeminds.community/)          |
| **strokeWidth**     | Sets the width of the FAB's stroke.                 | [Int](https://docs.likeminds.community/)          |
| **elevation**       | Specifies the elevation of the FAB.                 | [Int](https://docs.likeminds.community/)          |
| **icon**            | Identifies the icon resource for the FAB.           | [Int](https://docs.likeminds.community/)          |
| **iconTint**        | Defines the tint color for the FAB icon.            | [Int](https://docs.likeminds.community/)          |
| **iconSize**        | Specifies the size of the FAB icon.                 | [Int](https://docs.likeminds.community/)          |
| **iconPadding**     | Sets the padding around the icon within the FAB.    | [Int](https://docs.likeminds.community/)          |
| **textStyle**       | Defines the style of the FAB's text.                | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedFABStyle.kt)




================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedIcon.md
================================================
---
sidebar_position: 5
title: Icon
slug: /android/core/widgets/fundamentals/icon
---

# **Widget Documentation: LMFeedIcon**

## **Widget: LMFeedIcon**
The `LMFeedIcon` is a customizable icon widget designed to handle active and inactive states with support for tinting, scaling, and padding.

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedIcon.kt)

## **View Style: LMFeedIconStyle**
The `LMFeedIconStyle` defines the appearance and layout properties for the `LMFeedIcon`, allowing customization for active and inactive states, icon tinting, padding, and background color.

| Field               | Description                                              | Type             |
|---------------------|----------------------------------------------------------|------------------|
| **activeSrc**       | Specifies the resource for the active state icon.        | [Int](https://docs.likeminds.community/)          |
| **inActiveSrc**     | Specifies the resource for the inactive state icon.      | [Int](https://docs.likeminds.community/)          |
| **iconTint**        | Defines the tint color for the icon.                     | [Int](https://docs.likeminds.community/)          |
| **elevation**       | Sets the elevation of the icon.                          | [Int](https://docs.likeminds.community/)          |
| **alpha**           | Determines the transparency level of the icon.           | [Float](https://docs.likeminds.community/)        |
| **scaleType**       | Specifies the scaling type for the icon display.         | [ScaleType](https://docs.likeminds.community/)    |
| **iconPadding**     | Defines the padding around the icon.                     | [LMFeedPadding](https://docs.likeminds.community/)|
| **backgroundColor** | Specifies the background color of the icon.              | [Int](https://docs.likeminds.community/)          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedIconStyle.kt)





================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedImageView.md
================================================
---
sidebar_position: 6
title: Image View
slug: /android/core/widgets/fundamentals/image-view
---

# **Widget Documentation: LMFeedImageView**

## **Widget: LMFeedImageView**
The `LMFeedImageView` is a custom `ImageView` component that supports dynamic image loading, circular shapes, grayscale rendering, and corner radius adjustments.

| Method                                                                                   | Description                            |
|------------------------------------------------------------------------------------------|----------------------------------------|
| **setImage(imageSrc: [Any](https://docs.likeminds.community/)?, imageViewStyle: [LMFeedImageStyle](../Fundamentals/LMFeedImageView.md))**                  | Sets the image source and applies the specified style. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedImageView.kt)

## **View Style: LMFeedImageStyle**
The `LMFeedImageStyle` defines the appearance and layout properties for the `LMFeedImageView`, including options for circular images, grayscale rendering, and corner radius adjustments.

| Field              | Description                                          | Type          |
|--------------------|------------------------------------------------------|---------------|
| **imageSrc**       | Specifies the source of the image.                  | [Any](https://docs.likeminds.community/)       |
| **placeholderSrc** | Defines the source for the placeholder image.       | [Any](https://docs.likeminds.community/)       |
| **isCircle**       | Indicates whether the image should be circular.     | [Boolean](https://docs.likeminds.community/)   |
| **showGreyScale**  | Determines whether the image is displayed in grayscale. | [Boolean](https://docs.likeminds.community/)   |
| **cornerRadius**   | Specifies the corner radius for the image.          | [Int](https://docs.likeminds.community/)       |
| **imageTint**      | Sets the tint color for the image.                  | [Int](https://docs.likeminds.community/)       |
| **alpha**          | Controls the transparency of the image.             | [Float](https://docs.likeminds.community/)     |
| **scaleType**      | Specifies how the image should be scaled to fit the view. | [ScaleType](https://docs.likeminds.community/) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedImageStyle.kt)




================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedProgressBar.md
================================================
---
sidebar_position: 7
title: Progress Bar
slug: /android/core/widgets/fundamentals/progress-bar
---

# **Widget Documentation: LMFeedProgressBar**

## **Widget: LMFeedProgressBar**
The `LMFeedProgressBar` is a helper utility for managing the display of progress bars with support for visibility checks and background options.

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/utils/LMFeedProgressBarHelper.kt)

## **View Style: LMFeedProgressBarStyle**
The `LMFeedProgressBarStyle` defines the appearance and behavior properties for the `LMFeedProgressBar`, including color, mode, and maximum value.

| Field             | Description                                      | Type      |
|-------------------|--------------------------------------------------|-----------|
| **progressColor** | Specifies the color of the progress bar.         | [Int](https://docs.likeminds.community/)   |
| **isIndeterminate** | Indicates whether the progress bar is in indeterminate mode. | [Boolean](https://docs.likeminds.community/) |
| **maxProgress**   | Sets the maximum value of the progress bar.      | [Int](https://docs.likeminds.community/)   |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedProgressBarStyle.kt)





================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedSwitch.md
================================================
---
sidebar_position: 8
title: Switch
slug: /android/core/widgets/fundamentals/switch
---

# **Widget Documentation: LMFeedSwitch**

## **Widget: LMFeedSwitch**
The `LMFeedSwitch` is a custom switch widget designed with advanced styling options, such as customizable text, thumb color, and track color.

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedSwitch.kt)

## **View Style: LMFeedSwitchStyle**
The `LMFeedSwitchStyle` defines the appearance and layout properties for the `LMFeedSwitch`, including options for text styling, thumb and track colors, and icons.

| Field              | Description                                       | Type             |
|--------------------|---------------------------------------------------|------------------|
| **textStyle**      | Specifies the style of the text associated with the switch. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **thumbColor**     | Defines the color of the switch's thumb.          | [Int](https://docs.likeminds.community/)          |
| **trackColor**     | Specifies the color of the switch's track.        | [Int](https://docs.likeminds.community/)          |
| **thumbIcon**      | Sets the icon resource for the switch's thumb.    | [Int](https://docs.likeminds.community/)          |
| **thumbIconColor** | Defines the tint color for the thumb icon.        | [Int](https://docs.likeminds.community/)          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedSwitchStyle.kt)





================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedTextView.md
================================================
---
sidebar_position: 11
title: Text View
slug: /android/core/widgets/fundamentals/text-view
---

# **Widget Documentation: LMFeedTextView**

## **Widget: LMFeedTextView**
The `LMFeedTextView` is a versatile text component with advanced customization options such as font resources, drawables, and expandable call-to-actions.

| Method               | Description                                   |
|----------------------|-----------------------------------------------|
| **clearDrawables()** | Removes all drawable resources attached to the `TextView`. |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedTextView.kt)

## **View Style: LMFeedTextStyle**
The `LMFeedTextStyle` defines the appearance and layout properties for the `LMFeedTextView`, allowing customization for text styling, drawables, and alignment.

| Field                | Description                                                | Type          |
|----------------------|------------------------------------------------------------|---------------|
| **textColor**        | Specifies the color of the text.                           | [Int](https://docs.likeminds.community/)       |
| **textSize**         | Defines the size of the text.                              | [Int](https://docs.likeminds.community/)       |
| **textAllCaps**      | Indicates whether the text should be displayed in all caps. | [Boolean](https://docs.likeminds.community/)   |
| **fontResource**     | Specifies the font resource for the text.                  | [Int](https://docs.likeminds.community/)       |
| **fontAssetsPath**   | Path to the font file in assets.                           | [String](https://docs.likeminds.community/)    |
| **typeface**         | Sets the typeface of the text.                             | [Int](https://docs.likeminds.community/)       |
| **maxLines**         | Specifies the maximum number of lines for the text.        | [Int](https://docs.likeminds.community/)       |
| **ellipsize**        | Determines how to truncate text that exceeds available space. | [TruncateAt](https://docs.likeminds.community/) |
| **maxHeight**        | Sets the maximum height of the `TextView`.                 | [Int](https://docs.likeminds.community/)       |
| **minHeight**        | Sets the minimum height of the `TextView`.                 | [Int](https://docs.likeminds.community/)       |
| **backgroundColor**  | Specifies the background color of the `TextView`.          | [Int](https://docs.likeminds.community/)       |
| **textAlignment**    | Defines the alignment of the text.                         | [Int](https://docs.likeminds.community/)       |
| **elevation**        | Sets the elevation of the `TextView`.                      | [Int](https://docs.likeminds.community/)       |
| **hintTextColor**    | Specifies the color of the hint text.                      | [Int](https://docs.likeminds.community/)       |
| **drawableLeftSrc**  | Resource ID for the left drawable.                         | [Int](https://docs.likeminds.community/)       |
| **drawableTopSrc**   | Resource ID for the top drawable.                          | [Int](https://docs.likeminds.community/)       |
| **drawableRightSrc** | Resource ID for the right drawable.                        | [Int](https://docs.likeminds.community/)       |
| **drawableBottomSrc**| Resource ID for the bottom drawable.                       | [Int](https://docs.likeminds.community/)       |
| **drawablePadding**  | Padding between text and drawables.                        | [Int](https://docs.likeminds.community/)       |
| **expandableCTAText**| Text for the "expandable" call-to-action.                  | [String](https://docs.likeminds.community/)    |
| **expandableCTAColor** | Color of the "expandable" call-to-action text.           | [Int](https://docs.likeminds.community/)       |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/styles/LMFeedTextStyle.kt)




================================================
File: feed/Android/Core/Widgets/Fundamentals/LMFeedVideoView.md
================================================
---
sidebar_position: 9
title: Video
slug: /android/core/widgets/fundamentals/video
---

# **Widget Documentation: 'LMFeedVideoView'**

## **Widget: 'LMFeedVideoView'**
The `LMFeedVideoView` is a custom widget designed for handling video playback in the LikeMinds feed. It supports playing videos from both local and remote sources and includes functionalities like caching, thumbnail management, and customizable styles.

| Method | Description |
|--------|-------------|
| **fun init()** | Initializes the video player for use. |
| **fun onPlaybackStateChanged(playbackState: Int)** | Handles changes in the video playback state. |
| **fun startPlayingRemoteUri(videoUri: Uri, progressBar: [LMFeedProgressBar](../Fundamentals/LMFeedProgressBar.md), thumbnailView: [LMFeedImageView](../Fundamentals/LMFeedImageView.md), thumbnailSrc: Any? = null)** | Starts playing a video from a remote URI. Displays a progress bar and manages a thumbnail. |
| **fun createCachedMediaSource(context: Context, uri: Uri)** | Creates a cached media source for efficient playback of videos. |
| **fun inferContentType(uri: Uri)** | Infers the content type of the video based on its URI. |
| **fun startPlayingLocalUri(videoUri: Uri, progressBar: [LMFeedProgressBar](../Fundamentals/LMFeedProgressBar.md), thumbnailView: [LMFeedImageView](../Fundamentals/LMFeedImageView.md), thumbnailSrc: Any? = null)** | Starts playing a video from a local URI. Displays a progress bar and manages a thumbnail. |
| **fun removePlayer()** | Removes and releases the video player resources. |
| **fun setStyle(postVideoMediaStyle: [LMFeedPostVideoMediaViewStyle](../Post/Media/LMFeedPostVideoMediaView.md))** | Applies a specific style configuration to the video view. |
| **fun setThumbnail(thumbnailView: [LMFeedImageView](../Fundamentals/LMFeedImageView.md), thumbnailSrc: Any?)** | Sets a thumbnail for the video view. |

[View LMFeedVideoView on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/base/views/LMFeedVideoView.kt)

## **View Style: 'LMFeedPostVideoMediaViewStyle'**
The `LMFeedPostVideoMediaViewStyle` defines the visual configuration for the video view widget, including styles for its thumbnail, progress bar, play/pause button, and other customizable elements.

| Field                   | Description                                           | Type                       |
|--------------------------|-------------------------------------------------------|----------------------------|
| **videoThumbnailStyle**    | The style for the video thumbnail.                    | **[LMFeedImageStyle?](../Fundamentals/LMFeedImageView.md)**        |
| **videoProgressStyle**     | The style for the progress bar displayed on the video.| **[LMFeedProgressBarStyle?](../Fundamentals/LMFeedProgressBar.md)**  |
| **videoPlayPauseButton**   | The style for the play/pause button on the video.     | **[LMFeedIconStyle](../Fundamentals/LMFeedIcon.md)**         |
| **videoMuteUnmuteButton**  | The style for the mute/unmute button on the video.    | **[LMFeedIconStyle?](../Fundamentals/LMFeedIcon.md)**         |
| **showController**         | Indicates whether the video controller is shown.      | `Boolean`                  |
| **keepScreenOn**           | Keeps the screen on while the video is playing.       | `Boolean`                  |
| **controllerAutoShow**     | Automatically shows the controller when video starts. | `Boolean`                  |
| **controllerShowTimeoutMs**| Timeout for hiding the video controller.              | `Int`                      |
| **backgroundColor**        | The background color for the video view.             | `Int?`                     |
| **removeIconStyle**        | Style for the remove icon on the video view.          | **[LMFeedIconStyle](../Fundamentals/LMFeedIcon.md)**         |

[View LMFeedPostVideoMediaViewStyle on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/style/LMFeedPostVideoMediaViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Fundamentals/_category_.json
================================================
{
  "label": "Fundamentals",
  "position": 1,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Fundamentals Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Poll/LMFeedPollOptionView.md
================================================
---
sidebar_position: 2
title: Poll Options 
slug: /android/core/widgets/poll/poll-options
---

# **Widget Documentation: LMFeedPollOptionView**

## **Widget: LMFeedPollOptionView**
The `LMFeedPollOptionView` represents a customizable view for a single poll option, enabling advanced styling, configuration, and interaction options.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postPollOptionViewStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md))**                   | Applies the given style to the poll option view.                                           |
| **configurePollOptionText(pollOptionTextStyle: [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md))**                     | Configures the text style for the poll option.                                             |
| **configurePollOptionAddedByText(pollOptionAddedByTextStyle: [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md))**       | Configures the text style for the "added by" information.                                  |
| **configurePollOptionCheckedIcon(pollOptionCheckIconStyle: [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md))**         | Configures the style of the checked icon.                                                  |
| **configurePollOptionVotesCountText(pollOptionVotesCountTextStyle: [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md))** | Configures the text style for the votes count.                                             |
| **setPollOptionText(pollOptionText: [String](https://docs.likeminds.community/))**                                          | Sets the text for the poll option.                                                        |
| **setPollOptionAddedByText(pollOptionViewData: [LMFeedPollOptionViewData](https://docs.likeminds.community/), pollOptionViewStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md))** | Sets the "added by" text for the poll option.                   |
| **setPollOptionCheckedIconVisibility(pollOptionViewData: [LMFeedPollOptionViewData](https://docs.likeminds.community/), pollOptionViewStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md))** | Configures the visibility of the checked icon.         |
| **setPollVotesCountText(pollOptionViewData: [LMFeedPollOptionViewData](https://docs.likeminds.community/), pollOptionViewStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md))** | Sets the text for the poll option votes count.               |
| **setPollOptionBackgroundAndProgress(pollOptionViewData: [LMFeedPollOptionViewData](https://docs.likeminds.community/), pollOptionViewStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md))** | Configures the background and progress for the poll option. |
| **setPollOptionClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                             | Registers a click listener for the poll option.                                            |
| **setPollOptionVotesCountClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                   | Registers a click listener for the poll option votes count.                                |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/poll/view/LMFeedPollOptionView.kt)

## **View Style: LMFeedPostPollOptionViewStyle**
The `LMFeedPostPollOptionViewStyle` defines the appearance and layout properties for the `LMFeedPollOptionView`, enabling customization for text, colors, and icons.

| Field                           | Description                                         | Type              |
|---------------------------------|-----------------------------------------------------|-------------------|
| **pollOptionTextStyle**         | Defines the text style for poll options.            | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pollSelectedOptionColor**     | Specifies the color for the selected poll option.   | [Int](https://docs.likeminds.community/)           |
| **pollOtherOptionColor**        | Specifies the color for unselected poll options.    | [Int](https://docs.likeminds.community/)           |
| **pollOptionVotesCountTextStyle** | Defines the text style for displaying vote counts. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pollOptionAddedByTextStyle**  | Specifies the text style for "added by" information.| [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pollOptionCheckIconStyle**    | Defines the style of the check icon for poll options. | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/poll/style/LMFeedPostPollOptionViewStyle.kt)





================================================
File: feed/Android/Core/Widgets/Poll/LMFeedPollOptionsListView.md
================================================
---
sidebar_position: 1
title: Poll Options List
slug: /android/core/widgets/poll/poll-options-list
---

# **Widget Documentation: 'LMFeedPollOptionsListView'**

## **Widget: 'LMFeedPollOptionsListView'**
The `LMFeedPollOptionsListView` is a custom widget designed for displaying and managing a list of poll options in the LikeMinds feed. It supports customizable styling and interaction handling through an adapter.

| Method | Description |
|--------|-------------|
| **fun setAdapter(pollPosition: Int, optionStyle: [LMFeedPostPollOptionViewStyle?](../Poll/LMFeedPollOptionView.md), listener: LMFeedPollOptionsAdapterListener?)** | Sets the adapter for the poll options list, including position, style, and listener for user interactions. |
| **fun replacePollOptions(pollOptions: List&lt;[LMFeedPollOptionViewData](../Poll/LMFeedPollOptionView.md)&gt;)** | Replaces the current list of poll options with a new set of data. |

[View LMFeedPollOptionsListView on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/poll/view/LMFeedPollOptionsListView.kt)




================================================
File: feed/Android/Core/Widgets/Poll/LMFeedPostPollView.md
================================================
---
sidebar_position: 3
title: Poll  
slug: /android/core/widgets/poll/poll
---

# **Widget Documentation: LMFeedPostPollView**

## **Widget: LMFeedPostPollView**
The `LMFeedPostPollView` is a customizable view for displaying and interacting with polls, including options for configuration, styling, and click actions.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postPollViewStyle: [LMFeedPostPollViewStyle](../Poll/LMFeedPostPollView.md))**                               | Applies the given style to the poll view.                                                  |
| **setPollTitle(pollTitle: [String](https://docs.likeminds.community/))**                                                   | Sets the title of the poll.                                                                |
| **setPollInfo(pollInfo: [String](https://docs.likeminds.community/))**                                                     | Sets additional poll information.                                                          |
| **setMemberVotedCount(pollAnswerText: [String](https://docs.likeminds.community/))**                                       | Displays the count of members who have voted.                                              |
| **setTimeLeft(timeLeft: [String](https://docs.likeminds.community/))**                                                     | Sets the time left for the poll.                                                           |
| **setPollOptions(pollPosition: [Int](https://docs.likeminds.community/), options: [List]([LMFeedPollOptionViewData](https://docs.likeminds.community/)), optionStyle: [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md), listener: [LMFeedPollOptionsAdapterListener](https://docs.likeminds.community/))** | Configures the poll options. |
| **setSubmitButtonVisibility(pollViewData: [LMFeedPollViewData](https://docs.likeminds.community/))**                       | Controls the visibility of the submit button.                                              |
| **setAddPollOptionButtonVisibility(pollViewData: [LMFeedPollViewData](https://docs.likeminds.community/))**                | Controls the visibility of the "add poll option" button.                                   |
| **setEditPollVoteVisibility(pollViewData: [LMFeedPollViewData](https://docs.likeminds.community/))**                       | Controls the visibility of the "edit poll vote" option.                                    |
| **setPollTitleClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                              | Registers a click listener for the poll title.                                             |
| **setEditPollClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                               | Registers a click listener for the edit poll action.                                       |
| **setClearPollClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                              | Registers a click listener for the clear poll action.                                      |
| **setAddPollOptionClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                          | Registers a click listener for the "add poll option" button.                               |
| **setSubmitPollVoteClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for submitting poll votes.                                      |
| **setMemberVotedCountClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the member-voted count.                                     |
| **setEditPollVoteClicked(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                           | Registers a click listener for editing poll votes.                                         |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/poll/view/LMFeedPostPollView.kt)

## **View Style: LMFeedPostPollViewStyle**
The `LMFeedPostPollViewStyle` defines the appearance and layout properties for the `LMFeedPostPollView`, including text, button, and icon configurations.

| Field                           | Description                                         | Type              |
|---------------------------------|-----------------------------------------------------|-------------------|
| **pollTitleTextStyle**          | Defines the text style for the poll title.          | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pollOptionsViewStyle**        | Configures the style for poll options.              | [LMFeedPostPollOptionViewStyle](../Poll/LMFeedPollOptionView.md) |
| **membersVotedCountTextStyle**  | Sets the text style for the member-voted count.     | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pollInfoTextStyle**           | Defines the text style for additional poll information. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **submitPollVoteButtonStyle**   | Configures the style for the submit button.         | [LMFeedButtonStyle](../Fundamentals/LMFeedButton.md) |
| **pollExpiryTextStyle**         | Configures the text style for the poll expiry time. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **addPollOptionButtonStyle**    | Sets the style for the "add poll option" button.    | [LMFeedButtonStyle]../Fundamentals/LMFeedButton.md) |
| **editPollIconStyle**           | Defines the style of the edit poll icon.            | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **clearPollIconStyle**          | Defines the style of the clear poll icon.           | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **editPollVoteTextStyle**       | Configures the text style for editing poll votes.   | [LMFeedTextStyle](../Fundamentals/LMFeedIcon.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/poll/style/LMFeedPostPollViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Poll/_category_.json
================================================
{
  "label": "Poll",
  "position": 9,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Poll Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Post/LMFeedPostDetailListView.md
================================================
---
sidebar_position: 5
title: Post Detail List View
slug: /android/core/widgets/post/post-detail-list-view
---

# **Widget Documentation: LMFeedPostDetailListView**

## **Widget: LMFeedPostDetailListView**
The `LMFeedPostDetailListView` is a customizable list view designed for displaying detailed post data, supporting features like video autoplay, pagination, and dynamic item management.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **initiateVideoAutoPlayer()**                                                              | Initiates the video auto-player functionality.                                             |
| **refreshVideoAutoPlayer()**                                                              | Refreshes the video auto-player functionality.                                             |
| **destroyVideoAutoPlayer()**                                                              | Destroys the video auto-player functionality.                                              |
| **initAdapterAndSetListeners()**                                                          | Initializes the adapter and sets listeners for the list view.                              |
| **setAdapter()**                                                                          | Sets the adapter for the list view.                                                        |
| **setPaginationScrollListener(scrollListener: [LMFeedEndlessRecyclerViewScrollListener](https://docs.likeminds.community/))** | Sets the pagination scroll listener.                                                      |
| **resetScrollListenerData()**                                                             | Resets the scroll listener's data.                                                         |
| **addItem(item: [LMFeedBaseViewType](https://docs.likeminds.community/))**                                                 | Adds an item to the list.                                                                  |
| **addItem(position: [Int](https://docs.likeminds.community/), item: [LMFeedBaseViewType](https://docs.likeminds.community/))**                               | Adds an item at a specified position in the list.                                          |
| **addItems(items: [List]([LMFeedBaseViewType](https://docs.likeminds.community/)))**                                       | Adds multiple items to the list.                                                          |
| **updateItem(position: [Int](https://docs.likeminds.community/), updatedItem: [LMFeedBaseViewType](https://docs.likeminds.community/))**                    | Updates an item at a specific position in the list.                                        |
| **updateItemWithoutNotifying(position: [Int](https://docs.likeminds.community/), postItem: [LMFeedPostViewData](https://docs.likeminds.community/))**       | Updates an item at a specific position without notifying the adapter.                     |
| **replaceItems(items: [List]([LMFeedBaseViewType](https://docs.likeminds.community/)))**                                   | Replaces all items in the list.                                                           |
| **removeItem(position: [Int](https://docs.likeminds.community/))**                                                        | Removes an item at a specific position in the list.                                        |
| **getItem(position: [Int](https://docs.likeminds.community/)): [LMFeedBaseViewType](https://docs.likeminds.community/)**                                    | Retrieves an item at a specific position in the list.                                      |
| **items(): [List]([LMFeedBaseViewType](https://docs.likeminds.community/))**                                              | Retrieves all items in the list.                                                          |
| **getIndexAndCommentFromAdapter(commentId: [String](https://docs.likeminds.community/)): [Pair]([Int](https://docs.likeminds.community/), [LMFeedCommentViewData](https://docs.likeminds.community/))** | Retrieves the index and comment from the adapter based on a comment ID.                   |
| **getIndexAndCommentFromAdapterUsingTempId(tempId: [String](https://docs.likeminds.community/)?): [Pair]([Int](https://docs.likeminds.community/), [LMFeedCommentViewData](https://docs.likeminds.community/))** | Retrieves the index and comment from the adapter based on a temporary ID.                 |
| **getIndexAndReplyFromComment()**                                                        | Retrieves the index and reply from a comment.                                              |
| **scrollToPositionWithOffset(position: [Int](https://docs.likeminds.community/), offset: [Int](https://docs.likeminds.community/))**                       | Scrolls to a specific position with an offset.                                             |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/post/detail/view/LMFeedPostDetailListView.kt)




================================================
File: feed/Android/Core/Widgets/Post/LMFeedPostHeaderView.md
================================================
---
sidebar_position: 1
title: Post Header
slug: /android/core/widgets/post/post-header
---

# **Widget Documentation: LMFeedPostHeaderView**

## **Widget: LMFeedPostHeaderView**
The `LMFeedPostHeaderView` is a customizable header view for posts, supporting elements like author information, timestamps, pinned status, and menu actions with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postHeaderViewStyle: [LMFeedPostHeaderViewStyle](../Post/LMFeedPostHeaderView.md))**                           | Applies the given style to the post header view.                                           |
| **setAuthorImage(user: [LMFeedUserViewData](https://docs.likeminds.community/))**                                           | Sets the author's image.                                                                   |
| **setAuthorName(authorName: [String](https://docs.likeminds.community/))**                                                 | Sets the author's name.                                                                    |
| **setTimestamp(createdAtTimeStamp: [Long](https://docs.likeminds.community/))**                                            | Sets the timestamp of the post.                                                           |
| **setPostEdited(isEdited: [Boolean](https://docs.likeminds.community/))**                                                  | Sets whether the post has been edited.                                                    |
| **setPinIcon(isPinned: [Boolean](https://docs.likeminds.community/))**                                                     | Sets whether the post is pinned.                                                          |
| **setAuthorCustomTitle(customTitle: [String](https://docs.likeminds.community/))**                                         | Sets a custom title for the author.                                                       |
| **setAuthorFrameClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the author frame.                                          |
| **setMenuIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for the menu icon.                                             |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postheaderview/view/LMFeedPostHeaderView.kt)

## **View Style: LMFeedPostHeaderViewStyle**
The `LMFeedPostHeaderViewStyle` defines the appearance and layout properties for the `LMFeedPostHeaderView`, including configurations for author details, timestamps, and icons.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **authorImageViewStyle**     | Configures the style for the author's image.     | [LMFeedImageStyle](../Fundamentals/LMFeedImageView.md) |
| **authorNameViewStyle**      | Configures the text style for the author's name. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **timestampTextStyle**       | Configures the text style for the timestamp.     | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **postEditedTextStyle**      | Configures the text style for the "Edited" label.| [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **authorCustomTitleTextStyle** | Configures the text style for the custom title of the author. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **pinIconStyle**             | Configures the style for the pin icon.           | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **menuIconStyle**            | Configures the style for the menu icon.          | [LMFeedIconStyle](../Fundamentals/LMFeedIcon.md) |
| **backgroundColor**          | Specifies the background color of the post header view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postheaderview/style/LMFeedPostHeaderViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Post/LMFeedPostTopResponseView.md
================================================
---
sidebar_position: 4
title: Post Top Response
slug: /android/core/widgets/post/post-top-response
---

# **Widget Documentation: LMFeedPostTopResponseView**

## **Widget: LMFeedPostTopResponseView**
The `LMFeedPostTopResponseView` is a customizable view for displaying a top response, including author details, content, and timestamps, with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postTopResponseViewStyle: [LMFeedPostTopResponseViewStyle](../Post/LMFeedPostTopResponseView.md))**                 | Applies the given style to the top response view.                                          |
| **setTopResponseTitle(title: [String](https://docs.likeminds.community/))**                                                 | Sets the title of the top response.                                                        |
| **setAuthorImage(user: [LMFeedUserViewData](https://docs.likeminds.community/))**                                           | Sets the author's image.                                                                   |
| **setAuthorName(authorName: [String](https://docs.likeminds.community/))**                                                 | Sets the author's name.                                                                    |
| **setTopResponseContent(content: [String](https://docs.likeminds.community/))**                                            | Sets the content of the top response.                                                     |
| **setTimestamp(createdAtTimeStamp: [Long](https://docs.likeminds.community/))**                                            | Sets the timestamp of the top response.                                                   |
| **setAuthorFrameClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the author frame.                                          |
| **setTopResponseClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the top response.                                          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/posttopresponse/view/LMFeedPostTopResponseView.kt)

## **View Style: LMFeedPostTopResponseViewStyle**
The `LMFeedPostTopResponseViewStyle` defines the appearance and layout properties for the `LMFeedPostTopResponseView`, including configurations for text, images, and background.

| Field                        | Description                                      | Type              |
|------------------------------|--------------------------------------------------|-------------------|
| **titleTextStyle**           | Configures the text style for the title.         | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **authorImageViewStyle**     | Configures the style for the author's image.     | [LMFeedImageStyle](../Fundamentals/LMFeedImageView.md) |
| **authorNameTextStyle**      | Configures the text style for the author's name. | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **timestampTextStyle**       | Configures the text style for the timestamp.     | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **contentTextStyle**         | Configures the text style for the content.       | [LMFeedTextStyle](../Fundamentals/LMFeedTextView.md) |
| **backgroundColor**          | Specifies the background color of the top response view. | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/posttopresponse/style/LMFeedPostTopResponseViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Post/_category_.json
================================================
{
  "label": "Post",
  "position": 10,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Post Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Post/Action/LMFeedPostActionHorizontalView.md
================================================
---
sidebar_position: 1
title: Post Action Horizontal
slug: /android/core/widgets/post/action/post-action-horizontal
---

# **Widget Documentation: LMFeedPostActionHorizontalView**

## **Widget: LMFeedPostActionHorizontalView**
The `LMFeedPostActionHorizontalView` is a customizable horizontal action bar for posts, supporting actions like liking, commenting, saving, and sharing with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postActionViewStyle: [LMFeedPostActionViewStyle](../Action/LMFeedPostActionHorizontalView.md))**                           | Applies the given style to the post action view.                                           |
| **setLikesCount(likesCount: [String](https://docs.likeminds.community/))**                                                 | Sets the count of likes.                                                                   |
| **setCommentsCount(commentsCount: [String](https://docs.likeminds.community/))**                                           | Sets the count of comments.                                                                |
| **setLikesIcon(isLiked: [Boolean](https://docs.likeminds.community/) = false)**                                            | Configures the state of the "Like" icon.                                                  |
| **setLikeIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for the "Like" icon.                                           |
| **setLikesCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the likes count.                                           |
| **setCommentsCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                    | Registers a click listener for the comments count.                                        |
| **setSaveIcon(isSaved: [Boolean](https://docs.likeminds.community/) = false)**                                             | Configures the state of the "Save" icon.                                                  |
| **setSaveIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                              | Registers a click listener for the "Save" icon.                                           |
| **setShareIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                             | Registers a click listener for the "Share" icon.                                          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postactionview/view/LMFeedPostActionHorizontalView.kt)

## **View Style: LMFeedPostActionViewStyle**
The `LMFeedPostActionViewStyle` defines the appearance and layout properties for the `LMFeedPostActionHorizontalView`, including text and icon configurations.

| Field                | Description                                      | Type              |
|----------------------|--------------------------------------------------|-------------------|
| **likeIconStyle**    | Defines the style of the "Like" icon.            | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **likeTextStyle**    | Configures the text style for the "Like" option. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **commentTextStyle** | Configures the text style for the "Comments" option. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **saveIconStyle**    | Defines the style of the "Save" icon.            | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **shareIconStyle**   | Defines the style of the "Share" icon.           | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **menuIconStyle**    | Defines the style of the "Menu" icon.            | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **backgroundColor**  | Specifies the background color of the view.      | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postactionview/style/LMFeedPostActionViewStyle.kt)





================================================
File: feed/Android/Core/Widgets/Post/Action/LMFeedPostActionVerticalView.md
================================================
---
sidebar_position: 2
title: Post Action Vertical
slug: /android/core/widgets/post/action/post-action-vertical
---

# **Widget Documentation: LMFeedPostActionVerticalView**

## **Widget: LMFeedPostActionVerticalView**
The `LMFeedPostActionVerticalView` is a customizable vertical action bar for posts, supporting actions like liking, commenting, sharing, and menu options with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postActionViewStyle: [LMFeedPostActionViewStyle](../Action/LMFeedPostActionHorizontalView.md))**                           | Applies the given style to the post action view.                                           |
| **setLikesCount(likesCount: [String](https://docs.likeminds.community/))**                                                 | Sets the count of likes.                                                                   |
| **setCommentsCount(commentsCount: [String](https://docs.likeminds.community/))**                                           | Sets the count of comments.                                                                |
| **setLikesIcon(isLiked: [Boolean](https://docs.likeminds.community/) = false)**                                            | Configures the state of the "Like" icon.                                                  |
| **setLikeIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                         | Registers a click listener for the "Like" icon.                                           |
| **setLikesCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the likes count.                                           |
| **setCommentsCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                    | Registers a click listener for the comments count.                                        |
| **setShareIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                             | Registers a click listener for the "Share" icon.                                          |
| **setMenuIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                              | Registers a click listener for the "Menu" icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postactionview/view/LMFeedPostActionVerticalView.kt)





================================================
File: feed/Android/Core/Widgets/Post/Action/LMFeedPostQnAActionHorizontalView.md
================================================
---
sidebar_position: 3
title: Post QnA Action Horizontal
slug: /android/core/widgets/post/action/post-qna-action-horizontal
---

# **Widget Documentation: LMFeedPostQnAActionHorizontalView**

## **Widget: LMFeedPostQnAActionHorizontalView**
The `LMFeedPostQnAActionHorizontalView` is a customizable horizontal action bar for Q&A posts, supporting actions like upvoting, commenting, saving, and sharing with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postActionViewStyle: [LMFeedPostActionViewStyle](../Action/LMFeedPostActionHorizontalView.md))**                           | Applies the given style to the post action view.                                           |
| **setUpvoteText(upvoteText: [String](https://docs.likeminds.community/))**                                                 | Sets the text for the "Upvote" option.                                                    |
| **setUpvoteCount(upvoteCount: [String](https://docs.likeminds.community/))**                                               | Sets the count of upvotes.                                                                |
| **setCommentsCount(commentsCount: [String](https://docs.likeminds.community/))**                                           | Sets the count of comments.                                                                |
| **setUpvoteIcon(isUpvoted: [Boolean](https://docs.likeminds.community/) = false)**                                         | Configures the state of the "Upvote" icon.                                                |
| **setSaveIcon(isSaved: [Boolean](https://docs.likeminds.community/) = false)**                                             | Configures the state of the "Save" icon.                                                  |
| **setUpvoteIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the "Upvote" icon.                                         |
| **setUpvoteCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the upvote count.                                          |
| **setCommentsCountClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                    | Registers a click listener for the comments count.                                        |
| **setSaveIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                              | Registers a click listener for the "Save" icon.                                           |
| **setShareIconListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                             | Registers a click listener for the "Share" icon.                                          |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postactionview/view/LMFeedPostQnAActionHorizontalView.kt)




================================================
File: feed/Android/Core/Widgets/Post/Action/_category_.json
================================================
{
  "label": "Post Action",
  "position": 2,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Post Action Widgets in Chat"
  }
}



================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostDocumentView.md
================================================
---
sidebar_position: 2
title: Post Media Document 
slug: /android/core/widgets/post/media/post-media-document
---

# **Widget Documentation: LMFeedPostDocumentView**

## **Widget: LMFeedPostDocumentView**
The `LMFeedPostDocumentView` is a customizable view for displaying an individual document, supporting actions like styling, configuring attributes, and adding click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postDocumentMediaViewStyle: [LMFeedPostDocumentsMediaViewStyle](../Media/LMFeedPostDocumentsMediaView.md))**            | Applies the given style to the document view.                                              |
| **setDocumentName(documentName: [String](https://docs.likeminds.community/))**                                              | Sets the name of the document.                                                            |
| **setDocumentPages(documentPages: [Int](https://docs.likeminds.community/))**                                               | Sets the number of pages in the document.                                                 |
| **setDocumentSize(documentSize: [Long](https://docs.likeminds.community/))**                                                | Sets the size of the document.                                                            |
| **setDocumentType(documentType: [String](https://docs.likeminds.community/))**                                              | Sets the type of the document.                                                            |
| **setDocumentClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                          | Registers a click listener for the document.                                              |
| **setRemoveIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the remove icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostDocumentView.kt)




================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostDocumentsMediaView.md
================================================
---
sidebar_position: 1
title: Post Media Document List
slug: /android/core/widgets/post/media/post-media-document-list
---

# **Widget Documentation: LMFeedPostDocumentsMediaView**

## **Widget: LMFeedPostDocumentsMediaView**
The `LMFeedPostDocumentsMediaView` is a customizable view for displaying a list of document media, supporting actions like showing more documents, removing documents, and configuring styles.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postDocumentsMediaViewStyle: [LMFeedPostDocumentsMediaViewStyle](../Media/LMFeedPostDocumentsMediaView.md))**           | Applies the given style to the document media view.                                        |
| **configureShowMore(documentShowMoreStyle: [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md))**                          | Configures the text style for the "Show More" option.                                      |
| **setAdapter(parentPosition: [Int](https://docs.likeminds.community/), mediaData: [LMFeedMediaViewData](https://docs.likeminds.community/), listener: [LMFeedPostAdapterListener](https://docs.likeminds.community/), isMediaRemovable: [Boolean](https://docs.likeminds.community/) = false)** | Sets the adapter for displaying document media. |
| **removeDocument(position: [Int](https://docs.likeminds.community/))**                                                     | Removes a document from the view at the specified position.                                |
| **setShowMoreTextClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                      | Registers a click listener for the "Show More" text.                                       |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostDocumentsMediaView.kt)

## **View Style: LMFeedPostDocumentsMediaViewStyle**
The `LMFeedPostDocumentsMediaViewStyle` defines the appearance and layout properties for the `LMFeedPostDocumentsMediaView`, including text, icon, and visibility configurations.

| Field                   | Description                                      | Type              |
|-------------------------|--------------------------------------------------|-------------------|
| **documentNameStyle**   | Defines the text style for the document name.    | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **documentIconStyle**   | Configures the style for the document icon.      | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **documentPageCountStyle** | Defines the text style for the document page count. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **documentSizeStyle**   | Configures the text style for the document size. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **documentTypeStyle**   | Defines the text style for the document type.    | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **documentShowMoreStyle** | Configures the text style for the "Show More" option. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **visibleDocumentsLimit** | Specifies the limit for visible documents.    | [Int](https://docs.likeminds.community/)           |
| **removeIconStyle**     | Configures the style for the remove icon.        | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/style/LMFeedPostDocumentsMediaViewStyle.kt)



================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostImageMediaView.md
================================================
---
sidebar_position: 3
title: Post Media Image List 
slug: /android/core/widgets/post/media/post-media-image-list
---

# **Widget Documentation: LMFeedPostImageMediaView**

## **Widget: LMFeedPostImageMediaView**
The `LMFeedPostImageMediaView` is a customizable view for displaying an image, supporting actions like styling, setting the image source, and adding a remove icon with configurable click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(lmFeedPostImageMediaViewStyle: [LMFeedPostImageMediaViewStyle](../Media/LMFeedPostImageMediaView.md))**             | Applies the given style to the image media view.                                           |
| **setImage(imageSrc: [Any](https://docs.likeminds.community/), postImageMediaViewStyle: [LMFeedPostImageMediaViewStyle](../Media/LMFeedPostImageMediaView.md))** | Sets the image source and applies the style.                                              |
| **setRemoveIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the remove icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostImageMediaView.kt)

## **View Style: LMFeedPostImageMediaViewStyle**
The `LMFeedPostImageMediaViewStyle` defines the appearance and layout properties for the `LMFeedPostImageMediaView`, including configurations for the image and remove icon.

| Field                | Description                                      | Type              |
|----------------------|--------------------------------------------------|-------------------|
| **imageStyle**       | Configures the style for the image.              | [LMFeedImageStyle](../../Fundamentals/LMFeedImageView.md) |
| **removeIconStyle**  | Configures the style for the remove icon.         | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/style/LMFeedPostImageMediaViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostLinkMediaView.md
================================================
---
sidebar_position: 4
title: Post Media Link  
slug: /android/core/widgets/post/media/post-media-link
---

# **Widget Documentation: LMFeedPostLinkMediaView**

## **Widget: LMFeedPostLinkMediaView**
The `LMFeedPostLinkMediaView` is a customizable view for displaying a link preview, supporting actions like styling, setting link details, and adding click listeners for the link and its remove icon.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postLinkViewStyle: [LMFeedPostLinkMediaViewStyle](../Media/LMFeedPostLinkMediaView.md))**                          | Applies the given style to the link media view.                                            |
| **setLinkTitle(linkTitle: [String](https://docs.likeminds.community/))**                                                   | Sets the title of the link.                                                                |
| **setLinkDescription(linkDescription: [String](https://docs.likeminds.community/))**                                       | Sets the description of the link.                                                         |
| **setLinkUrl(linkUrl: [String](https://docs.likeminds.community/))**                                                       | Sets the URL of the link.                                                                  |
| **setLinkImage(imageSrc: [String](https://docs.likeminds.community/))**                                                    | Sets the image source for the link.                                                       |
| **setLinkClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                             | Registers a click listener for the link.                                                  |
| **setLinkRemoveClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                       | Registers a click listener for the remove icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostLinkMediaView.kt)

## **View Style: LMFeedPostLinkMediaViewStyle**
The `LMFeedPostLinkMediaViewStyle` defines the appearance and layout properties for the `LMFeedPostLinkMediaView`, including text, icon, and box configurations.

| Field                    | Description                                      | Type              |
|--------------------------|--------------------------------------------------|-------------------|
| **linkTitleStyle**       | Configures the text style for the link title.    | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **linkDescriptionStyle** | Configures the text style for the link description. | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **linkUrlStyle**         | Configures the text style for the link URL.      | [LMFeedTextStyle](../../Fundamentals/LMFeedTextView.md) |
| **linkImageStyle**       | Configures the style for the link image.         | [LMFeedImageStyle](../../Fundamentals/LMFeedImageView.md) |
| **linkRemoveIconStyle**  | Configures the style for the remove icon.        | [LMFeedIconStyle](../../Fundamentals/LMFeedIcon.md) |
| **linkBoxCornerRadius**  | Specifies the corner radius for the link box.    | [Int](https://docs.likeminds.community/)           |
| **linkBoxElevation**     | Specifies the elevation for the link box.        | [Int](https://docs.likeminds.community/)           |
| **linkBoxStrokeColor**   | Specifies the stroke color for the link box.     | [Int](https://docs.likeminds.community/)           |
| **linkBoxStrokeWidth**   | Specifies the stroke width for the link box.     | [Int](https://docs.likeminds.community/)           |
| **backgroundColor**      | Specifies the background color of the link box.  | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/style/LMFeedPostLinkMediaViewStyle.kt)



================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostMultipleMediaView.md
================================================
---
sidebar_position: 5
title: Post Multiple Media List 
slug: /android/core/widgets/post/media/post-multiple-media-list
---

# **Widget Documentation: LMFeedPostMultipleMediaView**

## **Widget: LMFeedPostMultipleMediaView**
The `LMFeedPostMultipleMediaView` is a customizable view for displaying multiple media items, such as images or videos, with support for indicators and media management.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postMultipleMediaStyle: [LMFeedPostMultipleMediaViewStyle](../Media/LMFeedPostMultipleMediaView.md))**                 | Applies the given style to the multiple media view.                                        |
| **setViewPager(mediaData: [List]([LMFeedMediaViewData](https://docs.likeminds.community/)), mediaClickListener: [LMFeedOnClickListener](https://docs.likeminds.community/))** | Sets up the view pager with media data and a click listener.                                |
| **removeMedia(position: [Int](https://docs.likeminds.community/))**                                                        | Removes media from the view at the specified position.                                     |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostMultipleMediaView.kt)

## **View Style: LMFeedPostMultipleMediaViewStyle**
The `LMFeedPostMultipleMediaViewStyle` defines the appearance and layout properties for the `LMFeedPostMultipleMediaView`, including configurations for indicators.

| Field                   | Description                                      | Type              |
|-------------------------|--------------------------------------------------|-------------------|
| **indicatorActiveColor**    | Specifies the active color for the indicator.   | [Int](https://docs.likeminds.community/)           |
| **indicatorInActiveColor**  | Specifies the inactive color for the indicator. | [Int](https://docs.likeminds.community/)           |
| **indicatorActiveWidth**    | Specifies the active width for the indicator.   | [Int](https://docs.likeminds.community/)           |
| **indicatorStyle**          | Specifies the style of the indicator.           | [Int](https://docs.likeminds.community/)           |
| **indicatorInactiveWidth**  | Specifies the inactive width for the indicator. | [Int](https://docs.likeminds.community/)           |
| **indicatorHeight**         | Specifies the height of the indicator.          | [Int](https://docs.likeminds.community/)           |
| **indicatorSpacing**        | Specifies the spacing between indicators.        | [Int](https://docs.likeminds.community/)           |
| **indicatorSlideMode**      | Specifies the slide mode for the indicators.     | [Int](https://docs.likeminds.community/)           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/style/LMFeedPostMultipleMediaViewStyle.kt)




================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostVerticalVideoMediaView.md
================================================
---
sidebar_position: 6
title: Post Media Vertical Video List 
slug: /android/core/widgets/post/media/post-media-vertical-video-list
---

# **Widget Documentation: LMFeedPostVerticalVideoMediaView**

## **Widget: LMFeedPostVerticalVideoMediaView**
The `LMFeedPostVerticalVideoMediaView` is a customizable view for displaying a vertical video, supporting actions like play/pause, mute/unmute, and removal with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postVideoMediaViewStyle: [LMFeedPostVideoMediaViewStyle](../../Fundamentals/LMFeedVideoView.md))**                   | Applies the given style to the video media view.                                           |
| **setPlayPauseIcon(isPlaying: [Boolean](https://docs.likeminds.community/) = false)**                                       | Configures the play/pause icon based on the playing state.                                 |
| **setMuteUnmuteIcon(isMute: [Boolean](https://docs.likeminds.community/) = false)**                                         | Configures the mute/unmute icon based on the mute state.                                   |
| **playVideo()**                                                                           | Initiates video playback.                                                                 |
| **setRemoveIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the remove icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostVerticalVideoMediaView.kt)





================================================
File: feed/Android/Core/Widgets/Post/Media/LMFeedPostVideoMediaView.md
================================================
---
sidebar_position: 6
title: Post Media Video List 
slug: /android/core/widgets/post/media/post-media-video-list
---

# **Widget Documentation: LMFeedPostVideoMediaView**

## **Widget: LMFeedPostVideoMediaView**
The `LMFeedPostVideoMediaView` is a customizable view for displaying a video, supporting actions like play/pause, mute/unmute, and removal with configurable styles and click listeners.

| Method                                                                                      | Description                                                                                 |
|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **setStyle(postVideoMediaViewStyle: [LMFeedPostVideoMediaViewStyle](../../Fundamentals/LMFeedVideoView.md))**                   | Applies the given style to the video media view.                                           |
| **setPlayPauseIcon(isPlaying: [Boolean](https://docs.likeminds.community/) = false)**                                       | Configures the play/pause icon based on the playing state.                                 |
| **setMuteUnmuteIcon(isMute: [Boolean](https://docs.likeminds.community/) = false)**                                         | Configures the mute/unmute icon based on the mute state.                                   |
| **playVideo()**                                                                           | Initiates video playback.                                                                 |
| **setRemoveIconClickListener(listener: [LMFeedOnClickListener](https://docs.likeminds.community/))**                        | Registers a click listener for the remove icon.                                           |

[View the code on GitHub](https://github.com/LikeMindsCommunity/likeminds-feed-android/tree/master/likeminds-feed-android-core/src/main/java/com/likeminds/feed/android/core/ui/widgets/post/postmedia/view/LMFeedPostVideoMediaView.kt)



================================================
File: feed/Android/Core/Widgets/Post/Media/_category_.json
================================================
{
  "label": "Post Media",
  "position": 3,
  "link": {
    "type": "generated-index",
    "description": "Documentation for Core Layer Post Media Widgets in Chat"
  }
}



---
