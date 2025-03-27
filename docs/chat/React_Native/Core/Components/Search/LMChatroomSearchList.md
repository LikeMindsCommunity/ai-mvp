---
sidebar_position: 4
title: Search List
slug: /react-native/core/components/search/search-list
---

## Overview

The `SearchList` component in the LikeMinds Chat React Native integration is responsible for rendering a list of search results. It dynamically displays user-related or message-related results based on search input, with options to highlight the matched search terms within the list items. This component manages the presentation of the search data, including handling user interactions like tapping on a search result to trigger navigation or additional actions.

<img
src={require('../../../../../static/img/reactNative/lmSearchList.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## Customisations

| Property                          | Type         | Description                                       |
| --------------------------------- | ------------ | ------------------------------------------------- |
| `userImageStyles`                 | `ImageStyle` | The style applied to the user image.              |
| `userNameStyles`                  | `TextStyle`  | The style applied to the user's name text.        |
| `timeStampStyles`                 | `TextStyle`  | The style applied to the timestamp text.          |
| `searchedHighlightedTextStyle`    | `TextStyle`  | The style applied to the highlighted search text. |
| `searchedNonHighlightedTextStyle` | `TextStyle`  | The style applied to the non-highlighted text.    |
