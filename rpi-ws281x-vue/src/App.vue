<template>
  <v-app dark>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>RPI</span>
        <span class="font-weight-light">WS281x</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    </v-toolbar>
    <v-navigation-drawer v-model="drawer" fixed right app>
      <v-list>
        <v-list-tile>
          <v-toolbar-title class="headline">Settings</v-toolbar-title>
        </v-list-tile>
        <v-list-tile>
          <v-toolbar-title class="font-weight-light">Brightness</v-toolbar-title>
        </v-list-tile>
        <v-list-tile>
          <v-slider
            v-model="brightness"
            :min="5"
            step="5"
            ticks="always"
            prepend-icon="mdi-brightness-5"
            @change="sentBrightness"
          ></v-slider>
        </v-list-tile>
        <v-list-tile>
          <v-toolbar-title class="font-weight-light">Config</v-toolbar-title>
        </v-list-tile>
        <v-list-tile v-for="(value,key) in config" :key="key">
          {{key}}
          <span class="font-weight-light ma-2">{{value}}</span>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "App",
  components: {},
  data() {
    return {
      drawer: null,
      brightness: 10,
      config: null
    };
  },
  mounted() {
    this.$http.get("/config").then(res => (this.config = res.data.config));
  },
  computed: {},
  methods: {
    ...mapActions(["sendTask"]),
    sentBrightness: function() {
      this.sendTask({
        task: {
          name: "brighteness",
          arguments: { value: this.brightness / 100 }
        }
      });
    }
  }
};
</script>
