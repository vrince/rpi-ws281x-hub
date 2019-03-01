import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

// BASE_URL="http://192.168.2.109:5000" yarn serve
const base = axios.create({
  baseURL: process.env.VUE_APP_BASE_URL || ""
});

Vue.prototype.$http = base;

export default new Vuex.Store({
  state: {
    queue: {},
    lastTask: {},
    program: []
  },
  mutations: {
    setQueue: (state, { queue }) => {
      state.queue = queue;
    },
    setLastTask: (state, { task }) => {
      state.lastTask = task;
    },
    pushProgram: (state, { task }) => {
      state.program.push(task);
    },
    clearProgram: state => {
      state.program = [];
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
    sendTask: async function(context, { task, duration = null }) {
      const params = task.arguments;
      if (params.duration_s && duration) params.duration_s = duration;
      base.get(`task/${task.name}`, { params }).then(
        response => {
          context.commit("setLastTask", { task: response.data.data });
          return true;
        },
        err => {
          return false;
        }
      );
    },
    run: async function({ state }) {
      console.log(state.program);
      for (const key in state.program) {
        const task = state.program[key];
        base.get(`task/${task.name}`, { params: task.arguments }).then(
          response => {
            return true;
          },
          err => {
            return false;
          }
        );
      }
    },
    addToProgram: async function(context, task) {
      context.commit("pushProgram", { task });
    },
    clear: async function(context) {
      context.commit("clearProgram");
    }
  }
});
