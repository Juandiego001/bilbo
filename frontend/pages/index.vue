<template lang="pug">
v-container
  v-row.px-7.py-5
    .text-h5 Pedidos
    v-spacer
    .text-subtitle-1 {{ new Date().toDateString() }}

  v-row.px-7(align="center")
    div
      v-btn.text-capitalize(small) Todos
      v-btn.text-capitalize.mx-3(small color="primary") Pendientes
      v-btn.text-capitalize(small) Completados
    v-spacer
    v-text-field(
    prepend-icon="mdi-tune"
    label="Buscar nombre, pedido, o etc"
    solo
    dense
    hide-details
    append-outer-icon="mdi-magnify"
    width="50px")

  v-row.px-7.mb-12
    order-card(v-for="order, index in orders"
    :key="index"
    :index="index"
    :name="order.Nombre"
    :products="order.productos"
    :quantity="order.cantidad"
    :description="order.Descripcion.join()"
    :phone="order.Telefono"
    :address="order.Direccion"
    :paymentType="order['Forma de pago']")

</template>

<script>
export default {
  name: 'IndexPage',

  data: () => ({
    orders: []
  }),

  beforeMount () {
    this.getOrders()
  },

  methods: {
    async getOrders () {
      try {
        this.orders = await this.$axios.$get('/api/pedidos')
      } catch (err) {
        // eslint-disable-next-line no-console
        console.log(err)
      }
    }

  }
}
</script>
