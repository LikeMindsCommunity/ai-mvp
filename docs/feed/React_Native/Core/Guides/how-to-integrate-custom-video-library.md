---
sidebar_position: 6
title: How to Integrate a Custom Video Library with LikeMinds Feed SDK ?
slug: /react-native/core/guide/how-to-integrate-custom-video-library
---

## Introduction

By default, our LikeMinds SDK uses the `react-native-video` library for video playback. To use this default library, install it as follows:

```bash
npm install react-native-video @types/react-native-video@5.0.14
```

However, if you prefer to use a custom video library, first uninstall `react-native-video` `@types/react-native-video` and you can configure your custom video library using the `videoCallback` and `videoCarouselCallback` props in the `LMOverlayProvider`. These callbacks provide access to playback control and video state, enabling custom integration with any video library of your choice.

## Steps to Configure a Custom Video Library

### Step 1: Import the Necessary Libraries and Configure LMOverlayProvider with Custom Video Callbacks

```jsx
import {
  LMOverlayProvider,
  LMFeedClient,
  initMyClient,
  Layout,
} from "@likeminds.community/feed-rn-core";
import { LMCoreCallbacks } from "@likeminds.community/feed-rn-core/setupFeed";
import { GestureHandlerRootView } from "react-native-gesture-handler";

// import your custom video library
import YourCustomVideoPlayer from "<path_to_custom_video_library>";

const App = () => {
  const [myClient, setMyClient] = useState<LMFeedClient>();
  const apiKey = "<YOUR_API_KEY>";
  const userName = "<USER_NAME>";
  const uuid = "<USER_ID>";

  useEffect(() => {
    async function generateClient() {
      const res: any = initMyClient();
      setMyClient(res);
    }
    generateClient();
  }, []);

  return (
    <>
      {userName && uuid && apiKey && myClient ? (
        <GestureHandlerRootView style={{ flex: 1 }}>
          <LMOverlayProvider
            myClient={myClient}
            apiKey={apiKey}
            userName={userName}
            userUniqueId={uuid}

            // Example of a custom video setup
            videoCallback={(videoProps) => {
              return (
                <YourCustomVideoPlayer
                  paused={videoProps.paused}
                  source={{ uri: videoProps.source }}
                  onLoad={(data) => videoProps.onLoad(data)}
                  style={videoProps.style}
                  muted={videoProps.muted}
                  repeat={videoProps.repeat}
                  resizeMode={videoProps.resizeMode}
                />
              );
            }}

            // Example for a video carousel setup
            videoCarouselCallback={(videoProps) => {
              return (
                <YourCustomVideoPlayer
                  paused={videoProps.paused}
                  source={{ uri: videoProps.source }}
                  onProgress={(x) => videoProps.setProgress(x)}
                  style={{
                    width: Layout.window.width,
                    height: Layout.window.height,
                  }}
                  resizeMode="contain"
                  muted={videoProps.muted}
                />
              );
            }}
          >
            {/* Add navigation container */}
          </LMOverlayProvider>
        </GestureHandlerRootView>
      ) : null}
    </>
  );
};

export default App;
```

#### Explanation of Callbacks

- `videoCallback`: Sets up your custom video component for single video playback. `videoProps` provides state information like `paused`, `muted`, `repeat`, and `resizeMode`, which you can pass to your custom player for handling playback.

- `videoCarouselCallback`: Configures the custom video component for carousel display. It includes a `setProgress` function to handle video playback progress within the carousel, as well as parameters like `paused` and `muted` to manage state.

### Step 2: Customize Your Video Player

Modify your custom video component as needed to fit your app’s design and functional requirements. The videoProps parameter in the callback functions provides access to important playback state and controls.
