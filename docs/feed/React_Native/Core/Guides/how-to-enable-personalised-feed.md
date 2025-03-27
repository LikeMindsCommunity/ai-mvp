---
sidebar_position: 10
title: How to enable personalised feed?
slug: /react-native/core/guide/how-to-enable-personalised-feed
---

# How to enable personalised feed?

## Introduction

In this guide, you'll learn how to enable and configure a personalized feed for users in your React Native app using the LikeMinds Feed React Native SDK. A personalized feed helps enhance user engagement by tailoring the content they see based on their preferences, interactions, and other metrics.

## Prerequisites

Before you begin, ensure the following:

- **LikeMinds Chat React Native SDK**: The SDK must be properly installed and initialized in your React Native project. Refer to the [installation guide](https://docs.likeminds.community/chat/react-native/getting-started) if needed.
- **Basic Understanding of React Native Components**: Familiarity with React Native components concepts.
- Basic knowledge of Postman or equivalent API testing tools.

## Steps

### Step 1: Initiate a user session

Authenticated API calls to the LikeMinds backend require an authorization token. This token can be generated using this [Getting Started doc](https://docs.likeminds.community/rest-api/authentication#getting-started). Make sure to log in with the Community Manager's credentials.

### Step 2: Enable personalised feed

To enable the personalized feed, go to your [likeminds dashboard](https://dashboard.likeminds.community/home) and enable personalized feed from feed settings.

### Step 3: Set weigths for different metrics

The personalized feed relies on various metrics such as likes, comments, recency, and user interactions. Set the weights for these metrics using the following cURL request:

```bash
curl --location --request PATCH 'https://auth.likeminds.community/community/configurations' \
--header 'Content-Type: application/json' \
--header 'Authorization: {cm_access_token}' \
--data '{
    "description": "Personalised feed weights metadata for the community",
    "type": "personalised_feed_weights",
    "value": {
        "comments_metrics": {
            "max_threshold": 200,
            "weight": 10
        },
        "likes_metrics": {
            "max_threshold": 100,
            "weight": 5
        },
        "post_dampening_metrics": {
            "max_threshold": 100,
            "weight": 5
        },
        "recency_metrics": {
            "max_threshold": 100,
            "weight": 5
        },
        "user_groups_metrics": {
            "max_threshold": 50,
            "weight": 2
        },
        "user_topics_metrics": {
            "max_threshold": 100,
            "weight": 5
        },
        "user_connection_metrics": {
            "max_threshold": 100,
            "weight": 5
        }
    }
}'
```

:::note
The sample values in the cURL are subjective in nature, please change it as per your user group.
:::

### Step 4: Initiate React Native Feed SDK and Navigate to Personalised Feed Screen

1. Follow the [Getting Started doc](../../getting-started.md) to initialize React Native Feed SDK.
2. To navigate to the personalized feed screen, use the `UniversalFeed` screen with `LMSocialFeedScreen` component with the feedType set to `LMFeedType.PERSONALISED_FEED`.

```tsx
<Stack.Screen
  name={"UniversalFeed"}
  component={LMSocialFeedScreen}
  initialParams={{
    feedType: FeedType.PERSONALISED_FEED,
  }}
/>
```
