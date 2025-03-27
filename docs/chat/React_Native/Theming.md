---
sidebar_position: 3
title: Theming
slug: /react-native/theming
---

## Overview of Styling and Theming in LikeMinds SDK

The `STYLES` class provides extensive customization capabilities for the LikeMinds Chat SDK, allowing developers to define and maintain a consistent design language across their application. By configuring its properties, you can set colors, fonts, spacing, and styles for various components and screens.

### Default Styles and Customization Options

**Key Properties of `STYLES`:**

```tsx
class STYLES {
  static $COLORS: {
    PRIMARY: string;
    SECONDARY: string;
    FONT_PRIMARY: string;
  };

  static $FONT_SIZES: {
    XS: number;
    SMALL: number;
    REGULAR: number;
    MEDIUM: number;
    LARGE: number;
    XL: number;
    XXL: number;
  };

  static $FONT_WEIGHTS: {
    LIGHT: string;
    MEDIUM: string;
    BOLD: string;
  };

  static $FONT_TYPES: {
    LIGHT: string;
    MEDIUM: string;
    SEMI_BOLD: string;
    BOLD: string;
    BLACK: string;
  };

  static $BACKGROUND_COLORS: {
    LIGHT: string;
    DARK: string;
  };

  static $SHADOWS: {
    LIGHT: string;
    MEDIUM: string;
    HEAVY: string;
  };

  static $MARGINS: {
    XS: number;
    SMALL: number;
    MEDIUM: number;
    LARGE: number;
  };

  static $PADDINGS: {
    SMALL: number;
    MEDIUM: number;
    LARGE: number;
  };

  static $AVATAR: {
    WIDTH: number;
    HEIGHT: number;
    BORDER_RADIUS: number;
  };

  static $ALIGN_ROW: {
    display: string;
    flexDirection: string;
    alignItems: string;
  };

  static $TEXTVIEW_WIDTH: {
    REGULAR: number;
  };

  static $STATUS_BAR_STYLE: {
    default: string;
    "dark-content": string;
    "light-content": string;
  };

  // Various screen-specific styles
  static $CHAT_BUBBLE_STYLE: ChatBubbleStyles;
  static $INPUT_BOX_STYLE: InputBoxStyles;
  static $REACTION_LIST_STYLE: ReactionListStyles;
  static $CHATROOM_HEADER_STYLE: ChatroomHeaderStyles;
  static $CHATROOM_TOPIC_STYLE: ChatroomTopicStyles;
  static $FILE_UPLOAD_STYLE: FileUploadStyles;
  static $MEMBER_DIRECTORY_STYLE: MemberDirectoryStyles;
  static $CAROUSEL_SCREEN_STYLE: CarouselScreenStyles;
  static $EXPLORE_CHATROOM_STYLE: ExploreChatroomStyles;
  static $HOME_FEED_STYLE: HomeFeedStyles;
  static $SEARCH_IN_CHATROOM: SearchInChatroomStyles;
  static $CHATBOT_INIT_SCREEN_STYLE: ChatBotInitiateScreenStyles;
  static $LMCHAT_AI_BUTTON_STYLE: LMChatAIButtonStyle;
}
```

### Theme Configuration

You can dynamically configure themes using the `setTheme` method, which allows you to update colors, font types, and background styles. Below is an example:

```tsx
import { STYLES } from "@likeminds.community/chat-rn-core";

const App = () => {
  useEffect(() => {
    // Set theme colors and fonts
    STYLES.setTheme({
      hue: 220,
      fontColor: "#333",
      primaryColor: "#0055FF",
      secondaryColor: "#FFAA00",
      lightBackgroundColor: "#FFFFFF",
      fontTypes: {
        LIGHT: "Roboto-Light",
        MEDIUM: "Roboto-Medium",
        SEMI_BOLD: "Roboto-SemiBold",
        BOLD: "Roboto-Bold",
        BLACK: "Roboto-Black",
      },
    });
  }, []);

  return <>{/* Your application code here */}</>;
};
```

### Screen-Specific Style Configuration

You can customize individual components or screens by using the provided setter methods. Each setter method accepts a style object to override default styles.

#### Example: Customizing Chat Bubble Styles

```tsx
STYLES.setChatBubbleStyle({
  bubbleColor: "#0055FF",
  textColor: "#FFFFFF",
  borderRadius: 12,
});
```

#### Example: Customizing Input Box Styles

```tsx
STYLES.setInputBoxStyle({
  borderColor: "#AAAAAA",
  placeholderTextColor: "#888888",
  backgroundColor: "#FFFFFF",
  fontSize: 14,
});
```

### Available Setter Methods

- `setChatBubbleStyle(chatBubbleStyles: ChatBubbleStyles)`
- `setInputBoxStyle(inputBoxStyles: InputBoxStyles)`
- `setReactionListStyle(reactionListStyles: ReactionListStyles)`
- `setChatroomHeaderStyle(chatroomHeaderStyles: ChatroomHeaderStyles)`
- `setChatroomTopicStyle(chatroomTopicStyles: ChatroomTopicStyles)`
- `setFileUploadStyle(fileUploadStyles: FileUploadStyles)`
- `setMemberDirectoryStyle(memberDirectoryStyles: MemberDirectoryStyles)`
- `setCarouselScreenStyle(carouselScreenStyles: CarouselScreenStyles)`
- `setExploreChatroomStyle(exploreChatroomStyles: ExploreChatroomStyles)`
- `setHomeFeedStyle(homeFeedStyles: HomeFeedStyles)`
- `setSearchInChatroomStyle(searchInChatroomStyles: SearchInChatroomStyles)`
- `setChatbotInitScreenStyle(chatBotInitiateScreenStyles: ChatBotInitiateScreenStyles)`
- `setLMChatAIButtonStyle(lmChatAIButtonStyle: LMChatAIButtonStyle)`

### Applying Custom Styles Across Components

By leveraging the flexibility of `STYLES`, you can create a cohesive and branded experience for your application. Experiment with different configurations to achieve the desired look and feel.
