<template>
  <div class="main-container">
    <HeaderComponent />
    <SidebarComponent />

    <div class="content">
      <div class="edit-material-container">
        <h1>{{ isEditMode ? 'Редактирование материала' : 'Добавление нового материала' }}</h1>

        <form @submit.prevent="saveMaterial">
          <div class="form-group">
            <label for="name">Название материала:</label>
            <input type="text" v-model="material.name" id="name" />
          </div>
          <div class="form-group">
            <label for="quantity">Количество:</label>
            <input type="number" v-model="material.quantity" id="quantity" />
          </div>
          <div class="form-group">
            <label for="unit">Ед. изм:</label>
            <input type="text" v-model="material.unit" id="unit" />
          </div>
          <div class="form-group">
            <label for="price">Цена за единицу:</label>
            <input type="number" v-model="material.pricePerUnit" id="price" />
          </div>
          <div class="form-group">
            <label for="stock">В наличии:</label>
            <input type="checkbox" v-model="material.inStock" id="stock" />
          </div>

          <div class="button-container">
            <button type="submit" class="save-button" @click="addProcurement">{{ isEditMode ? 'Сохранить изменения' : 'Сохранить' }}</button>
            <button type="button" class="cancel-button" @click="goToProcurements">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import SidebarComponent from '../bars/SidebarComponent.vue';
import axios from 'axios';
import {clearAllCookies, useCookies} from '@/src/js/useCookies';
const { getProjectId, getMaterialId } = useCookies();

export default {
  components: {
    HeaderComponent,
    SidebarComponent,
  },
  data() {
    return {
      material: {
        name: '',
        quantity: 0,
        unit: '',
        pricePerUnit: 0,
        inStock: false,
      },
      isEditMode: false, // Определяет режим редактирования или добавления
    };
  },
  methods: {
    async checkPath() {
      if (this.$route.path !== '/add_procurement') {
        try {
          const response = await axios.get(`/api/projects/${getProjectId()}/get_procurement/${getMaterialId()}`);
          this.material.name = response.data.procurement.item_name;
          this.material.quantity = response.data.procurement.quantity;
          this.material.unit = response.data.procurement.units;
          this.material.pricePerUnit = response.data.procurement.price;
          this.material.inStock = response.data.procurement.inStock;
        } catch (error) {
          if(error.response.status === 401){
              this.$store.commit('removeUsers');  // Изменяем состояние
              clearAllCookies();
              this.$router.push("/login");
            }
          console.error('Ошибка при загрузке Закупки:', error);
        }
        this.isEditMode = true;
      }
    },
    async addProcurement() {
      this.showErrors = true;

      if (this.material.name) {
        const dataToSend = {
          item_name: this.material.name,
          quantity: this.material.quantity,
          price: this.material.pricePerUnit,
          inStock: this.material.inStock,
          units: this.material.unit,
        };
        if (this.isEditMode) {
          try {
            await axios.put(`/api/projects/${getProjectId()}/update_procurement/${getMaterialId()}`, dataToSend, {
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            alert('Закупка успешно изменена!');
            this.$router.push(`/procurements`);
          } catch (error) {
            if(error.response.status === 401){
                this.$store.commit('removeUsers');  // Изменяем состояние
                clearAllCookies();
                this.$router.push("/login");
              }
            console.error("Ошибка сети:", error.message);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }
        } else {
          try {
            await axios.post(`/api/projects/${getProjectId()}/add_procurement`, dataToSend, {
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
              },
              withCredentials: true,
            });
            alert('Закупка успешно создана!');
            this.$router.push(`/procurements`);
          } catch (error) {
            if(error.response.status === 401){
                this.$store.commit('removeUsers');  // Изменяем состояние
                clearAllCookies();
                this.$router.push("/login");
              }
            console.error("Ошибка сети:", error.message);
            if (error.response && error.response.data.detail) {
              this.errorMessage = error.response.data.detail;
            }
          }
        }
      } else {
        this.errorMessage = 'Пожалуйста, заполните все поля.';
      }
    },
    goToProcurements() {
      this.$router.push(`/procurements`);
    }
  },
  beforeMount() {
    this.checkPath();
  },
};
</script>

<style scoped>
.edit-material-container {
  margin-left: 150px;
  padding-top: 60px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  font-weight: bold;
}

input {
  padding: 5px;
  margin-top: 5px;
}

.button-container {
  display: flex;
  gap: 10px;
}

.save-button, .cancel-button {
  padding: 10px 15px;
  background-color: #625b71;
  color: white;
  cursor: pointer;
  border: none;
  border-radius: 20px; /* Rounded corners */
}

.save-button:hover, .cancel-button:hover {
  background-color: #4f416d;
}
</style>
