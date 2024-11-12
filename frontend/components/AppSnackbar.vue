<template lang="pug">
v-snackbar(v-model="snackbar" :color="type" :multi-line="!confirm"
:vertical="!!confirm")
  v-row(v-if="confirm")
    v-col(cols="10") {{ text }}
    v-col(cols="2")
      v-btn(@click="snackbar=false" icon)
        v-icon mdi-close
  span(v-else) {{ text }}
  template.pe-0(#action="{ attrs }")
    p-btn(v-if="!!confirm" :color="type" @click="updateLanguage") {{ confirm }}
    v-btn(v-else @click="snackbar=false" icon)
      v-icon mdi-close
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  computed: {
    text () { return this.$store.state.snackbar.text },
    type () { return this.$store.state.snackbar.type },
    confirm () { return this.$store.state.snackbar.confirm },
    language: {
      get () { return this.$store.state.app.language },
      ...mapMutations({ set: 'app/language' })
    },
    snackbar: {
      get () { return this.$store.state.snackbar.snackbar },
      ...mapMutations({ set: 'snackbar/snackbar' })
    }
  }
}
</script>
