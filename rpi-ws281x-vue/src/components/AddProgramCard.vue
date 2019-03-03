<template>
  <v-card class="white--text">
    <v-card-text class="pl-0 pr-0">
      <div v-dragscroll.x="true" :style="'{ width:100%; overflow: scroll; overflow: hidden;}'">
        <v-layout row>
          <v-btn
            fab
            dark
            large
            round
            :color="select && task.title === select.title ? 'primary' : ''"
            v-for="(task, i) in tasksList"
            :key="i"
            class="ma-4 elevation-8"
            @click="createTask(task)"
          >
            <v-icon>{{ task.icon }}</v-icon>
          </v-btn>
        </v-layout>
      </div>
    </v-card-text>
    <v-card-text v-if="select">
      <v-container class="pa-0" grid-list-md text-xs-center>
        <v-layout row wrap ma-0 pa-0>
          <v-flex xs8>
            <v-flex xs12 v-if="select.arguments.duration_s">
              <v-slider
                v-model="select.arguments.duration_s"
                :max="600"
                :min="30"
                step="30"
                ticks="always"
                tick-size="2"
                prepend-icon="mdi-timer"
                thumb-label="always"
              ></v-slider>
            </v-flex>
            <v-flex xs12 v-if="select.arguments.wait_ms">
              <v-slider
                v-model="select.arguments.wait_ms"
                :max="100"
                :min="5"
                step="5"
                ticks="always"
                tick-size="2"
                prepend-icon="mdi-play-speed"
                thumb-label="always"
              ></v-slider>
            </v-flex>
          </v-flex>
          <v-flex xs4>
            <v-btn v-if="select" color="success" fab small @click="testTask">
              <v-icon>mdi-play</v-icon>
            </v-btn>
            <v-btn v-if="select" color="error" fab small @click="select = null">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-btn v-if="select" color="primary" fab large @click="saveTask">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-flex>
          <v-flex v-for="color in colorArgs" :key="color" xs12>
            <v-card class="pa-2" :color="select.arguments[color]" elevation="8">
              <swatches
                v-model="select.arguments[color]"
                shapes="circles"
                inline
                colors="text-advanced"
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
import { dragscroll } from "vue-dragscroll";
import { tasks } from "../constant";

export default {
  directives: {
    dragscroll
  },
  components: {
    Swatches
  },
  data: () => ({
    select: null,
    color: null,
    swipeDirection: "None",
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
    testTask: function() {
      this.sendTask({
        task: this.select,
        duration: 10
      });
    },
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
