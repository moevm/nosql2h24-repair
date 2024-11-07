<template>
  <div class="task-page">
    <h2>Задача: {{ task.title }}</h2>
    <p>{{ task.description }}</p>
    <button @click="deleteTask" class="delete-task-btn">Удалить задачу</button>
  </div>
</template>

<script>
export default {
  props: {
    stageId: {
      type: Number,
      required: true
    },
    taskId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      task: {
        id: this.taskId,
        title: 'Задача 1',
        description: 'Описание задачи 1'
      }
    };
  },
  methods: {
    deleteTask() {
      if (confirm(`Удалить задачу "${this.task.title}"?`)) {
        // Удаление задачи, вы можете обновить данные с API или локально
        this.$router.push(`/tasks/${this.stageId}`);
      }
    }
  }
};
</script>

<style scoped>
.task-page {
  padding: 20px;
}

.delete-task-btn {
  padding: 10px 15px;
  background-color: #ff4c4c;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.delete-task-btn:hover {
  background-color: #ff1c1c;
}
</style>