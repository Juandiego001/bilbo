export const state = () => ({
  orderStatus: 'PENDING'
})

export const mutations = {
  setOrderStatus (state, text) {
    state.orderStatus = text
  }
}
