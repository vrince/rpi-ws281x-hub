<template>
  <v-container fluid grid-list-lg>
    <v-layout row wrap>
      <v-flex xs12>
        <AddProgramCard></AddProgramCard>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import AddProgramCard from "./AddProgramCard"

export default {
  components: {
      AddProgramCard
      },
  data: () => ({}),
  computed: {...mapState(["queue"])},
  methods: {...mapActions(['newTask'])}
};
</script>
