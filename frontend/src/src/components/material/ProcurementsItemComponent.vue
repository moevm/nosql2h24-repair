<template>
  <div class="purchase-item">
    <!-- Контейнер для групп, выстраивающий их в две колонки -->
    <div class="item-groups">
      <!-- Первая группа элементов -->
      <div class="item-group">
        <div class="item-row">
          <span class="label">Название материала:</span>
          <p class="value">{{ material.name }}</p>
        </div>
        <div class="item-row">
          <span class="label">Количество:</span>
          <p class="value">{{ material.quantity }}</p>
        </div>
        <div class="item-row">
          <span class="label">Ед. изм:</span>
          <p class="value">{{ material.unit }}</p>
        </div>
        <div class="item-row">
          <span class="label">Создатель Закупки</span>
          <p class="value">{{ material.user }}</p>
        </div>
        <div class="item-row">
          <span class="label">Дата создания заказа</span>
          <p class="value">{{ material.created_date }}</p>
        </div>
      </div>

      <!-- Вторая группа элементов -->
      <div class="item-group">
        <div class="item-row">
          <span class="label">Цена за единицу:</span>
          <p class="value">{{ material.pricePerUnit }} рублей</p>
        </div>
        <div class="item-row">
          <span class="label">Стоимость:</span>
          <p class="value">{{ material.totalCost }} рублей</p>
        </div>
        <div class="item-row">
          <span class="label">В наличии:</span>
          <p class="value">{{ material.inStock ? 'Да' : 'Нет' }}</p>
        </div>
        <div class="item-row">
          <span class="label">Роль Создателя</span>
          <p class="value">{{ material.userRole }}</p>
        </div>
        <div class="item-row">
          <span class="label">Дата поставки</span>
          <p class="value">{{ material.deliveryDate}}</p>
        </div>
      </div>
    </div>

    <!-- Кнопки внизу карточки -->
    <div class="button-group">
      <!-- Переход на страницу редактирования материала при нажатии на кнопку "Редактировать" -->
      <button @click="editMaterial" class="details-button">Редактировать</button>
      <button @click="deleteMaterial" class="delete-button">Удалить</button>
    </div>
  </div>
</template>

<script>
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
import axios from 'axios';
const { setMaterialId,getProjectId } = useCookies();
export default {
  props: {
    material: Object,
  },
  methods: {
    // Метод для перехода на страницу редактирования материала
    editMaterial() {
      setMaterialId(this.material.materialId);
      this.$router.push('/material');
    },
    async deleteMaterial() {
      if (confirm(`Удалить материал "${this.material.name}"?`)) {
        try {
          await axios.delete(`/api/projects/${getProjectId()}/delete_procurement/${this.material.materialId}`, {
            headers: {
              'Accept': 'application/json',
            },
            withCredentials: true,
          });
          this.$emit('delete', this.material.materialId);
        } catch (error) {
          if(error.response.status === 401){
            this.$store.commit('removeUsers');  // Изменяем состояние
            clearAllCookies();
            this.$router.push("/login");
          }
          // Обработка ошибки, если нужно
          console.error(error);
        }


      }
    }
  },
};
</script>

<style scoped>
.purchase-item {
  display: flex;
  justify-content: center;
  width: auto;
  height: auto;
  flex-direction: column;
  background-color: #f1f1f1;
  padding: 20px;
  margin: 10px 0;
  border-radius: 5px;
}

.item-groups {
  display: flex;
  justify-content: space-between;
}

.item-group {
  width: 48%;
}

.item-row {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.label {
  font-weight: bold;
  color: #333;
  width: 130px;
}

/* Стиль для элементов <p> */
.value {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px 10px;
  color: #555;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #ffffff;
  margin-left: 10px; /* Отступ слева для разделения */
  flex-grow: 2;
}
  
/* Контейнер для кнопок */
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Стили кнопок */
.details-button,
.delete-button {
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  border-radius: 10px;
}

.details-button {
  background-color: #625b71;
  color: white;
}

.delete-button {
  background-color: #625b71;
  color: white;
}
</style>
