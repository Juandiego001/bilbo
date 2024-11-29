export const state = () => ({
  snackbar: false,
  text: '',
  type: 'success'
})

export const mutations = {
  snackbar (state, value) {
    state.snackbar = value
  },
  show (state, { type, text }) {
    state.type = type || 'success'
    state.text = text
    state.snackbar = true
  }
}
