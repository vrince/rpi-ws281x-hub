import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

const base = axios.create({
  baseURL: "http://192.168.2.109:5000"
});

Vue.prototype.$http = base;

export default new Vuex.Store({
  state: {
    queue: {},
    lastTask: {},
    tasks: [
      {
        title: "fire",
        name: "colorFire",
        icon: "mdi-fire",
        arguments: {
          from_color: "orange",
          to_color: "red",
          duration_s: 10,
          wait_s: 0.01
        }
      },
      {
        title: "rainbow",
        name: "rainbow",
        icon: "mdi-palette",
        arguments: {
          duration_s: 10,
          wait_s: 0.01
        }
      },
      {
        title: "gradient",
        name: "colorWipe",
        icon: "mdi-gauge",
        arguments: {
          color: "orange",
          wait_s: 0.5
        }
      },
      {
        title: "cycle",
        name: "rainbowCycle",
        icon: "mdi-pinwheel",
        arguments: {
          duration_s: 10,
          wait_s: 0.025
        }
      },
      {
        title: "random",
        name: "colorRandom",
        icon: "mdi-auto-fix",
        arguments: {
          duration_s: 10,
          wait_s: 0.025
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
    ]
  },
  mutations: {
    setQueue: (state, { queue }) => {
      state.queue = queue;
    },
    setLastTask: (state, { task }) => {
      state.lastTask = task;
    }
  },
  actions: {
    loadQueue: async function(context) {
      base.get("/queue").then(
        response => {
          context.commit("setQueue", { queue: response.data.data });
          return true;
        },
        err => {
          return false;
        }
      );
    },
    newTask: async function(context, task) {
      base.get(`task/${task.name}`, { params: task.arguments }).then(
        response => {
          context.commit("setLastTask", { task: response.data.data });
          return true;
        },
        err => {
          return false;
        }
      );
    }
  }
});
