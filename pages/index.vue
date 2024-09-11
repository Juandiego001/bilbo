<template lang="pug">
v-container
  v-row.px-7.py-5
    .text-h5 Pedidos
    v-spacer
    .text-subtitle-1 Miércoles, 28 Agosto 2024 

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
    template(v-for="order in orders")
    order-card(
      :name="order.Nombre"
      :products="order.productos"
      :quantity="order.cantidad"
      :description="order.Descripcion"
      :phone="order.Telefono"
      :address="order.Direccion"
      :payment_type="order['Forma de pago']"
    )
  
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
        console.log(err)
      }
    }

  }
}
</script>
