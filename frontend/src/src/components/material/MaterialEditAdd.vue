<template>
    <div class="main-container">
      <HeaderComponent />
      <ProjectSidebarComponent />
      
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
            
            <button type="submit" class="save-button">{{ isEditMode ? 'Сохранить изменения' : 'Добавить материал' }}</button>
          </form>
        </div>
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
    created() {
      const materialId = this.$route.params.id;
      if (materialId) {
        this.isEditMode = true;
        this.material = this.fetchMaterialById(materialId);
      }
    },
    methods: {
      fetchMaterialById(id) {
        const materials = [
          { id: 1, name: 'краска бежевая', quantity: 20, unit: 'банка 5 л.', pricePerUnit: 5000, totalCost: 100000, inStock: true },
          { id: 2, name: 'богемский кафель', quantity: 1500, unit: 'шт', pricePerUnit: 20000, totalCost: 3000000, inStock: false },
        ];
        return materials.find(material => material.id === parseInt(id)) || {};
      },
      saveMaterial() {
        if (this.isEditMode) {
          // Сохраняем изменения (например, обновляем материал в базе данных)
          console.log('Material updated:', this.material);
        } else {
          // Добавляем новый материал (например, сохраняем в базу данных)
          console.log('New material added:', this.material);
        }
        this.$router.push({ path: '/project/procurements' }); // Переход на главную страницу после сохранения
      },
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
  
  .save-button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  </style>  