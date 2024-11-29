<template>
  <div class="stage-card">
    <div class="stage-tab">Этап {{ stage.id }}</div>
    <div class="stage-content">
      <div v-if="isEditing">
        <input v-model="editStageData.name" placeholder="Название этапа" />
        <input type="date" v-model="editStageData.startDate" placeholder="Дата начала" />
        <input type="date" v-model="editStageData.endDate" placeholder="Дата окончания" />
        <button @click="saveEdit">Сохранить</button>
        <button @click="cancelEdit">Отмена</button>
      </div>
      <div v-else>
        <div class="stage-header">
          <strong>{{ stage.name }}</strong>
          <div class="actions">
            <button @click="editStage">
              <img src="@/assets/icons/edit.png" alt="Edit Icon" class="icon icon-pencil" />
            </button>
            <button @click="deleteStage">
              <img src="@/assets/icons/delete.png" alt="Delete Icon" class="icon icon-trash" />
            </button>
          </div>
        </div>
        <div class="stage-dates">
          <div class="date-field">
            <span>Начало</span>
            <div class="date-value">
              <i class="icon-calendar"></i>
              {{ stage.startDate }}
            </div>
          </div>
          <div class="date-field">
            <span>Конец</span>
            <div class="date-value">
              <i class="icon-calendar"></i>
              {{ stage.endDate }}
            </div>
          </div>
          <button class="tasks-button" @click="goToTasks">
            <i class="icon-tasks"></i> К задачам
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useCookies } from '@/src/js/useCookies';
const { setStageId,setStageName, getProjectId } = useCookies();


export default {
  props: {
    stage: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isEditing: false,
      editStageData: {
        name: this.stage.name,
        startDate: this.stage.startDate,
        endDate: this.stage.endDate,
      },
    };
  },
  watch: {
    stage: {
      handler(newStage) {
        this.editStageData = { ...newStage };
      },
      deep: true,
    },
  },
  methods: {
    formatToDateTime(date) {
      return `${date}T00:00:00`; // Преобразует в формат `YYYY-MM-DDT00:00:00`
    },
    editStage() {
      this.isEditing = true;
    },
    async saveEdit() {
      const dataToSend = {
        name:this.editStageData.name,
        start_date: this.formatToDateTime(this.editStageData.startDate),
        end_date:  this.formatToDateTime(this.editStageData.endDate),
      };
      console.log(dataToSend)
      try {
        const res = await axios.put(`/api/projects/${getProjectId()}/update_stage/${this.stage.stageId}`, dataToSend, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          withCredentials: true,
        });
        console.log(res);
        this.isEditing = false;
        this.$emit('update-stage', { ...this.stage, ...this.editStageData });
      } catch (error) {
        console.error("Ошибка сети:", error.message);
        if (error.response) {
          console.error("Данные ответа:", error.response.data);
          // Вывод ошибки с сервера
          if (error.response.data.detail) {
            this.errorMessage = error.response.data.detail; // Сохраняем ошибку с сервера
          }
        }
      }


    },
    cancelEdit() {
      this.isEditing = false;
      this.editStageData = { ...this.stage };
    },
    async deleteStage() {
      if (confirm(`Удалить этап "${this.stage.name}"?`)) {
        try {
          await axios.delete(`/api/projects/${getProjectId()}/delete_stage/${this.stage.stageId}`, {
            headers: {
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
        } catch (error) {
          // Обработка ошибки, если нужно
          console.error(error);
        }

        this.$emit("delete", this.stage.stageId);
      }
    },
    async goToTasks() {
      setStageId(this.stage.stageId);
      setStageName(this.stage.name);
      this.$router.push(`/tasks`);
    },
  },
};
</script>

<style scoped>
.stage-card {
  width: 800px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 8px;
  margin: 0 auto 16px;
  position: relative;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.icon-pencil,
.icon-trash {
  width: 16px;
  height: 16px;
}

.stage-tab {
  position: absolute;
  top: -12px;
  left: 16px;
  background-color: #7a6f8f;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 14px;
}

.stage-content {
  margin-top: 16px;
}

.stage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
}

.actions button {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 4px;
}

.stage-dates {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
}

.date-field {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.date-field span {
  margin-right: 8px;
}

.date-value {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  background-color: #eaeaea;
  border-radius: 8px;
}

.icon-calendar {
  margin-right: 4px;
}

.tasks-button {
  background-color: #eaeaea;
  color: #333;
  border: none;
  border-radius: 8px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: bold;
  margin-top: 8px;
}

.tasks-button i {
  margin-right: 4px;
}
</style>
