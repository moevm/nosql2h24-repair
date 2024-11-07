<template>
  <div class="tasks-list-page">
    <h2>Задачи этапа: {{ stageName }}</h2>
    <div v-if="tasks.length">
      <div v-for="task in tasks" :key="task.id">
        <router-link :to="`/tasks/${stageId}/${task.id}`">
          <div class="task-card">
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
          </div>
        </router-link>
      </div>
    </div>
    <div v-else>
      <p>Задачи отсутствуют для этого этапа.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    stageId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      tasks: [
        { id: 1, title: 'Задача 1', description: 'Описание задачи 1', stageId: this.stageId },
        { id: 2, title: 'Задача 2', description: 'Описание задачи 2', stageId: this.stageId }
      ]
    };
  },
  computed: {
    stageName() {
      const stage = this.$route.params.stageId;
      // Здесь можно получить название этапа на основе его ID, если данные хранятся в общем списке этапов.
      return `Этап ${stage}`;
    }
  }
};
</script>

<style scoped>
.task-card {
  background-color: #f9f9f9;
  padding: 10px;
  margin-top: 10px;
  border-radius: 5px;
}

.task-card h3 {
  margin: 0;
}

.task-card p {
  margin: 5px 0;
}
</style>
