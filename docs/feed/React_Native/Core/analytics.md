---
sidebar_position: 5
title: Analytics
slug: /react-native/core/analytics
---

# Analytics

The SDK has in built analytics events that are trigged for the events listed in the Analytics Events page. You can track those using tools like [Segment](https://segment.com/), [Mixpanel](https://mixpanel.com/), [Clevertap](https://clevertap.com/) etc.

## Analytics Callback

We've implemented an analytics callback method within the `LMFeedCallbacks` interface. This method, characterized by parameters eventName and eventProperties, is designed to accommodate custom logic by allowing developers to override it as needed.

```tsx
export interface LMFeedCallbacks {
  onEventTriggered(
    eventName: string,
    eventProperties?: Map<string, string>
  ): void;
}
```
- `eventName`: This parameter is of type `string` representing the name of the event that has been triggered. It helps identify which specific event has occurred.
- `eventProperties`: A map containing key-value pairs with additional information or metadata related to the tracked event.

### Code snippet

```tsx
import { LMFeedCallbacks } from "@likeminds.community/feed-rn-core";

class CustomCallbacks implements LMFeedCallbacks {
  onEventTriggered(eventName: string, eventProperties?: Map<string, string>) {
    // Override onEventTriggered with custom logic
  }
}

const lmFeedInterface = new CustomCallbacks();

function App():: React.JSX.Element  {
  return (
    <LMOverlayProvider
        myClient={lmFeedClient}
        accessToken={accessToken}
        refreshToken={refreshToken}
        apiKey={apiKey}
        userName={userName}
        userUniqueId={userUniqueID}
        callbackClass={callbackClass}
        lmFeedInterface={lmFeedInterface} // add this line in LMOverlayProvider props
    >
      {/* Add navigation container */}
    </LMOverlayProvider>
  );
};
```
