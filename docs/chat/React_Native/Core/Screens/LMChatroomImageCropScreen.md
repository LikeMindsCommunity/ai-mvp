---
sidebar_position: 7
title: Image Crop Screen
slug: /react-native/core/screens/image-crop-screen
---

## Overview

The `ImageCrop` screen enables users to crop images within the LikeMinds chat application. It provides an intuitive interface for selecting and adjusting the crop area of an image, allowing users to focus on specific details before uploading or sharing. This screen enhances the user experience by ensuring that images are presented in the desired format and aspect ratio.

<img
src={require('../../../../static/img/reactNative/lmImageCrop.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Component

- [FileUpload](./LMChatroomFileUploadScreen.md)

## Data Variables

- `image`: Image data to be cropped.

## Props

| Property   | Type     | Description                                      | Required           |
| ---------- | -------- | ------------------------------------------------ | ------------------ |
| `uri`      | `string` | The URI of the image to be cropped.              | :heavy_check_mark: |
| `fileName` | `string` | The name of the file to be saved after cropping. | :heavy_check_mark: |

## Usage Example

- In your `App.tsx`, create a `Stack.Navigator`in the `NavigationContainer` wrapped by`LMOverlayProvider`.
- Add `ImageCropScreen` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import {
  IMAGE_CROP_SCREEN,
  ImageCropScreen,
  Themes
} from "@likeminds.community/chat-rn-core";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMChatClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">} // // pass the sdk theme based on the Themes enum
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            options={{ headerShown: false }}
            name={IMAGE_CROP_SCREEN}
            component={ImageCropScreen}
            initialParams={{
              uri: "",
              fileName: "",
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
