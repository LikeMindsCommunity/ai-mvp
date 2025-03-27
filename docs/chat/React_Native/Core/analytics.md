---
sidebar_position: 4
title: Analytics
---

# Analytics

The SDK has in built analytics events that are trigged for the events listed in the Analytics Events page. You can track those using tools like [Segment](https://segment.com/), [Mixpanel](https://mixpanel.com/), [Clevertap](https://clevertap.com/) etc.

## Analytics Callback

We've implemented an analytics callback method within the `LMChatCallbacks` interface. This method, characterized by parameters eventName and eventProperties, is designed to accommodate custom logic by allowing developers to override it as needed.

```tsx
export interface LMChatCallbacks {
  onEventTriggered(
    eventName: string,
    eventProperties?: Map<string, string>
  ): void;
}
```

### Code snippet

```tsx
import { LMChatCallbacks } from "@likeminds.community/chat-rn-core";

class CustomCallbacks implements LMChatCallbacks {
  onEventTriggered(eventName: string, eventProperties?: Map<string, string>) {
    // Override onEventTriggered with custom logic
  }
}

const lmChatInterface = new CustomCallbacks();

function App():: React.JSX.Element  {
  return (
    <LMOverlayProvider
      lmChatClient={lmChatClient}
      userName={userName}
      userUniqueId={userUniqueId}
      profileImageUrl={profileImageUrl}
      lmChatInterface={lmChatInterface} // add this line in LMOverlayProvider props
    >
      {/* Add navigation container */}
    </LMOverlayProvider>
  );
};
```
