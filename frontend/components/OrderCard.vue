<template lang="pug">
v-card(width="300px" elevation=10)
  v-card-title
    v-row(dense)
      //- Primera letra del cliente
      v-col.primary.d-flex.align-center.justify-center.rounded-lg(cols=2)
        span.text-h6.text-center.white--text {{ name[0] }}

      v-col.d-flex.align-center.ps-4(cols=8)
        div
          //- Nombre del cliente
          p.mb-0.text-subtitle-2 {{ name }}
          //- Si se recoge el pedido en el local o para llevar a domicilio
          p.mb-0.text-caption Pedido {{ `#${id}` }} / En local

      //- Estado del pedido
      v-col.d-flex.align-center.white--text.rounded-lg.justify-center(
      :class="setColorStatus(status)" cols=2)
        v-icon.px-1(color="white") {{ setIconStatus(status) }}

  v-card-text
    //- Fecha de solicitud de la orden
    p.text-body-2.text-justify.my-2 {{ createdAt }}

    //- Items - Cantidades - Precio individual
    v-data-table(:headers="headers" :items="products" disable-filtering
    disable-pagination disable-sort hide-default-footer dense)
      template(#item.name="{ item }")
        div.d-flex.align-center.text-caption {{ item.name }}
      template(#item.price="{ item }")
        span {{ `$${item.price.toLocaleString('es-ES')}` }}

    //- Cálculo de precio total
    div.text-right.mt-2.mb-4.text-subtitle-2
      | {{ `$${totalPrice.toLocaleString('es-ES')}` }}

    //- Estados de la orden
    div.d-flex.justify-space-between
      v-btn.primary.white--text(outlined @click="getDetails()")
        v-icon mdi-eye
      v-btn.info.white--text(outlined :disabled="status === 'PENDING'"
      @click="updateOrder(id, 'PENDING')")
        v-icon mdi-timer-sand
      v-btn.success.white--text(outlined :disabled="status === 'COMPLETED'"
      @click="updateOrder(id, 'COMPLETED')")
        v-icon mdi-check-circle-outline

  //- Detalles de la orden
  order-details(v-model="showDetails" :details="details")
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  props: {
    id: {
      type: Number,
      default: 1
    },
    name: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    phone: {
      type: String,
      default: ''
    },
    address: {
      type: String,
      default: ''
    },
    paymentMethod: {
      type: String,
      default: ''
    },
    products: {
      type: Array,
      default: new Array([])
    },
    status: {
      type: String,
      default: ''
    },
    createdAt: {
      type: String,
      default: ''
    },
    getOrders: {
      type: Function,
      default: () => {}
    }
  },
  data: () => ({
    showDetails: false,
    details: {
      phone: '',
      address: '',
      paymentMethod: '',
      description: ''
    }
  }),
  computed: {
    statuses () {
      return {
        PENDING: 'Pendiente',
        COMPLETED: 'Completado'
      }
    },
    headers () {
      return [
        { text: 'Items', value: 'name', align: 'start', class: 'px-0', cellClass: 'px-0' },
        { text: 'Cantidad', value: 'quantity', align: 'center', class: 'px-0', cellClass: 'px-0' },
        { text: 'Precio', value: 'price', align: 'end', class: 'px-0', cellClass: 'px-0' }
      ]
    },
    orderStatus () {
      return this.$store.state.orders.orderStatus
    },
    totalPrice () {
      return this.products.reduce((total, product) => {
        return total + Number(product.quantity) * Number(product.price)
      }, 0)
    }
  },
  methods: {
    ...mapMutations({
      showSnackbar: 'snackbar/show'
    }),
    getDetails () {
      this.details.phone = this.phone
      this.details.address = this.address
      this.details.paymentMethod = this.paymentMethod
      this.details.description = this.description
      this.showDetails = true
    },
    async updateOrder (id, status) {
      try {
        const message = (await this.$axios.$put(`/api/orders/orders/${id}`,
          { status })).message
        this.getOrders()
        this.showSnackbar({ type: 'success', text: message })
      } catch (err) {
        this.showSnackbar({ type: 'error', text: err.response.data.message })
      }
    },
    setColorStatus (theStatus) {
      return theStatus === 'PENDING'
        ? 'info'
        : 'success'
    },
    setIconStatus (theStatus) {
      return theStatus === 'PENDING'
        ? 'mdi-timer-sand'
        : 'mdi-check-circle-outline'
    }
  }
}
</script>
