import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

const base = axios.create({
//  baseURL: "http://192.168.2.109:5000"
});

Vue.prototype.$http = base;

export default new Vuex.Store({
  state: {
    queue: {},
    lastTask: {}
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
    newTask: async function(context, name) {
      base.get(`task/${name}`).then(
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
