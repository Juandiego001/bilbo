<template lang="pug">
v-dialog(v-model="value" width="500" @click:outside="$emit('input', false)"
@keydown.esc="$emit('input', false)")
  v-card
    v-card-title.primary.white--text Filter orders
      v-spacer
      v-btn(color="white" icon @click="$emit('input', false)")
        v-icon mdi-close
    v-card-text
      v-row(dense)
        v-col(cols="12")
          .primary--text.mt-4 Búsqueda de ordenes
        v-col(cols="6")
          v-text-field(v-model="id" label="Id" hide-details filled
          depressed)
        v-col(cols="6")
          v-text-field(v-model="name" label="Nombre del cliente"
          hide-details filled depressed)
        v-col(cols="6")
          v-text-field(v-model="phone" label="Teléfono" hide-details
          filled depressed)
        v-col(cols="6")
          v-text-field(v-model="paymentMethod" label="Método de pago"
          hide-details filled depressed)
        v-col(cols="12")
          v-text-field(v-model="products" label="Productos"
          hide-details filled depressed)

      v-row.mt-3(dense)
        v-col(cols="12")
          .primary--text.mt-2 Fecha de solicitud de la orden

        //- Seleccion de fecha inicial
        v-col(cols="6")
          v-dialog(ref="dialog" v-model="modalInitialDate"
          persistent width="290px")
            template(#activator="{ on, attrs }")
              v-text-field(v-model="initialDate" label="Fecha de inicio"
              prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"
              hide-details)
            v-date-picker(v-model="initialDate" scrollable)
              v-spacer
              v-btn(@click="modalInitialDate=false")  Cancel
              v-btn(color="primary" @click="modalInitialDate=false") OK

        //- Seleccion de fecha final
        v-col(cols="6")
          v-dialog(ref="dialog" v-model="modalFinalDate"
          persistent width="290px")
            template(#activator="{ on, attrs }")
              v-text-field(v-model="finalDate" label="Fecha de fiin"
              prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"
              hide-details)
            v-date-picker(v-model="finalDate" scrollable)
              v-spacer
              v-btn(@click="modalFinalDate=false")  Cancel
              v-btn(color="primary" @click="modalFinalDate=false") OK

    v-card-actions.pb-4
      v-spacer
      v-btn(@click="$emit('input', false)") Cancelar
      v-btn(v-if="searched" outlined color="primary" @click="cleanSearch()") Limpiar valores
      v-btn(color="primary" @click="search") Buscar
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  model: {
    prop: 'value',
    event: 'input'
  },
  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  data: () => {
    return {
      modalInitialDate: false,
      modalFinalDate: false,
      initialDate: '',
      finalDate: '',
      id: null,
      name: '',
      phone: '',
      paymentMethod: '',
      products: []
    }
  },

  computed: {
    orderStatus () {
      return this.$store.state.orders.orderStatus
    },
    searchData () {
      return this.$store.state.search.searchData
    },
    searched () {
      return this.$store.state.search.searched
    }
  },

  watch: {
    value (v) {
      if (v) {
        this.id = this.searchData.id
        this.name = this.searchData.name
        this.phone = this.searchData.phone
        this.paymentMethod = this.searchData.paymentMethod
        this.products = this.searchData.products
        this.initialDate = this.searchData.initialDate
        this.finalDate = this.searchData.finalDate
      }
    }
  },

  methods: {
    ...mapMutations({
      setSearchData: 'search/setSearchData',
      setSearched: 'search/setSearched'
    }),
    search () {
      const newSearchData = {
        id: this.id,
        name: this.name,
        phone: this.phone,
        paymentMethod: this.paymentMethod,
        products: this.products,
        initialDate: this.initialDate,
        finalDate: this.finalDate
      }
      this.setSearchData(newSearchData)

      // Verify if in the search form have some values
      const hasValues = Object.values(newSearchData)
        .some((value) => {
          if (Array.isArray(value)) { return value.length > 1 }
          return value !== '' && value !== null
        })
      if (hasValues) { this.setSearched(true) }

      this.$emit('input', false)
      this.$emit('search')
    },
    cleanSearch () {
      this.setSearchData({
        id: null,
        name: '',
        phone: '',
        paymentMethod: '',
        products: [],
        initialDate: '',
        endDate: ''
      })

      this.setSearched(false)
      this.$emit('input', false)
      this.$emit('search')
    }
  }
}
</script>
