---
sidebar_position: 5
title: How to create topics and add child-topics in LikeMinds Feed?
slug: /react-native/core/guide/how-to-create-topics-and-add-child-topics-in-likeMinds-feed
---

## Creating Parent and Child topics.

This document will guide you to create topics in LikeMinds Feed SDK as well as adding **child-topics** to it. This sort of use-case comes handy where you want to serialize your posts and link them to make a relational order.

### Step 1 - Get Access Token for a Admin

1. Get the User Unique Id of the **Owner Bot** from the LikeMinds Admin Dashboard. Navigate to [Members section](https://dashboard.likeminds.community/community/members) and Get the Unique Id of the Owner Bot for further use. Save the the Unique ID for futures usages for calling APIs.
2. Now, you need to obtain the `accessToken` for Owner Bot. This token is necessary for authenticating API calls. Call the `POST sdk/initiate API` to login with **Owner Bot ID** credentials. You can fetch the user unique id and API key from the dashboard and add in the respective placeholder below.

```bash
curl --location 'https://auth.likeminds.community/sdk/initiate' \
--header 'x-api-key: {LIKEMINDS_API_KEY}' \
--header 'x-sdk-source: chat' \
--header 'x-api-version: 1' \
--header 'Content-Type: application/json' \
--data '{
    "uuid": "{UUID_OF_OWNER_BOT_FROM_DASHBOARD}",
}'
```

When you receive a `200 response` in the response body `data.access_token` will be used as `Authorization` token in the following APIs.

### Step 1 - Create a Parent Topic

You will have to create a regular topic which will serve as a parent to all the subsequent topics you will make. You can make a topic through a curl request.

```bash
curl --location 'https://auth.likeminds.community/feed/topic' \
--header 'Authorization: {{auth_token}}' \
--header 'x-platform-type: dashboard' \
--header 'Content-Type: application/json' \
--data '{
    "topics": [
        {
            "name": "Topic #1"
        },
        {
            "name": "Topic #2"
        },
        {
            "name": "Topic #3"
        }
    ]
}'
```

### Step 2 - Add Child Topics to Parent Topics

Now you will have to create child-topics for the above created parent topic. To do so copy the `_id` for the parent topic, you will put this in the `parent-topic-id` key of the subsequent topic object.

```bash
curl --location 'https://auth.likeminds.community/feed/topic' \
--header 'Authorization: {{auth_token}}' \
--header 'x-platform-type: dashboard' \
--header 'Content-Type: application/json' \
--data '{
    "topics": [
        {
            "name": "Child Topic #1"
            "parent_id":"{{topic_id of Topic #1}}"
        },
        {
            "name": "Child Topic #2"
            "parent_id":"{{topic_id of Topic #1}}"
        },
        {
            "name": "Child Topic #3"
            "parent_id":"{{topic_id of Topic #1}}"
        }
    ]
}'
```

## Fetching Topics using data layer

### Fetch Parent Topics

You can get the parent-topics, by using the function `getTopics()` of your `LMFeedClient` instance.

Below snippet explains how you can achieve this.

```ts
import { GetTopicsRequest } from "@likeminds.community/feed-js";

async function fetchTopics() {
  try {
    const response = await lmFeedclient?.getTopics(
      GetTopicsRequest.builder()
        .setPage(1)
        .setPageSize(10)
        .setIsEnabled(true)
        .build()
    );
    // parse the response as needed
  } catch {
    // parse the error as needed
  }
}
```

The above `response` will have all the parent topics present in LikeMinds Feed. For detailed information about `getTopics()`, click [here](../../Data/Topic/get-topics.md)

### Fetch Child Topics

You can get the child-topics for any parent-topic, Provided you have the `id` of the topic, by using the function `getTopics()` of your `LMFeedClient` instance.

:::info
You can get the `parent id` of any topic, inside the topic object itself.
:::

Below snippet explains how you can achieve this.

```ts
import { GetTopicsRequest } from "@likeminds.community/feed-js";

async function fetchTopics() {
  try {
    // List of your parent Ids
    const parentIdsList = ["ADD-TO-YOUR-LIST-OF-PARENT-IDS"];

    const getTopicsCall = await lmFeedclient?.getTopics(
      GetTopicsRequest.builder()
        .setPage(1)
        .setIsEnabled(true)
        .setPageSize(10)
        .setParentIds(parentIdsList)
        .build()
    );
    // parse the response as needed
  } catch {
    // parse the error as needed
  }
}
```

The above `response` will have all the parent topics present in LikeMinds Feed. For detailed information about `getTopics()`, click [here](../../Data/Topic/get-topics.md)

## How to get posts of child topic and parent topic in a single feed?

While rendering your feed, you can select specific topics and get feed only related to those topics. You can do so by passing the `id`s of desired topic in the `getFeed()` function of you `LMFeedClient` instance. Additionally, you can also select the desired topics along with it's parent-topic. Below snippet explains on how you can do so.

### Step 1: Create your custom Universal Feed component

```jsx
import React, { useEffect, useState } from 'react';
import { View } from "react-native";
import {
    LMFilterTopics,
    LMPostUploadIndicator,
    LMUniversalFeedHeader,
    PostsList,
    UniversalFeed,
    LMCreatePostButton,
    LMPostQnAFeedFooter
    usePostListContext,
    useUniversalFeedContext,
} from '@likeminds.community/feed-rn-core';
import { Client } from '@likeminds.community/feed-rn-core/client';

function CustomUniversalFeed() {
  return (
    <View style={{flex: 1, backgroundColor: 'black'}}>
      <UniversalFeed>
        <LMUniversalFeedHeader />
        <LMPostUploadIndicator />
        <PostsList />
        <LMCreatePostButton />
      </UniversalFeed>
    </View>
  );
}
```

### Step 2: Wrap the `<CustomUniversalFeed/>` with context providers

```jsx
import {
  UniversalFeedContextProvider,
  PostListContextProvider,
} from "@likeminds.community/feed-rn-core";
function CustomUniversalFeedScreen({ navigation, route }) {
  const [selectedTopics, setSelectedTopics] = useState([]);
  useEffect(() => {
    const childTopic = "YOUR-CHILD-TOPIC-ID";
    const parentTopic = `#$ONLY$#${"<PARENT_TOPIC_ID>"}`;
    const topicList = [childTopic, parentTopic];
    setSelectedTopics(topicList);
  }, []);
  return (
    <>
      {selectedTopics.length > 0 ? (
        <UniversalFeedContextProvider
          navigation={navigation}
          route={route}
          predefinedTopics={selectedTopics}
        >
          <PostListContextProvider navigation={navigation} route={route}>
            <Feed />
          </PostListContextProvider>
        </UniversalFeedContextProvider>
      ) : null}
    </>
  );
}
```

### Step 3: Integrating with the Stack Navigator

Once your `CustomUniversalFeedScreen` component is set up, you need to integrate it into your stack navigator to render this screen when required. Here’s an example of how to add the UniversalFeedScreen to your stack:

```jsx
import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import CustomUniversalFeedScreen from "<path_to_custom_universal_feed";
import { UNIVERSAL_FEED } from "@likeminds.community/feed-rn-core";

const Stack = createStackNavigator();

const StackScreen = () => {
  return (
    <Stack.Navigator>
      {/* Other screens */}
      <Stack.Screen
        name={UNIVERSAL_FEED}
        component={CustomUniversalFeedScreen} // Reference to your custom CreateScreen
      />
    </Stack.Navigator>
  );
};

export default StackScreen;
```

By adding the `CustomCreatePostScreen` to the `Stack.Screen` in the stack navigator, you can navigate to the custom `CREATE_POST` screen from anywhere in your app.
