---
sidebar_position: 7
title: Carousel screen
slug: /react-native/core/screens/carousel-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `CarouselScreen` component is designed to display a carousel of images or media within a screen format, allowing users to swipe through a set of media items. It supports various media types like images and videos and includes pagination controls for easy navigation. The component is customizable, enabling developers to style and configure media elements to fit the overall UI. Commonly used in posts or feeds, it provides an interactive and visually engaging way for users to view multiple media items.

<Tabs>
<TabItem value="ImageCarouselScreen" label="ImageCarouselScreen">

<img
src={require('../../../../static/img/reactNative/mediaLMCarouselImage.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

</TabItem>
<TabItem value="VideoCarouselScreen" label="VideoCarouselScreen">

<img
src={require('../../../../static/img/reactNative/mediaLMCarouselVideoPlayer.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

</TabItem>
</Tabs>

## UI Components

- [LMFeedCarouselVideoPlayer](../Components/Media/LMFeedCarouselVideoPlayer.md)
- [LMFeedImage](../Components/Media/LMFeedImage.md)
- [LMFeedText](../Components/Fundamentals/LMFeedText.md)

## Data Variables

- `attachments`: Stores the attachment data conforming to [`LMAttachmentViewData[]`](../Models/LMAttachmentViewData.md).

## Callbacks

- `onBackPressOnCarouselScreen`: Its trigerred on pressing of the back button in carousel screen.

## Customisation

The `STYLES` class allows you to customize the appearance of the `LMPostContent`. You can set the styles in [`carouselScreenStyle`](../Components/Media/LMFeedCarouselVideoPlayer.md#customisation) in `STYLES`.

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `CarouselScreen` as a Stack screen in your `NavigationContainer`.
- Create `carouselScreenStyle` for customisation and call the `setCarouselScreenStyles` to set the customisation.
- Create a `CustomCallbacks` implementing `LMCarouselScreenCallbacks`, and override the `onBackPressOnCarouselScreen` with custom logic.

### App.tsx

```ts
import {
  CAROUSEL_SCREEN,
  CarouselScreen,
  LMOverlayProvider,
  STYLES,
  LMCarouselScreenCallbacks,
} from "@likeminds.community/feed-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

// custom callback class implementing carouselCallBackClass
class CustomCallbacks implements LMCarouselScreenCallbacks {
  onBackPressOnCarouselScreen() {
    // override onBackPressOnCarouselScreen with custom logic
    navigationRef.goBack();
  }
}

const lmFeedInterface = new CustomCallbacks();

export const App = () => {
  const Stack = createNativeStackNavigator();
  const carouselScreenStyle = {
    headerTitle: {
      color: "green",
    },
    headerSubtitle: {
      color: "purple",
    },
    thumbTintColor: "pink",
    minimumTrackTintColor: "red",
    maximumTrackTintColor: "blue",
    muteIconPath: "https://lm.jpg",
    isMuteIconLocalPath: false,
    muteIconStyle: {
      tintColor: null,
    },
    unmuteIconStyle: {
      tintColor: "red",
    },
  };

  // carousel screen customisation
  if (carouselScreenStyle) {
    STYLES.setCarouselScreenStyles(carouselScreenStyle);
  }

  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      lmFeedInterface={lmFeedInterface} // pass the callback interface object
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={CAROUSEL_SCREEN}
            component={CarouselScreen}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
