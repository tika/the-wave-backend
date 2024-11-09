import { SplashScreen } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import MapView from "react-native-maps";
import { RippleLandmark } from "../../components/RippleLandmark";
import { ThemedText } from "../../components/ThemedText";

SplashScreen.preventAutoHideAsync();

export default function HomeScreen() {
  const coordinate = {
    latitude: 37.78225,
    longitude: -122.4324,
  };

  return (
    <View>
      <ThemedText
        style={{
          fontFamily: "ClashDisplay",
          fontSize: 20,
          textAlign: "center",
          marginTop: 60,
          marginBottom: 10,
        }}
      >
        name of app
      </ThemedText>
      <Text style={{ fontFamily: "ClashDisplay" }}>Group</Text>
      <MapView
        initialRegion={{
          ...coordinate,
          latitudeDelta: 0.001,
          longitudeDelta: 0.001,
        }}
        userInterfaceStyle="dark"
        showsBuildings={false}
        showsPointsOfInterest={false}
        showsCompass={false}
      >
        <RippleLandmark coordinate={coordinate} groupSize={100} />
      </MapView>
    </View>
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
