<template>
  <div>
    <v-container fluid grid-list-lg>
      <v-layout row wrap>
        <v-flex xs12>
          <ProgramCard
            v-for="(p, i) in program"
            :key="i"
            :task="p"
            class="mb-3"
          ></ProgramCard>
          <AddProgramCard></AddProgramCard>
        </v-flex>
      </v-layout>
    </v-container>
     <v-btn
      fab
      :disabled="!program.length"
      large
      fixed
      bottom
      left
      color="error"
      @click="clear"
      ><v-icon>mdi-delete</v-icon></v-btn
    >
    <v-btn
      fab
      :disabled="!program.length"
      large
      fixed
      bottom
      right
      color="success"
      @click="run"
      ><v-icon>mdi-play</v-icon></v-btn
    >
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import ProgramCard from "./ProgramCard";
import AddProgramCard from "./AddProgramCard";

export default {
  components: {
    ProgramCard,
    AddProgramCard
  },
  data: () => ({}),
  computed: { ...mapState(["queue", "program"]) },
  methods: { ...mapActions(["run","clear"]) }
};
</script>
