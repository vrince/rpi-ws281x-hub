<template>
  <v-container fluid grid-list-lg>
    <v-btn @click="$store.dispatch('loadQueue')">LOAD</v-btn>
    <v-layout row wrap>
      <v-flex xs12 v-for="item in this.queue.reserved" :key="item">
        <v-card color="blue-grey darken-2" class="white--text">
          <v-card-title primary-title>
            <div>
              <div class="headline">Unlimited music now</div>
              <span
                >Listen to your favorite artists and albums whenever and
                wherever, online and offline.</span
              >
            </div>
          </v-card-title>
          <v-card-actions>
            <v-btn flat dark>Listen now</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card color="primary" class="white--text">
            <v-card-title primary-title>
                <div class="headline">New</div>
                <v-spacer></v-spacer>
                <v-btn fab color='accent' @click="newTask('rainbow')"><v-icon>add</v-icon></v-btn>
            </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  data: () => ({}),
  computed: {...mapState(["queue"])},
  methods: {...mapActions(['newTask'])}
};
</script>
