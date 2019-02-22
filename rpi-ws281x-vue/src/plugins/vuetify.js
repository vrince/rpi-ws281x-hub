import Vue from "vue";
import Vuetify from "vuetify/lib";
import "vuetify/src/stylus/app.styl";
import "@mdi/font/css/materialdesignicons.css";

import colors from "vuetify/es5/util/colors";

Vue.use(Vuetify, {
  iconfont: "mdi",
  theme: {
    primary: colors.cyan.darken1, // #E53935
    secondary: colors.yellow.lighten4, // #FFCDD2
    accent: colors.orange.base // #3F51B5
  }
});
