import { Tabs } from "expo-router";
import React from "react";
import { StatusBar } from "expo-status-bar";
import { Ionicons } from '@expo/vector-icons';

export default function Layout() {
  return (
    <React.Fragment>
      <StatusBar style="auto" />
      <Tabs
        screenOptions={{
          headerShown: false,
          tabBarActiveTintColor: '#ffd700',
          tabBarInactiveTintColor: '#888',
          tabBarStyle: { backgroundColor: '#232946', borderTopWidth: 0 },
        }}
      >
        <Tabs.Screen
          name="map"
          options={{
            title: 'Map',
            tabBarIcon: ({ color, size }) => <Ionicons name="map" color={color} size={size} />,
          }}
        />
        <Tabs.Screen
          name="search"
          options={{
            title: 'Search',
            tabBarIcon: ({ color, size }) => <Ionicons name="search" color={color} size={size} />,
          }}
        />
      </Tabs>
    </React.Fragment>
  );
}
