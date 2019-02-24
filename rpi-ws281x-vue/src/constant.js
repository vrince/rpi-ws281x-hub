export const tasks = [
  {
    title: "fire",
    name: "colorFire",
    icon: "mdi-fire",
    arguments: {
      from_color: "#ffa500",
      to_color: "#ff4500",
      duration_s: 10,
      wait_ms: 10
    }
  },
  {
    title: "rainbow",
    name: "rainbow",
    icon: "mdi-palette",
    arguments: {
      duration_s: 10,
      wait_ms: 10
    }
  },
  {
    title: "gradient",
    name: "colorWipe",
    icon: "mdi-gauge",
    arguments: {
      color: "#ffa500",
      wait_ms: 50
    }
  },
  {
    title: "cycle",
    name: "rainbowCycle",
    icon: "mdi-pinwheel",
    arguments: {
      duration_s: 10,
      wait_ms: 25
    }
  },
  {
    title: "random",
    name: "colorRandom",
    icon: "mdi-auto-fix",
    arguments: {
      duration_s: 10,
      wait_ms: 25
    }
  },
  {
    title: "fade",
    name: "colorFade",
    icon: "mdi-weather-night",
    arguments: {
      duration_s: 60
    }
  }
];
