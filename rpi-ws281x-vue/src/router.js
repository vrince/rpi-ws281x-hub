import Vue from "vue";
import Router from "vue-router";
import Program from "./components/Program";
import Settings from "./components/Settings";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Program
    },
    {
      path: "/settings",
      name: "settings",
      component: Settings
    }
  ]
});
