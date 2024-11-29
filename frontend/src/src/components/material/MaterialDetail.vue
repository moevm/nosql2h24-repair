<template>
    <div class="main-container">
      <HeaderComponent />
      <ProjectSidebarComponent />
      
      <div class="content">
        <div class="material-detail-container">
          <h1>{{ material.name }}</h1>
          <div class="material-info">
            <p><strong>Количество:</strong> {{ material.quantity }}</p>
            <p><strong>Ед. изм:</strong> {{ material.unit }}</p>
            <p><strong>Цена за единицу:</strong> {{ material.pricePerUnit }} руб</p>
            <p><strong>Стоимость:</strong> {{ material.totalCost }} руб</p>
            <p><strong>В наличии:</strong> {{ material.inStock ? 'Да' : 'Нет' }}</p>
          </div>
  
          <div class="buttons">
            <button @click="goBack" class="back-button">Назад</button>
            <button @click="goToEditMaterial" class="edit-button">Редактировать</button>
          </div>
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
        material: {},
      };
    },
    created() {
      const materialId = this.$route.params.id;
      // Загружаем данные материала по ID (например, из API или массива)
      this.material = this.fetchMaterialById(materialId);
    },
    methods: {
      fetchMaterialById(id) {
        // Здесь можно заменить на запрос к серверу, для примера используем жестко заданные данные
        const materials = [
          { id: 1, name: 'краска бежевая', quantity: 20, unit: 'банка 5 л.', pricePerUnit: 5000, totalCost: 100000, inStock: true },
          { id: 2, name: 'богемский кафель', quantity: 1500, unit: 'шт', pricePerUnit: 20000, totalCost: 3000000, inStock: false },
          // добавьте другие материалы здесь
        ];
        return materials.find(material => material.id === parseInt(id));
      },
      goBack() {
        this.$router.push({ path: '/project/procurements' }); // Переход на главную страницу
      },
      goToEditMaterial() {
        this.$router.push({ path: `/material/edit/${this.material.id}` }); // Переход на страницу редактирования
      },
    },
  };
  </script>
  
  <style scoped>
  .material-detail-container {
    margin-left: 150px;
    padding-top: 60px;
  }
  
  .material-info {
    margin-top: 20px;
  }
  
  .material-info p {
    font-size: 16px;
  }
  
  .buttons {
    margin-top: 20px;
  }
  
  .back-button,
  .edit-button {
    padding: 10px 15px;
    margin-right: 10px;
    cursor: pointer;
  }
  
  .back-button {
    background-color: #ccc;
  }
  
  .edit-button {
    background-color: #625b71;
    color: white;
  }
  </style>  