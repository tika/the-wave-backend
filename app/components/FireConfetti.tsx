import React, { useEffect } from 'react';
import { StyleSheet } from 'react-native';
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
  withDelay,
  Easing,
} from 'react-native-reanimated';

interface FireConfettiProps {
  index: number;
}

export function FireConfetti({ index }: FireConfettiProps) {
  const translateY = useSharedValue(0);
  const translateX = useSharedValue(0);
  const opacity = useSharedValue(1);
  const scale = useSharedValue(1);

  useEffect(() => {
    const delay = index * 400;

    translateY.value = withRepeat(
      withDelay(
        delay,
        withSequence(
          withTiming(-30, { duration: 1000, easing: Easing.out(Easing.ease) }),
          withTiming(0, { duration: 1000, easing: Easing.in(Easing.ease) })
        )
      ),
      -1,
      true
    );

    translateX.value = withRepeat(
      withDelay(
        delay,
        withSequence(
          withTiming(20 * (index % 2 === 0 ? 1 : -1), { duration: 1500 }),
          withTiming(0, { duration: 1500 })
        )
      ),
      -1,
      true
    );

    opacity.value = withRepeat(
      withDelay(
        delay,
        withSequence(
          withTiming(1, { duration: 1000 }),
          withTiming(0, { duration: 1000 })
        )
      ),
      -1,
      true
    );

    scale.value = withRepeat(
      withDelay(
        delay,
        withSequence(
          withTiming(1.2, { duration: 1000 }),
          withTiming(0.8, { duration: 1000 })
        )
      ),
      -1,
      true
    );
  }, [index]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateY: translateY.value },
      { translateX: translateX.value },
      { scale: scale.value },
    ],
    opacity: opacity.value,
  }));

  return (
    <Animated.Text style={[styles.emoji, animatedStyle]}>🔥</Animated.Text>
  );
}

const styles = StyleSheet.create({
  emoji: {
    position: 'absolute',
    fontSize: 20,
  },
});
