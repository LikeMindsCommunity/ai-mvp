---
sidebar_position: 2
title: Theming
slug: /react-native/theming
---

## Detailed Overview of Theme Styles

The `LMFeedTheme` class allows you to customize various aspects of the LikeMinds Feed SDK's UI. By defining properties in the `LMFeedTheme` class, you can control the appearance of all UI widgets to ensure a consistent theme throughout your application.

**Types for `LMFeedTheme`:**

```tsx
class LMFeedTheme {
  public $IS_DARK_THEME: boolean;
  public $HUE: number;
  public $COLORS: {
    PRIMARY: string;
    SECONDARY: string;
    FONT_PRIMARY: string;
  };
  public $FONT_TYPES: {
    LIGHT?: string;
    MEDIUM?: string;
    SEMI_BOLD?: string;
    BOLD?: string;
    BLACK?: string;
  };
  public $BACKGROUND_COLORS: {
    LIGHT?: string;
    DARK?: string;
    DARK_TRANSPARENT?: string;
  };
  public $TEXT_COLOR: {
    PRIMARY_TEXT_LIGHT?: string;
    SECONDARY_TEXT_LIGHT?: string;
    PRIMARY_TEXT_DARK?: string;
    SECONDARY_TEXT_DARK?: string;
  };
  public $LMLoaderSizeiOS: number;
  public $LMLoaderSizeAndroid: number;

  public $POLL_STYLE: PollStyle;
  public $UNIVERSAL_FEED_STYLE: UniversalFeedStyleProps;
  public $POST_LIST_STYLE: PostListStyleProps;
  public $LOADER_STYLE: LoaderStyleProps;
  public $POST_DETAIL_STYLE: PostDetailStyleProps;
  public $CREATE_POST_STYLE: CreatePostStyleProps;
  public $POST_LIKES_LIST_STYLE: PostLikesListStyleProps;
  public $NOTIFICATION_FEED_STYLE: NotificationFeedStyleProps;
  public $TOPICS_STYLE: TopicsStyle;
  public $CAROUSEL_SCREEN_STYLE: CarouselScreenStyle;
  public $CREATE_POLL_STYLE: CreatePollStyle;
  public $USER_ONBOARDING_SCREEN_STYLES: UserOnboardingStylesProps
  public $SEARCH_FEED_STYLES: SearchFeedStyleProps
  public $UPLOADING_HEADER_STYLES: UploadingHeaderStylesProps
}
```

### Properties:

#### Color & Font Properties: 

- `$IS_DARK_THEME`: Sets the theme light or dark.
- `$HUE`: Sets the hue of the maintain consistency across the app.
- `$COLORS`: Sets the primary color, secondary color and primary font color.
- `$FONT_TYPES`: Sets the font across the app.
- `$BACKGROUND_COLORS`: Defines the custom background color in dark and light themes.
- `$TEXT_COLOR`: Sets the primary and secondary text color in light and dark themes.

#### Size Properties: 

- `$LMLoaderSizeiOS`: Defines the size of the loader on iOS.
- `$LMLoaderSizeAndroid`: Defines the size of the loader on iOS.


#### Screens Properties: 

- `$POLL_STYLE`: Customizes the style of Poll Component.
- `$UNIVERSAL_FEED_STYLE`: Customizes the style of Universal Feed Screen.
- `$POST_LIST_STYLE`: Customizes the style of posts, further you can customize post header, footer, postContent and media.
- `$LOADER_STYLE`: Defines the size and color of the loader across the app.
- `$POST_DETAIL_STYLE`: Customizes the style of post detail screen.
- `$CREATE_POST_STYLE`: Customizes the style of create post screen.
- `$POST_LIKES_LIST_STYLE`: Customizes the style of post likes list screen.
- `$NOTIFICATION_FEED_STYLE`: Customizes the style of notification feed screen.
- `$TOPICS_STYLE`: Sets the style for topics in posts.
- `$CAROUSEL_SCREEN_STYLE`: Customizes the style of carousel screen.
- `$CREATE_POLL_STYLE`: Customizes the style of create poll screen.
- `$USER_ONBOARDING_SCREEN_STYLES`: Customizes the style of user onboarding screen.
- `$SEARCH_FEED_STYLES`: Customizes style for search feed screen.
- `$UPLOADING_HEADER_STYLES`: Customizes style for the uploading header.

## Applying Custom Themes in Your Application

In this example, `LMFeedTheme` is configured using the `STYLES`

```tsx
import STYLES from "@likeminds.community/feed-rn-core";

const App = () => {
  useEffect(() => {
    // to set theme
    STYLES.setTheme({
      hue: 18,
      isDarkTheme: true,
      primaryColor: "#d26232",
      secondaryColor: "hsl(18, 47%, 31%)",

      // to change font
      fontTypes: {
        fontFamilyLight: "Montserrat-Light",
        fontFamilyMedium: "Montserrat-Medium",
        fontFamilySemiBold: "Montserrat-SemiBold",
        fontFamilyBold: "Montserrat-Bold",
        fontFamilyBlack: "Montserrat-Black",
      },

      // for custom primary font color across the app
      fontColor: "hsl(18, 75%, 59%)",

      // for custom text color in dark theme or light theme
      primaryDarkTextColor: "#ffffff",
      secondaryDarkTextColor: "grey",
      primaryLightTextColor: "#000000",
      secondaryLightTextColor: "grey",

      // for custom theme background color
      darkThemeBackgroundColor: "#000000",
      lightThemeBackgroundColor: "#ffffff",

      // for custom modal color in dark theme
      darkTransparentBackgroundColor: "#00000088",
    });

    // to set post list styles
    STYLES.setPostListStyles({
      header: {
        profilePicture: {
          size: 40,
          profilePictureStyle: {
            borderRadius: 20,
          },
          fallbackTextStyle: {
            color: "#888888",
            fontSize: 14,
          },
        },
        titleText: {
          color: "#333333",
          fontSize: 16,
          fontFamily: "Arial-BoldMT",
        },
      },
    });

  }, []);
  return <>{/* Your JSX code*/}</>;
};
```
