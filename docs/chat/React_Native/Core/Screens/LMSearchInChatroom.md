---
sidebar_position: 11
title: Search in Chatroom Screen
slug: /react-native/core/screens/search-in-chatroom-screen
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Overview

The `SearchInChatroom` screen enables users to search for messages and content within a specific chatroom in the LikeMinds chat application. It provides a user-friendly interface for entering search queries and displays relevant results, making it easy for users to find specific discussions, media, or topics within the chat history. This feature enhances user experience by improving navigation and accessibility of past conversations.

<img
src={require('../../../../static/img/reactNative/lmSearchList.webp').default}
alt="LMFeedMediaPreviewScreen"
style={{border: '2px solid #d6d6d6', padding: '8px', width: '40%'}}
/>

## UI Components

- [LMChatroomSearchList](../Components/Search/LMChatroomSearchList.md)
- [LMChatroomSearchHeader](../Components/Search/LMChatroomSearchHeader.md)

## Data Variables

- `search`: Text to be searched.

## Callbacks

- `customSearchHeader`: Custom function to render the search header component for the chatroom search interface.

## Customisation

The `SearchInChatroom` screen can be customised using the [`searchInChatroomStyles`](../Widgets/Components/Search/LMChatroomSearchHeader.md)

## Props

| Property             | Type       | Description                                  |
| -------------------- | ---------- | -------------------------------------------- |
| `customSearchHeader` | `Function` | Custom function to render the search header. |

## Usage Example

### Step 1: Create Custom Screen and Wrapper

- In your app, create a `SearchInChatroomScreenWrapper` file which will wrap the `SearchInChatroomScreen` within the `Chat` so that the callbacks becomes accessible inside of the `SearchInChatroomScreen`.
- Create `searchInChatroomStyles` for customisation and call the `setSearchInChatroomStyle` to set the customisation.

<Tabs>
<TabItem value="SearchInChatroomScreen" label="SearchInChatroomScreen">

```tsx
import {
  STYLES,
  SearchInChatroomComponent,
  useSearchInChatroomContext,
} from "@likeminds.community/chat-rn-core";

const SearchInChatroomScreen = () => {
  const { searchHeader } = useSearchInChatroomContext();

  const customSearchHeader = async () => {
    console.log("before custom searchHeader");
    const response = await searchHeader();
    console.log("response after custom searchHeader", response);
  };

  const searchInChatroomStyles = {
    backArrowColor: "red",
    crossIconColor: "blue",
    searchPlaceholderTextColor: "Search...",
  };

  // custom styling for search in chatroom screen
  if (searchInChatroomStyles) {
    STYLES.setSearchInChatroomStyle(searchInChatroomStyles);
  }

  return <SearchInChatroomComponent customSearchHeader={customSearchHeader} />;
};

export default SearchInChatroomScreen;
```

</TabItem>
<TabItem value="SearchInChatroomScreenWrapper" label="SearchInChatroomScreenWrapper">

```tsx
import { SearchInChatroomContextProvider } from "@likeminds.community/chat-rn-core";
import { SearchInChatroomScreen } from "<<path_to_SearchInChatroomScreen.tsx>>";

function SearchInChatroomScreenWrapper() {
  return (
    <SearchInChatroomContextProvider>
      <SearchInChatroomScreen />
    </SearchInChatroomContextProvider>
  );
}

export default SearchInChatroomScreenWrapper;
```

</TabItem>
</Tabs>

### Step 2: Add the Custom Screen in App.tsx

- In your `App.tsx`, create a `Stack.Navigator` in the `NavigationContainer` wrapped by `LMOverlayProvider`.
- Add `SearchInChatroomScreenWrapper` as a Stack screen in your `NavigationContainer`.

```tsx title="App.tsx"
import {
  SEARCH_IN_CHATROOM,
  LMOverlayProvider,
  Themes
} from "@likeminds.community/feed-rn-core";
import { SearchInChatroomScreenWrapper } from "<<path_to_SearchInChatroomScreenWrapper.tsx>>";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

export const App = () => {
  const Stack = createNativeStackNavigator();
  return (
    <LMOverlayProvider
      myClient={myClient} // pass in the LMFeedClient created
      apiKey={apiKey} // pass in the API Key generated
      userName={userName} // pass in the logged-in user's name
      userUniqueId={userUniqueID} // pass in the logged-in user's uuid
      theme={<"SDK_THEME">}
    >
      <NavigationContainer ref={navigationRef} independent={true}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen
            name={SEARCH_IN_CHATROOM}
            component={SearchInChatroomScreenWrapper}
            options={{
              gestureEnabled: Platform.OS === "ios" ? false : true,
              headerShown: false,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </LMOverlayProvider>
  );
};
```
