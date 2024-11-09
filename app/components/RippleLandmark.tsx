import React, { useEffect } from "react";
import { StyleSheet, View } from "react-native";
import { Marker } from "react-native-maps";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from "react-native-reanimated";
import { FireConfetti } from "./FireConfetti";

interface RippleLandmarkProps {
  coordinate: {
    latitude: number;
    longitude: number;
  };
  groupSize: number;
}

function calculateScale(groupSize: number) {
  return Math.log10(groupSize) * 10;
}

export function RippleLandmark({ groupSize, coordinate }: RippleLandmarkProps) {
  const scale = useSharedValue(calculateScale(groupSize));
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
      <View style={styles(groupSize).container}>
        <Animated.View style={[styles(groupSize).ripple, rippleStyle]} />
        <View style={styles(groupSize).center} />
        {[...Array(5)].map((_, index) => (
          <FireConfetti key={index} index={index} />
        ))}
      </View>
    </Marker>
  );
}

const styles = (groupSize: number) =>
  StyleSheet.create({
    container: {
      width: 20,
      height: 20,
      alignItems: "center",
      justifyContent: "center",
    },
    ripple: {
      position: "absolute",
      width: 20,
      height: 20,
      backgroundColor: "rgba(255, 255, 255, 0.4)",
      borderRadius: 10,
    },
    center: {
      width: calculateScale(groupSize),
      height: calculateScale(groupSize),
      backgroundColor: "#FFFFFF",
      borderRadius: 9999,
    },
  });
