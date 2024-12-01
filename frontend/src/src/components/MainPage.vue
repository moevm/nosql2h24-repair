<template>
  <div class="main-page">
    <HeaderComponent />
    <StaticSidebarComponent />
    <WorkerContentComponent v-if="userRole === 'Рабочий'" />
    <ContentComponent v-else-if="userRole !== 'Рабочий'" />
  </div>
</template>

<script>
import HeaderComponent from '../components/bars/HeaderComponent.vue';
import StaticSidebarComponent from '../components/bars/StaticSidebarComponent.vue';
import ContentComponent from '../components/ContentComponent.vue';
import WorkerContentComponent from '../components/main_content/WorkerContentComponent.vue';

export default {
  components: {
    HeaderComponent,
    StaticSidebarComponent,
    ContentComponent,
    WorkerContentComponent,
  },
  computed: {
    userRole() {
      const user = this.$store.getters.getUser[0];
      return user ? user.role : null;
    },
  },
};
</script>

<style scoped>
.access-denied {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 24px;
  color: red;
}
</style>