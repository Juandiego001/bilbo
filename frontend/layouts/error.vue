<template lang="pug">
v-app
  v-main
    v-container(fluid fill-height)
      v-row(justify="center")
        v-col(cols="12" md="6" lg="4")
          v-alert.text-center.py-7(
          :color="errorMessage.type"
          border="top"
          prominent outlined)
            v-icon.mb-5(size="96" :color="errorMessage.type")
              | {{ errorMessage.icon }}

            .text-h3 {{ errorMessage.code }}
            .text-h6.text--secondary.mb-5 {{ errorMessage.message }}

            V-btn(:color="errorMessage.type" nuxt to="/") Regresar

  app-footer
</template>
<script>
export default {
  name: 'EmptyLayout',
  layout: 'empty',

  props: {
    error: { type: Object, default: null }
  },

  data () {
    return {
      pageNotFound: '404 Not Found.',
      insufficientPermissions: 'Insufficient permissions.',
      otherError: 'An error occurred.'
    }
  },

  head () {
    const title = this.errorMessage.message
    return { title }
  },

  computed: {
    errorMessage () {
      const code = this.error.statusCode
      let type = 'error'
      let icon = 'mdi-close-circle'
      let message = 'error.serverErrorMessage'

      if (code === 404) {
        message = 'Page not found'
        type = 'info'
        icon = 'mdi-comment-question'
      } else if (code === 403) {
        message = 'error.forbidenMessage'
        type = 'warning'
        icon = 'mdi-shield-lock'
      }

      return { type, code, icon, message }
    }
  }
}
</script>
