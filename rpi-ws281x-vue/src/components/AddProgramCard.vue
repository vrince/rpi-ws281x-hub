<template>
  <v-card class="white--text">
    <v-card-title primary-title class="pa-2">
      <v-menu bottom right>
        <v-btn slot="activator" fab dark large class="mr-3">
          <v-icon v-if="select">{{ select.icon }}</v-icon>
          <v-icon v-else>mdi-plus</v-icon>
        </v-btn>
        <v-list two-line>
          <v-list-tile
            v-for="(task, i) in tasksList"
            :key="i"
            @click="createTask(task)"
          >
            <v-list-tile-action>
              <v-icon>{{ task.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ task.title }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ task.name }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-spacer />
      <v-btn
        v-if="select"
        color="success"
        fab small
        @click="sendTask({ task: select, duration: 10 })"
        ><v-icon>mdi-play</v-icon></v-btn
      >
      <v-btn v-if="select" color="primary" fab @click="saveTask"
        ><v-icon>mdi-plus</v-icon></v-btn
      >
      <v-btn v-if="select" color="error" fab small @click="select = null"
        ><v-icon>mdi-delete</v-icon></v-btn
      >
    </v-card-title>
    <v-card-text v-if="select">
      <v-container class="pa-0" grid-list-md text-xs-center>
        <v-layout row wrap ma-0 pa-0>
          <v-flex xs12 v-if="select && select.arguments.duration_s">
            <v-slider
              v-model="select.arguments.duration_s"
              :max="600"
              :min="10"
              step="10"
              ticks="always"
              tick-size="2"
              prepend-icon="mdi-timer"
              thumb-label="always"
            >
            </v-slider>
          </v-flex>
          <v-flex xs12 v-if="select && select.arguments.wait_ms">
            <v-slider
              v-model="select.arguments.wait_ms"
              :max="100"
              :min="10"
              step="5"
              ticks="always"
              tick-size="2"
              prepend-icon="mdi-play-speed"
              thumb-label="always"
            >
            </v-slider>
          </v-flex>
          <v-flex v-for="color in colorArgs" :key="color" xs12>
            <v-card
              class="pa-2"
              :color="select.arguments[color]"
              elevation="10"
            >
              <swatches
                v-model="select.arguments[color]"
                shapes="circles"
                inline
                :colors="colors"
              ></swatches>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapActions } from "vuex";
import Swatches from "vue-swatches";
import "vue-swatches/dist/vue-swatches.min.css";
import { tasks } from "../constant";

export default {
  components: {
    Swatches
  },
  data: () => ({
    select: null,
    color: null,
    colors: [
      "#FF0000",
      "#FF8000",
      "#FFFF00",
      "#80FF00",
      "#00FF00",
      "#00FF80",
      "#00FFFF",
      "#0080FF",
      "#0000FF",
      "#8000FF",
      "#FF00FF",
      "#FF0080"
    ]
  }),
  mounted() {},
  computed: {
    tasksList: function() {
      return tasks;
    },
    colorArgs: function() {
      return this.select
        ? Object.keys(this.select.arguments).filter(
            a => a.indexOf("color") !== -1
          )
        : [];
    }
  },
  methods: {
    ...mapActions(["sendTask", "addToProgram"]),
    createTask: function(task) {
      this.select = JSON.parse(JSON.stringify(task));
    },
    saveTask: function() {
      this.addToProgram(this.select);
      this.select = null;
    }
  }
};
</script>
