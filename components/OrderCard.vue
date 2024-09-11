<template lang="pug">
v-card.mt-8(width="350px" flat)
    v-card-title
        v-row
          v-col.px-3.py-2.d-flex(cols=2)
            v-container.primary.rounded-lg.d-flex.align-center.justify-center(fluid)
              span.text-h6.text-center.white--text H
          v-col(cols=10)
            v-row.py-1.mx-2(align="center")
              v-col.d-flex.py-0.px-0(cols="12")
                .text-subtitle-1 Ariel Hikman
                v-spacer
                .info.px-2.d-flex.align-center.rounded-lg
                  v-icon.me-2 mdi-check-all
                  span.text-subtitle-2 Ready

              v-col.d-flex.align-center.px-0.py-0.pt-2(cols="12")
                .text-caption Pedido #925 / En local
                v-spacer
                v-sheet.green.rounded-lg.me-2(width=10 height=10)
                .text-caption Ready to serve

        v-row.px-5.py-2
          .text-body-2 Mie, Agosto 28, 2024
          v-spacer
          .text-body-2 06:12 PM

    v-card-text.px-2
        v-data-table(:headers="headers" :items="items" disable-filtering
        disable-pagination disable-sort hide-default-footer dense)

        v-row.px-8.pt-6.pb-4
          .text-subtitle-1.black--text Total
          v-spacer
          .text-subtitle-1.black--text $34000

    v-card-footer
        .px-7.d-flex.justify-center
          v-btn.text-subtitle-1.text-capitalize Ver detalles
          v-spacer
          v-btn.text-subtitle-1.text-capitalize(color="primary") Completado
</template>

<script>
export default {
  computed: {
    headers () {
      return [
        { text: 'Items', value: 'name', align: 'start' },
        { text: 'Cantidad', value: 'qty', align: 'center' },
        { text: 'Precio', value: 'price', align: 'center' }
      ]
    },
    items () {
      return [
        { name: 'Hamburguesa', qty: 2, price: '$12000' },
        { name: 'Perro Especial', qty: 2, price: '$16000' },
        { name: 'Gaseosa ', qty: 2, price: '$6000' }
      ]
    }
  }
}
</script>
