import colors from 'vuetify/es5/util/colors'

export default function ({ app }) {
  return {
    theme: {
      dark: false,
      themes: {
        light: {
          primary: '#0065A2',
          accent: '#B7C6E3',
          secondary: '#2A3541',
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: '#E57373',
          success: colors.green.darken3
        }
      }
    },
    icons: {
      iconfont: 'mdi'
    }
  }
}
