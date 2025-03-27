---
sidebar_position: 6
title: Migration Guide Feed React Native SDK (v1.12.1 or below to v1.13.0)
slug: /react-native/core/migration-guide-feed-react-native-sdk-v1.12.1-or-below--to-v1.13.0
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Migration Guide: Feed React Native SDK (v1.12.1 or below to v1.13.0)

This guide provides an overview of the key changes in **v1.13.0** of the LikeMinds Feed React Native SDK and instructions for updating your project from **v1.12.1 or below**.

---

## Key Updates in v1.13.0

1. Introduced a new Stack Screen for [post search](./Screens/LMFeedSearchScreen.md) functionality.

2. Integrated new dependencies for a circular progress indicator to visually track attachment uploads during post creation.

---

### Migration Steps

#### Step 1: Upgrade the LikeMinds Feed packages in package.json to the below versions

```json
"@likeminds.community/feed-rn": "1.5.0",
"@likeminds.community/feed-rn-core": "1.13.0"
```

#### Step 2: Install the new dependencies given below

```
npm install react-native-svg react-native-circular-progress
```

### Step 3: Add the new Search Screen in the Stack Navigator

<Tabs>
<TabItem value="SocialFeed" label="Social Feed">

```tsx
import { LMSocialFeedSearchScreenWrapper } from "@likeminds.community/feed-rn-core";
import { SEARCH_SCREEN } from "@likeminds.community/feed-rn-core/constants/screenNames";

<NavigationContainer>
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    {/* add this below other screen */}
    <Stack.Screen
      name={SEARCH_SCREEN}
      component={LMQnaFeedSearchScreenWrapper}
    />
  </Stack.Navigator>
</NavigationContainer>

```

</TabItem>
<TabItem value="QnA Feed" label="QnA Feed">

```tsx
import { LMQnaFeedSearchScreenWrapper } from "@likeminds.community/feed-rn-core";
import { SEARCH_SCREEN } from "@likeminds.community/feed-rn-core/constants/screenNames";

<NavigationContainer>
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    {/* add this below other screen */}
    <Stack.Screen
      name={SEARCH_SCREEN}
      component={LMQnaFeedSearchScreenWrapper}
    />
  </Stack.Navigator>
</NavigationContainer>
```

</TabItem>
</Tabs>


---

By following these steps, you can migrate seamlessly to **v1.13.0** and take advantage newly introduced features and customizations.
