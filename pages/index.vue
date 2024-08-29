<template lang="pug">
v-container
  div.position-relative
    v-img(src="billos-logo.png" max-width="100px")
    h1.position-absolute.pedidos Pedidos
  div

</template>

<script>
export default {
  name: 'IndexPage',
}
</script>

<style>

.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
}

.pedidos {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

</style>
