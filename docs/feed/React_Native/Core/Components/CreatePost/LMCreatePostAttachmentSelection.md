---
sidebar_position: 2
title: Create Post Attachment Selection
slug: /react-native/core/components/universal-feed/create-post-attachment-selection
---

# LMCreatePostAttachmentSelection

The `LMCreatePostAttachmentSelection` component provides users with multiple options for adding attachments (photos, videos, files, and polls) to a new post. This component is highly customizable and integrates with `CreatePostContext` for managing various post creation options.

<img
src={require('../../../../../static/img/reactNative/createPostAttachmentSelection.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostAttachmentSelection` includes:

- Configurable buttons for adding images, videos, files, and polls.
- Dynamic styling and customization through context.
- Integration with analytics to track attachment selection events.

## Callbacks

The component supports callback through context values, which are configured within the `CreatePost` component.

| Property             | Type       | Description                                                      |
| -------------------- | ---------- | ---------------------------------------------------------------- |
| `handleDocumentProp` | `function` | Optional custom callback for handling document attachments.      |
| `handlePollProp`     | `function` | Optional custom callback for handling poll creation.             |
| `handleGalleryProp`  | `function` | Optional custom callback for handling image and video selection. |

## Customization with Styles

The component supports customization through context styles, which are configured within the `CreatePost` component.

| Property                 | Type                                                                                                                                                  | Description                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `attachmentOptionsStyle` | [`object`](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L311) | Styles for customizing the layout and appearance of the attachment options container. |
## Example Usage

To use this component, make sure it's placed within a provider that supplies `CreatePostContext` and `CreatePostCustomisableMethodsContext`. Here’s an example of integrating `LMCreatePostAttachmentSelection` in a `CreatePost` screen:

```javascript
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  LMCreatePostAttachmentSelection,
  CreatePostProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {
  // to customise ui
  useEffect(() => {
    STYLES.setCreatePostStyles({
      attachmentOptionsStyle: {
        photoAttachmentView: {
          borderRadius: 10,
        },
      },
    });
  }, []);
  return (
    <View style={{ flex: 1 }}>
      {/* Other create post components */}
      <LMCreatePostAttachmentSelection />
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)