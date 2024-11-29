<template>
    <div class="task-item">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <button @click="$emit('details')">Подробнее</button>
      <button @click="deleteStage">>Удалить</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useCookies } from '@/src/js/useCookies';
  const { getProjectId } = useCookies();
  export default {
    props: {
      id: String,
      title: String,
      description: String,
    },
    methods: {
      async deleteStage() {
        if (confirm(`Удалить риск "${this.title}"?`)) {
          try {
            await axios.delete(`/api/projects/${getProjectId()}/delete_risk/${this.id}`, {
              headers: {
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
          } catch (error) {
            // Обработка ошибки, если нужно
            console.error(error);
          }

          this.$emit("delete", this.id);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .task-item {
    background-color: #f1f1f1;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
  }
  
  button {
    margin: 5px;
    padding: 5px 10px;
    background-color: #625b71;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>  