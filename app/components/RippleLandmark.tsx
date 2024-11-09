import React, { useEffect } from "react";
import { StyleSheet } from "react-native";
import { Marker } from "react-native-maps";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from "react-native-reanimated";

interface RippleLandmarkProps {
  coordinate: {
    latitude: number;
    longitude: number;
  };
}

export function RippleLandmark({ coordinate }: RippleLandmarkProps) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  useEffect(() => {
    scale.value = withRepeat(
      withTiming(4, {
        duration: 2000,
        easing: Easing.out(Easing.ease),
      }),
      -1,
      false
    );

    opacity.value = withRepeat(
      withTiming(0, {
        duration: 2000,
        easing: Easing.out(Easing.ease),
      }),
      -1,
      false
    );
  }, []);

  const rippleStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <Marker coordinate={coordinate}>
      <Animated.View style={[styles.ripple, rippleStyle]} />
      <Animated.View style={[styles.center]} />
    </Marker>
  );
}

const styles = StyleSheet.create({
  ripple: {
    position: "absolute",
    width: 20,
    height: 20,
    backgroundColor: "rgba(255, 255, 255, 0.4)",
    borderRadius: 10,
  },
  center: {
    width: 10,
    height: 10,
    backgroundColor: "#FFFFFF",
    borderRadius: 5,
  },
});
