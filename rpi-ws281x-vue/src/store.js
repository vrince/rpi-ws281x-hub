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
        name: "fire",
        icon: "mdi-fire",
        arguments: {
          from_color: "orange",
          to_color: "red"
        }
      },
      {
        title: "rainbow",
        name: "rainbow",
        icon: "mdi-palette",
        arguments: {}
      },
      {
        title: "gradient",
        name: "gradient",
        icon: "mdi-gauge",
        arguments: {
          from_color: "orange",
          to_color: "red",
          wait_ms: 345
        }
      },
      {
        title: "fire",
        name: "rainbow-2",
        icon: "mdi-pinwheel",
        arguments: {}
      },
      {
        title: "fire",
        name: "magic",
        icon: "mdi-auto-fix",
        arguments: {}
      },
      {
        title: "fire",
        name: "star",
        icon: "mdi-weather-night",
        arguments: {}
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
