<template lang="pug">
v-navigation-drawer(color="primary" app dark)
  v-list-item
    v-list-item-content
      v-img.mx-auto(src="billos-logo.png" max-width="150px")
      v-list-item-title.text-subtitle-1.text-center Gestión de pedidos

  v-list(dense nav)
    template(v-for="menuItem in menuItems")
      v-list-item(nuxt :to="menuItem.path" :key="menuItem.path")
        v-list-item-icon
          v-icon {{ menuItem.icon }}
        v-list-item-content
          v-list-item-title.text-body-2 {{ menuItem.title }}
</template>

<script>
export default {
  data: () => ({
    menuItems: [
      {
        icon: 'mdi-food-outline',
        title: 'Pedidos',
        path: '/orders'
      }
    ]
  })
}
</script>
