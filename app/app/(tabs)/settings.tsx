import { StyleSheet, Switch, useColorScheme } from 'react-native';
import { useState } from 'react';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import Ionicons from '@expo/vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function SettingsScreen() {
  const navigation = useNavigation();
  const colorScheme = useColorScheme();
  const insets = useSafeAreaInsets();
  const [isGhostMode, setIsGhostMode] = useState(false);

  return (
    <ThemedView style={[styles.container, { paddingTop: insets.top }]}>
      <ThemedView style={styles.header}>
        <Ionicons 
          name="arrow-back" 
          size={24}
          color={colorScheme === 'dark' ? 'white' : 'black'}
          onPress={() => navigation.goBack()}
          style={styles.backButton}
        />
        <ThemedText type="title">Settings</ThemedText>
      </ThemedView>

      <ThemedView style={styles.settingItem}>
        <ThemedText type="defaultSemiBold">Ghost Mode</ThemedText>
        <Switch
          value={isGhostMode}
          onValueChange={setIsGhostMode}
        />
      </ThemedView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    marginTop: 0,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
    marginTop: 20,
  },
  backButton: {
    marginRight: 15,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
});
