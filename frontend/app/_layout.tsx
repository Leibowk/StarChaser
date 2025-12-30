import { Stack } from "expo-router";
import React from "react";
import { StatusBar } from "expo-status-bar";

export default function Layout() {
    return (
    <React.Fragment>
      <StatusBar style="auto" />
      <Stack 
        screenOptions={{
          headerTitleAlign: 'center',
          headerTintColor: '#ffd700',
          headerTransparent: true,
        }}
      />
    </React.Fragment>
  );
}