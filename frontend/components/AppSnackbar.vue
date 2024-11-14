<template lang="pug">
v-snackbar(v-model="snackbar" :color="type" multi-line)
  span {{ text }}
  template.pe-0(#action="{ attrs }")
    v-btn(@click="snackbar=false" icon)
      v-icon mdi-close
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  computed: {
    text () { return this.$store.state.snackbar.text },
    type () { return this.$store.state.snackbar.type },
    snackbar: {
      get () { return this.$store.state.snackbar.snackbar },
      ...mapMutations({ set: 'snackbar/snackbar' })
    }
  }
}
</script>
