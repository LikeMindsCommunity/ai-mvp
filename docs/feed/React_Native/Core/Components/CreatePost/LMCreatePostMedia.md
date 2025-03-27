---
sidebar_position: 4
title: Create Post Media
slug: /react-native/core/components/universal-feed/create-post-media
---

# LMCreatePostMedia

The `LMCreatePostMedia` component handles the media section of the post creation screen. It allows users to attach various media types (images, videos, documents, polls, and links) to their posts and provides functionality for previewing, managing, and removing attachments.

<img
src={require('../../../../../static/img/reactNative/createPostMedia.webp').default}
alt="LMFeedPostContent"
style={{border: '2px solid #d6d6d6', padding: '8px'}}
width="50%"
/>

## Overview

`LMCreatePostMedia` provides the following functionality:

- Displays previews of attached media (images, videos, polls, and documents).
- Allows users to add more attachments to their post.
- Supports conditional rendering based on the attachment types.
- Provides cancel functionality for each attachment type.

## Callbacks & Props

The component supports callback through context values, which are configured within the `CreatePost` component. It supports the following customizable properties:

| Property                       | Type       | Description                                              |
| ------------------------------ | ---------- | -------------------------------------------------------- |
| `postToEdit`                   | `boolean`  | Indicates whether the post is in edit mode.              |
| `handleDocument`               | `function` | Method to handle document attachment.                    |
| `handleGallery`                | `function` | Method to handle gallery attachment (images, videos).    |
| `allAttachment`                | `array`    | List of all media attachments.                           |
| `formattedMediaAttachments`    | `array`    | List of formatted media attachments (images, videos).    |
| `formattedPollAttachments`     | `array`    | List of formatted poll attachments.                      |
| `formattedDocumentAttachments` | `array`    | List of formatted document attachments.                  |
| `formattedLinkAttachments`     | `array`    | List of formatted link attachments.                      |
| `removeMediaAttachment`        | `function` | Function to remove media attachments.                    |
| `removePollAttachment`         | `function` | Function to remove poll attachments.                     |
| `removeDocumentAttachment`     | `function` | Function to remove document attachments.                 |
| `removeSingleAttachment`       | `function` | Function to remove a single attachment.                  |
| `showLinkPreview`              | `boolean`  | Flag to control the display of the link preview section. |
| `setShowLinkPreview`           | `function` | Function to set the link preview state.                  |

## Customisations with Styles

| Property                   | Type                                                                                                                                                  | Description                                          |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `addMoreAttachmentsButton` | [`object`](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L332) | Custom styles for the "Add More Attachments" button. |
| `media`     | [`object`](https://github.com/LikeMindsCommunity/likeminds-feed-reactnative/blob/main/likeminds-feed-reactnative-integration/lmFeedProvider/types.ts#L131) | Custom styles for the media section of the post.     |

## Example Usage

To use this component, make sure to wrap it within a `CreatePostProvider`. Here’s an example:

```javascript
import React, { useEffect } from "react";
import { View } from "react-native";
import {
  LMCreatePostMedia,
  CreatePostProvider,
  STYLES,
} from "@likeminds.community/feed-rn-core";

const CreatePostScreen = () => {

  // to customise ui
  useEffect(() => {
    STYLES.setPostListStyles({
      media: {
        image: {
          height: 10,
          width: 10,
        },
      },
    });
  }, []);
  return (
    <View style={{ flex: 1 }}>
      <LMCreatePostMedia />
      {/* Additional CreatePost components */}
    </View>
  );
};

export default CreatePostScreen;
```

- Use the `CreatePostScreen` component with [all other create post components](../../Screens/LMFeedCreatePostScreen.md#ui-components) as a child of the `CreatePost` component in the relevant screens:
  - [Create Post Screen](../../Screens/LMFeedCreatePostScreen.md)
