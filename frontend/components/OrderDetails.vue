<template lang="pug">
v-dialog(v-model="value" width="500")
  v-card
    v-card-title
      span Order details
      v-spacer
      v-btn(icon @click="$emit('input', false)")
        v-icon mdi-close
    v-card-text
      v-row(dense)
        v-col(cols="12" md="12")
          v-text-field(:value="details.address" label="Dirección" hide-details
          filled depressed readonly)
        v-col(cols="6" md="12")
          v-text-field(:value="details.phone" label="Teléfono" hide-details
          filled depressed readonly)
        v-col(cols="6" md="12")
          v-text-field(:value="details.paymentMethod" label="Forma de pago"
          hide-details filled depressed readonly)
        v-col(cols="12" md="12")
          v-textarea(:value="details.description" label="Descripción"
          hide-details filled depressed readonly)
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
      default: true
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
