<template>
  <div class="main-page">
    <HeaderComponent />
    <StaticSidebarComponent />
    <ContentComponent />
  </div>
</template>

<script>
import HeaderComponent from '../components/bars/HeaderComponent.vue';
import StaticSidebarComponent from '../components/bars/StaticSidebarComponent.vue';
import ContentComponent from '../components/ContentComponent.vue';

export default {
  components: {
    HeaderComponent,
    StaticSidebarComponent,
    ContentComponent,
  },
};
</script>

<style scoped>

</style>
