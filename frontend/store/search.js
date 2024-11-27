export const state = () => ({
  searched: false,
  searchData: {
    id: null,
    name: '',
    phone: '',
    paymentMethod: '',
    products: [],
    initialDate: '',
    finalDate: ''
  }
})

export const mutations = {
  setSearchData (state, newSearchValues) {
    state.searchData = newSearchValues
  },
  setSearched (state, newSearched) {
    state.searched = newSearched
  }
}
