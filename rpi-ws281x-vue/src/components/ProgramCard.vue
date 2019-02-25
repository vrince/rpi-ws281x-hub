<template>
  <v-card class="white--text">
    <v-card-title primary-title class="pa-2">
      <v-btn fab dark large class="mr-3">
        <v-icon>{{ task.icon }}</v-icon>
      </v-btn>
      <v-btn
        v-for="(color, i) in colors"
        :key="i"
        :color="color"
        fab
        large
      ></v-btn>
      <v-btn v-if="duration" round large
        ><v-icon>mdi-timer</v-icon>{{ duration }}</v-btn
      >
      <v-btn v-if="speed" round large
        ><v-icon>mdi-play-speed</v-icon>{{ speed }}</v-btn
      >
      <v-spacer />
    </v-card-title>
  </v-card>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  components: {},
  props: {
    task: Object
  },
  data: () => ({}),
  computed: {
    colors: function() {
      const keys = Object.keys(this.task.arguments).filter(
        a => a.indexOf("color") !== -1
      );
      return keys.map(e => this.task.arguments[e]);
    },
    duration: function() {
      return this.task.arguments.duration_s
        ? `${this.task.arguments.duration_s} s`
        : "";
    },
    speed: function() {
      return this.task.arguments.wait_ms
        ? `${this.task.arguments.wait_ms} ms`
        : "";
    }
  },
  methods: {}
};
</script>
