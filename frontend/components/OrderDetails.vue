<template lang="pug">
v-dialog(v-model="value" width="500" @click:outside="$emit('input', false)")
  v-card
    v-card-title.primary.white--text Order details
      v-spacer
      v-btn(color="white" icon @click="$emit('input', false)")
        v-icon mdi-close
    v-card-text
      v-row(dense)
        v-col(cols="12")
          .primary--text.mt-4 Detalles de la orden
        v-col(cols="12")
          v-text-field(:value="details.address" label="Dirección" hide-details
          filled depressed readonly)
        v-col(cols="6")
          v-text-field(:value="details.phone" label="Teléfono" hide-details
          filled depressed readonly)
        v-col(cols="6")
          v-text-field(:value="details.paymentMethod" label="Forma de pago"
          hide-details filled depressed readonly)
        v-col(cols="12")
          v-textarea(:value="details.description" label="Descripción"
          hide-details filled depressed readonly)

    v-card-actions.pb-4
      v-spacer
      v-btn(@click="$emit('input', false)") Cancelar
</template>

<script>
export default {
  model: {
    prop: 'value',
    event: 'input'
  },
  props: {
    value: {
      type: Boolean,
      default: false
    },
    details: {
      type: Object,
      default: () => ({
        address: '',
        phone: '',
        paymentMethod: '',
        description: ''
      })
    }
  }
}
</script>
