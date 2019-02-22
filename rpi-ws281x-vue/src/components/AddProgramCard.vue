<template>
    <v-card color="primary" class="white--text">
        <v-card-title primary-title>
            <v-menu bottom right>
            <v-btn slot="activator" fab dark large>
                <v-icon v-if="select">{{ select.icon }}</v-icon>
                <v-icon v-else>more_vert</v-icon>
            </v-btn>
            <v-list two-line>
              <v-list-tile
                v-for="(task, i) in tasks"
                :key="i"
                @click="select = task">
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
            <v-btn v-if="select" icon fab @click="newTask(select)"><v-icon>mdi-play</v-icon></v-btn>
            <v-btn v-if="select" icon fab @click="select = null"><v-icon>mdi-close</v-icon></v-btn>
        </v-card-title>
        <v-card-text v-if="select">
            <v-card light v-for="color in colors" :key="color" class="mb-2">
                <swatches v-model="select.arguments[color]" inline colors="material-basic"></swatches>
            </v-card>
            <v-btn fab large color='error' absolute right bottom @click=""><v-icon>mdi-playlist-plus</v-icon></v-btn>
        </v-card-text>
    </v-card>
</template>

<script>
import { mapState, mapActions } from "vuex";
import Swatches from 'vue-swatches'
import "vue-swatches/dist/vue-swatches.min.css"

export default {
  components: {
      Swatches
      },
  data: () => ({
    select: null,
    color: null
  }),
  computed: {
      ...mapState(['tasks']),
      colors: function () {
          return this.select ? Object.keys(this.select.arguments).filter( a => a.indexOf('color') !== -1) : []
      }
      },
  methods: {...mapActions(['newTask'])}
};
</script>
