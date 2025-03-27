---
sidebar_position: 2
title: Community Configurations
slug: /react-native/data/helper/community-configurations
---

The `getMemberState` function is used to fetch the member state of the current user. It provides information about the user's status, creation timestamp, edit requirements, and more.

## Steps to Get Community Configurations

1. Use the `getCommunityConfigurations()` function provided by the `lmFeedClient` object created earlier.
2. Use the response as per your requirement

```js
try {
  const response = await lmFeedClient.getCommunityConfigurations();
  // Use the response as per your requirement.
} catch (error) {
  // Use the error as per your requirement.
}
```

## Models

### GetCommunityConfigurationsResponse

| **VARIABLE**              | **TYPE**                                                                  | **DESCRIPTION**          | **OPTIONAL** |
| :------------------------ | :------------------------------------------------------------------------ | :----------------------- | :----------: |
| `communityConfigurations` | [Configuration](../Helper/get-community-configurations.md/#configuration) | Community Configurations |              |

### Configuration

| **VARIABLE**  | **TYPE**                                                                          | **DESCRIPTION**                   | **OPTIONAL** |
| :------------ | :-------------------------------------------------------------------------------- | :-------------------------------- | :----------: |
| `description` | string                                                                            | Description of the configurations |              |
| `type`        | [ConfigurationType](../Helper/get-community-configurations.md/#configurationtype) | Type of the configurations        |              |
| `value`       | [JSONObject](../Helper/get-community-configurations.md/#jsonobject)               | Value of the configurations       |              |

### ConfigurationType

```js
enum ManagerRightState {
    MEDIA_LIMITS = "media_limits",
    FEED_METADATA = "feed_metadata",
    PROFILE_METADATA = "profile_metadata",
    NSFW_FILTERING = "nsfw_filtering",
    WIDGETS_METADATA = "widgets_metadata",
    GUEST_FLOW_METADATA = "guest_flow_metadata",
}
```

### JSONObject

```js
interface JSONObject {
  [key: string]: any;
}
```
