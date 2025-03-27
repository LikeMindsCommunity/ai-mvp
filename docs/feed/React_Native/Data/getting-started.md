---
sidebar_position: 1
title: Getting Started
slug: /react-native/data/getting-started
---

# Getting Started

The LikeMinds ReactNative Feed SDK empowers you to integrate personalized and engaging feeds into your ReactNative application, enhancing user experiences and driving user engagement. This guide will walk you through the steps to get started with the LikeMinds ReactNative Feed SDK and set up a dynamic feed in your application. Obtain the necessary API key from the [LikeMinds dashboard](https://dashboard.likeminds.community).

## Step-by-step guide

### 1. Add Dependency

Add `@likeminds.community/feed-rn` as a dependency in your `package.json` file by running this command in the terminal.

```bash
npm i @likeminds.community/feed-rn
```

### 2. Initiate LikeMinds Feed SDK

To initiate LikeMinds SDK in your app, create an instance of `LMFeedClient` class as shown in the snippet below.

```js
const lmFeedClient = LMFeedClient.builder().build();
```

:::tip
Maintain this instance of the `LMFeedClient` class throughout your application. You can use it to access the different methods exposed from the package.
:::
