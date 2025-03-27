---
sidebar_position: 10
title: Trobleshooting Guides
slug: /react-native/core/guide/trobleshooting-guides.md
---

# Troubleshooting Guides
This section provides solutions and guidance for common challenges developers may encounter while working with the LikeMinds Feed SDK in React Native. From handling state resets to debugging unexpected behaviors, these guides aim to streamline your development process and help you implement best practices.

## How to Reset Store
In certain cases, you might need to reset LikeMinds SDK's Redux store to its initial state. This can be helpful when navigating back from LM Home Screen, logging out a user, or clearing data upon certain actions. The following example demonstrates how to implement a store reset action using the `LM_RESET_STORE` action type.

```tsx
// This component should be children component of LMOverlayProvider
const App = () => {
  const dispatch = useAppDispatch();
  // method to reset store
  const resetStore = () => {
    dispatch({ type: "LM_RESET_STORE", body: null });
  };

  // call this action in the children component of LMOverLayProvider
  useEffect(() => {
    // example of store reset on back press on universal feed header
    STYLES.setUniversalFeedStyles({
      screenHeader: {
        onBackPress() {
          resetStore();
        },
      },
    });
  }, []);
  return <></>;
};
```
