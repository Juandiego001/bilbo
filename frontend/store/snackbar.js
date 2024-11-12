export const state = () => ({
  snackbar: false,
  text: '',
  type: 'success',
  confirm: false
})

export const mutations = {
  snackbar (state, value) {
    state.snackbar = value
  },
  show (state, { type, text, confirm }) {
    state.confirm = confirm || false
    state.type = type || 'success'
    state.text = text
    state.snackbar = true
  }
}
