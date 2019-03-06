<template>
  <v-card class="white--text" transition="fade-transition">
    <v-card-text class="scrollContainer">
      <div v-dragscroll.x="true" class="scrollDragZone">
        <v-layout row>
          <v-btn fab dark large round disabled class="ma-2 mb-4 mt-4 elevation-2"></v-btn>
          <v-btn
            fab
            dark
            large
            round
            :color="select && task.title === select.title ? 'primary' : ''"
            v-for="(task, i) in tasksList"
            :key="i"
            class="ml-4 mr-4 mb-4 mt-4 elevation-8"
            @click="selectTask(task)"
          >
            <v-icon>{{ task.icon }}</v-icon>
          </v-btn>
          <v-btn fab dark large round disabled class="ma-2 mb-4 mt-4 elevation-2"></v-btn>
        </v-layout>
      </div>
    </v-card-text>
    <transition name="fade">
      <v-card-text v-if="select">
        <v-container class="pa-0" grid-list-md text-xs-center>
          <v-layout row wrap ma-0 pa-0>
            <v-flex xs9>
              <v-flex xs12 v-if="select.arguments.duration_s">
                <v-slider
                  v-model="duration"
                  :max="durationLabels.length-1"
                  step="1"
                  :tick-labels="durationLabels"
                  always-dirty
                  ticks
                  tick-size="2"
                  prepend-icon="mdi-timer"
                ></v-slider>
              </v-flex>
              <v-flex xs12 v-if="select.arguments.wait_ms">
                <v-slider
                  v-model="select.arguments.wait_ms"
                  :max="100"
                  :min="5"
                  step="5"
                  ticks
                  tick-size="2"
                  prepend-icon="mdi-play-speed"
                ></v-slider>
              </v-flex>
            </v-flex>
            <v-flex xs3>
              <v-flex xs12>
                <v-btn v-if="select" light fab small @click="testTask">
                  <v-icon>mdi-play</v-icon>
                </v-btn>
              </v-flex>
              <v-flex xs12>
                <v-btn v-if="select" :color="'primary'" fab large @click="saveTask">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-flex>
            </v-flex>
            <v-flex v-for="color in colorArgs" :key="color" xs12>
              <v-card class="pa-2 pl-3 pr-3" :color="select.arguments[color]" elevation="6">
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
    </transition>
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
    duration: 0,
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
    ],
    durations: [30, 60, 120, 300, 600, 900],
    durationLabels: ["½", "1", "2", "5", "10", "15"]
  }),
  watch: {
    duration: function(val) {
      this.select.arguments.duration_s = this.durations[this.duration];
    }
  },
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
    selectTask: function(task) {
      if (this.select && this.select.title === task.title) {
        this.select = null;
        return;
      }
      this.select = JSON.parse(JSON.stringify(task));
    },
    saveTask: function() {
      this.addToProgram(this.select);
      this.select = null;
    }
  }
};
</script>

<style scoped>
.scrollSpacer {
  width: 48px;
}
.scrollContainer {
  padding: 0px;
  margin-left: calc(50% - 50vw);
  width: 100vw;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  background-color: rgba(255, 255, 255, 0.199);
}
.scrollDragZone {
  width: 100%;
  overflow: scroll;
  overflow: hidden;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
