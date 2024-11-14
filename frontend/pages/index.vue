<template lang="pug">
v-container
  div.px-3.py-3.d-flex.align-center
    .text-h5 Pedidos
    v-spacer
    v-btn.white--text.me-2(icon :class="getColorAi()" @click="aiStatusDialog = true")
      v-icon {{ getIconAi() }}
    .text-subtitle-1 {{ new Date().toDateString() }}

  div.px-5.py-5.d-flex.align-center(align="center")
    div
      v-btn.text-capitalize(small @click="setOrderStatus('ALL')" :color="orderStatus === 'ALL' ? 'primary' : ''") Todos
      v-btn.text-capitalize.mx-3(small @click="setOrderStatus('PENDING')" :color="orderStatus === 'PENDING' ? 'info' : ''") Pendientes
      v-btn.text-capitalize(small @click="setOrderStatus('COMPLETED')" :color="orderStatus === 'COMPLETED' ?'success' : ''") Completados
    v-spacer
    v-text-field(prepend-icon="mdi-tune" label="Buscar nombre, pedido, o etc"
    solo dense hide-details append-outer-icon="mdi-magnify" width="50px")

  //- Diálogo para confirmar la activación/desactivación de la IA
  v-dialog(v-model="aiStatusDialog" max-width="500px")
    v-card
      v-card-title.white--text(:class="getDialogButtonColorIa()")
        | {{ getDialogTitleIa() }}
        v-spacer
        v-btn.white--text(icon @click="aiStatusDialog=false")
          v-icon mdi-close
      v-card-text.pt-3.pb-0
        p {{ getDialogTextIa() }}
      v-card-actions.pt-0
        v-spacer
        v-btn(@click="aiStatusDialog=false") Cancelar
        v-btn(:class="getDialogButtonColorIa()" @click="updateStatusAi()")
          | Confirmar

  v-row.px-6.mt-6
    order-card(v-if="orders.length" v-for="order, index in orders" :key="index"
    :id="order.id" :name="order.name" :description="order.description" :phone="order.phone"
    :address="order.address" :paymentMethod="order.payment_method" :products="order.products"
    :status="order.status" :createdAt="order.created_at" :getOrders="getOrders")
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  name: 'IndexPage',

  data: () => ({
    orders: [],
    aiStatus: true,
    aiStatusDialog: false
  }),

  computed: {
    orderStatus () {
      return this.$store.state.orders.orderStatus
    }
  },

  watch: {
    orderStatus () {
      this.getOrders()
    }
  },

  beforeMount () {
    this.getOrders()
    this.getStatusAi()
  },

  methods: {
    ...mapMutations({
      setOrderStatus: 'orders/setOrderStatus',
      showSnackbar: 'snackbar/show'
    }),
    async getOrders () {
      try {
        this.orders = (
          await this.$axios.$get(`/api/orders/orders/${this.orderStatus}`)
        ).orders
      } catch (err) {
        this.showSnackbar({ type: 'error', text: err.response.data.message })
      }
    },
    getIconAi () {
      return this.aiStatus ? 'mdi-robot' : 'mdi-robot-off'
    },
    getColorAi () {
      return this.aiStatus ? 'primary' : 'error'
    },
    // Título de diálogo para determinar si desea activar/desactivar la IA
    getDialogTitleIa () {
      return this.aiStatus
        ? '¿Seguro que desea desactivar la IA?'
        : '¿Desea volver a activar la IA?'
    },
    // Texto de diálogo para determinar lo que sucede al activar/desactivar la IA
    getDialogTextIa () {
      return this.aiStatus
        ? 'Al desactivar la IA, se desactivarán las respuestas automáticas hasta que se vuelva a activar la IA.'
        : 'Al activar la IA, se activan nuevamente las respuestas automáticas.'
    },
    getDialogButtonColorIa () {
      return this.aiStatus ? 'error' : 'primary'
    },
    async getStatusAi () {
      try {
        this.aiStatus = (await this.$axios.$get('/api/ai-status')).status
      } catch (err) {
        this.showSnackbar({ type: 'error', text: err.response.data.message })
      }
    },
    async updateStatusAi () {
      try {
        const message = (await this.$axios.$put('/api/ai-status', { status: !this.aiStatus })).message
        await this.getStatusAi()
        this.aiStatusDialog = false
        this.showSnackbar({ type: 'success', text: message })
      } catch (err) {
        this.showSnackbar({ type: 'error', text: err.response.data.message })
      }
    }
  }
}
</script>
