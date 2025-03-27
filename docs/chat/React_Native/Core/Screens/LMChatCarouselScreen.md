---
sidebar_position: 6
title: Carousel Screen
slug: /react-native/core/screens/carousel-screen
---

## Overview

The `CarouselScreen` component is designed to display a carousel of images or media within a screen format, allowing users to swipe through a set of media items. It supports various media types like images and videos and includes pagination controls for easy navigation. The component is customizable, enabling developers to style and configure media elements to fit the overall UI. Commonly used in posts or feeds, it provides an interactive and visually engaging way for users to view multiple media items.

<img
src={require('../../../../static/img/reactNative/lmCarouselScreen.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Data Variables

- `attachments`: An array of media items (e.g., images or videos) that are displayed in the carousel.
- `member`: Contains details about the user or member associated with the displayed content, such as name or profile image.
- `timestamp`: Represents the date and time when the attachment was shared, used to display the upload time of the media.

## Customisation

| Property         | Type                                | Description                                     |
| ---------------- | ----------------------------------- | ----------------------------------------------- |
| `headerTitle`    | [`HeaderTitle`](#headertitle)       | Styles for the header title of the carousel.    |
| `headerSubtitle` | [`HeaderSubtitle`](#headersubtitle) | Styles for the header subtitle of the carousel. |

### HeaderTitle

| Property     | Type     | Description                               |
| ------------ | -------- | ----------------------------------------- |
| `color`      | `string` | The text color of the header title.       |
| `fontSize`   | `number` | The font size of the header title.        |
| `fontFamily` | `string` | The font family of the header title text. |

### HeaderSubtitle

| Property     | Type     | Description                                  |
| ------------ | -------- | -------------------------------------------- |
| `color`      | `string` | The text color of the header subtitle.       |
| `fontSize`   | `number` | The font size of the header subtitle.        |
| `fontFamily` | `string` | The font family of the header subtitle text. |

## Props

| Property       | Type     | Description                                    |
| -------------- | -------- | ---------------------------------------------- |
| `backIconPath` | `string` | The path to the back icon shown on the header. |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `CarouselScreen` as a Stack screen in your `NavigationContainer`.
- Create `carouselScreenStyle` for customisation and call the `setCarouselScreenStyles` to set the customisation.

```tsx title="App.tsx"
import {
  CAROUSEL_SCREEN,
  CarouselScreen,
  STYLES,
  Themes
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  const carouselScreenStyles = {
    headerTitle: {
      color: "red",
    },
    headerSubtitle: {
      color: "blue",
    },
  };

  if (carouselScreenStyles) {
    STYLES.setCarouselScreenStyle(carouselScreenStyles);
  }

  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">} // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ gestureEnabled: false }}
            name={CAROUSEL_SCREEN}
            component={CarouselScreen}
            initialParams={{
              backIconPath: "", // add your back icon path here
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
