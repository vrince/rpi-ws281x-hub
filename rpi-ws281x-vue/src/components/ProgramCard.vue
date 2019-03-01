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
      ></v-btn>
      <v-chip v-if="duration" class="headline font-weight-light"
        ><v-icon left>mdi-timer</v-icon>{{ duration }}</v-chip
      >
      <v-chip v-if="speed" class="headline font-weight-light"
        ><v-icon left>mdi-play-speed</v-icon>{{ speed }}</v-chip
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
