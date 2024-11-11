<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="tasks-list-page">
    <h2>Задачи этапа: {{ stageName }}</h2>

    <button @click="addTask">Добавить задачу</button>

    <div v-if="tasks.length">
      <table class="task-table">
        <thead>
          <tr>
            <th>Название задачи</th>
            <th>Начало</th>
            <th>Конец</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="task in tasks" 
            :key="task.id"
            :class="{ selected: selectedTaskId === task.id }"
            @click="selectTask(task.id)"
          >
            <td>{{ task.title }}</td>
            <td>{{ task.startDate }}</td>
            <td>{{ task.endDate }}</td>
            <td>{{ task.status }}</td>
          </tr>
        </tbody>
      </table>
      
      <div class="task-actions" v-if="selectedTaskId">
        <button @click="viewTask(selectedTaskId)">Описание</button>
        <button @click="deleteTask(selectedTaskId)">Удалить</button>
      </div>
    </div>
    <div v-else>
      <p>Задачи отсутствуют для этого этапа.</p>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
  },
  // props: {
  //   stageId: {
  //     type: Number,
  //     required: true
  //   }
  // },
  data() {
    return {
      tasks: [
        { id: 1, title: 'Задача 1', startDate: '2024-01-01', endDate: '2024-01-10', status: 'В процессе' },
        { id: 2, title: 'Задача 2', startDate: '2024-01-05', endDate: '2024-01-15', status: 'Опоздание' },
        { id: 3, title: 'Задача 3', startDate: '2024-01-12', endDate: '2024-01-20', status: 'Готово' }
      ],
      nextTaskId: 4,
      selectedTaskId: null  // для отслеживания выбранной задачи
    };
  },
  computed: {
    stageName() {
      const stage = this.$route.params.stageId;
      return `Этап ${stage}`;
    }
  },
  methods: {
    addTask() {
      const newTask = {
        id: this.nextTaskId++,
        title: 'Новая задача',
        startDate: '',
        endDate: '',
        status: 'В процессе'
      };
      this.tasks.push(newTask);
      this.$router.push(`/tasks/${this.stageId}/${newTask.id}`); // переход на страницу новой задачи
    },
    deleteTask(taskId) {
      this.tasks = this.tasks.filter(task => task.id !== taskId);
      this.selectedTaskId = null;  // сбрасываем выбор после удаления
    },
    viewTask(taskId) {
      this.$router.push(`/tasks/${this.stageId}/${taskId}`);
    },
    selectTask(taskId) {
      this.selectedTaskId = taskId;
    },
    // async fetchStageData() {
    //   // try {
    //   //   const response = await axios.get(`/api/projects/${this.projectId}/get_task`);
    //   //   console.log(response.data);
    //   //   // this.stages = Object.values(response.data.stages).map(stage => ({
    //   //   //   name: stage.name,
    //   //   //   startDate: this.formatDate(stage.start_date),
    //   //   //   endDate: this.formatDate(stage.end_date),
    //   //   //   stageId: stage.id,
    //   //   // }));
    //   //   // console.log(this.stages);
    //   // } catch (error) {
    //   //   console.error('Ошибка при загрузке Этапов:', error);
    //   // }
    // },
    // beforeMount() {
    //   this.fetchStageData();
    // },
  }
};
</script>

<style scoped>
.tasks-list-page {
  padding: 20px;
  margin-left: 150px;
  margin-top: 60px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.task-table th, .task-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.task-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  text-align: left;
}

.task-table td {
  text-align: left;
}

.task-table tr:hover {
  background-color: #f5f5f5;
}

.task-table tr.selected {
  background-color: #e0f7fa; /* Подсветка выбранной задачи */
}

.task-actions {
  margin-top: 20px;
}

.task-actions button {
  padding: 5px 10px;
  margin-right: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-actions button:hover {
  background-color: #0056b3;
}
</style>
