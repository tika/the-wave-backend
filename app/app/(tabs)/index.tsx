import * as React from 'react';
import { StyleSheet, View, TouchableOpacity } from "react-native";
import MapView from "react-native-maps";
import Ionicons from 'react-native-vector-icons/Ionicons';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import SettingsScreen from './settings';

type RootStackParamList = {
  Home: undefined;
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

function MapScreen() {
  const navigation = useNavigation<NavigationProp>();

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: 37.78825,
          longitude: -122.4324,
          latitudeDelta: 0.001,
          longitudeDelta: 0.001,
        }}
        showsUserLocation={true}
        userInterfaceStyle="dark"
        showsBuildings={false}
        zoomEnabled={true}
      />

      <TouchableOpacity 
        style={{
          position: 'absolute',
          top: 50,
          right: 20,
        }}
        onPress={() => navigation.navigate('Settings')}
      >
        <Ionicons 
          name="settings-outline" 
          size={24} 
          color="#fff"
        />
      </TouchableOpacity>
    </View>
  );
}

export default function HomeScreen() {
  return (
    <NavigationContainer independent={true}>
      <Stack.Navigator>
        <Stack.Screen
          name="Home" 
          component={MapScreen} 
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Settings" 
          component={SettingsScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
});

