---
sidebar_position: 5
title: Create Post Text Input
slug: /react-native/core/components/universal-feed/create-post-text-input
---

# LMCreatePostTextInput

The `LMCreatePostTextInput` component renders a customizable text input field where users can enter the content of their posts.

It also utilizes the `LMInputText` component for input rendering and allows for custom styling of the input field. The placeholder text, input style, and other settings are configurable based on the current theme and the provided `STYLES`.

<img
src={require('../../../../../static/img/reactNative/createPostTextInput.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

---

## Customisations with Styles

| Prop                   | Type      | Description                                                             |
| ---------------------- | --------- | ----------------------------------------------------------------------- |
| `placeholderText`      | string    | Custom placeholder text for the input field.                            |
| `placeholderTextColor` | string    | The color of the placeholder text.                                      |
| `inputTextStyle`       | ViewStyle | Custom styles for the input text.                                       |
| `multilineField`       | boolean   | If `true`, the input field supports multiple lines. Defaults to `true`. |
| `textValueStyle`       | TextStyle | Styles for the input text value.                                        |

To see all the properties, visit [CreatePostStyleProps.createPostTextInputStyle](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L323)

---

## Usage Example

```jsx
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  STYLES,
  LMCreatePostTextInput,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setCreatePostStyles({
      createPostTextInputStyle: {
        placeholderText: "Create a post",
        placeholderTextColor: "pink",
      },
    });
  }, []);
  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostTextInput />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
