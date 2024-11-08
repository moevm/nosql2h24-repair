<template>
  <HeaderComponent />
  <ProjectSidebarComponent />
  <div class="task-page">
    <div class="task-header">
      <div>
        <h1>Ремонт кафедры МОЭВМ</h1>
        <p>СПбГЭТУ "ЛЭТИ"</p>
        <div class="task-title">
          <h2>Задача: покрасить полы</h2>
          <button @click="toggleEdit">{{ isEditing ? "Сохранить" : "Редактировать" }}</button>
        </div>
      </div>
    </div>

    <div class="task-content">
      <div class="task-description">
        <textarea v-if="isEditing" v-model="taskDescription" rows="5"></textarea>
        <p v-else>{{ taskDescription }}</p>
      </div>

      <div class="task-dates-status">
        <div class="task-dates">
          <div class="task-date">
            <p>Начало</p>
            <input type="date" v-model="startDate" :disabled="!isEditing" />
          </div>
          <div class="task-date">
            <p>Конец</p>
            <input type="date" v-model="endDate" :disabled="!isEditing" />
          </div>
        </div>
        <div class="task-status">
          <p>Статус</p>
          <select v-model="status" :disabled="!isEditing">
            <option value="in-progress">В процессе</option>
            <option value="not-selected">Не выбрано</option>
            <option value="overdue">Опоздание</option>
            <option value="completed">Готово</option>
          </select>
        </div>
      </div>

      <div class="task-contacts">
        <ContactsComponent />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import ContactsComponent from '../project/ContactsComponent.vue';

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    ContactsComponent
  },
  data() {
    return {
      isEditing: false,
      startDate: "2024-12-25",
      endDate: "2025-12-25",
      status: "in-progress",
      taskDescription: `1. Очистите поверхность пола от грязи и пыли.
      2. Нанесите грунтовку и дайте ей высохнуть.
      3. Используйте краску эмаль ПФ-115 (или другую, подходящую для полов).
      4. Нанесите краску валиком или кистью в 2 слоя, с перерывом на высыхание между слоями (24 часа).
      5. После завершения работы дайте полу высохнуть 48-72 часа перед эксплуатацией.`
    };
  },
  methods: {
    toggleEdit() {
      if (this.isEditing) {
        console.log("Сохранено:", this.startDate, this.endDate, this.status, this.taskDescription);
      }
      this.isEditing = !this.isEditing;
    }
  }
};
</script>

<style scoped>
.task-page {
  padding: 20px;
  margin-left: 150px;
  margin-top: 60px;
}

.task-header h1 {
  font-size: 24px;
}

.task-header p {
  font-size: 18px;
  color: #666;
}

.task-title {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.task-title h2 {
  font-size: 20px;
  margin-right: 10px;
}

.task-title button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-title button:hover {
  background-color: #0056b3;
}

.task-content {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.task-description {
  flex: 1;
  width: 80%;
}

.task-description p{
  width: 80%;
}

.task-description textarea {
  width: 80%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.task-dates-status {
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 14px;
}

.task-dates {
  display: flex;
  gap: 20px;
}

.task-date input[type="date"] {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.task-status select {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.task-contacts {
  margin-left: 20px;
}
</style>
