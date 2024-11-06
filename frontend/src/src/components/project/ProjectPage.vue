<template>
  <div class="project-page">
    <HeaderComponent />
    <ProjectSidebarComponent />
    <main class="content">
      <div class="main-content">
        <div class="project-description">
          <h2>Ремонт кафедры МОЭВМ</h2>
          <p>СПбГЭТУ "ЛЭТИ"</p>
          <p>Ремонт кафедры МОЭВМ включает три ключевых этапа:</p>
          <ul>
            <li>1) подготовка,</li>
            <li>2) основной ремонт,</li>
            <li>3) оснащение.</li>
          </ul>
          <p>
            Сроки проекта составляют от 2 до 4 месяцев, включая 1-2 недели на подготовку и 2-4 недели на установку оборудования. В ходе работ заменяются инженерные коммуникации, отделываются стены и полы, устанавливаются современные системы освещения, вентиляции и учебное оборудование.
          </p>
          <p><strong>Материалы:</strong> применяются качественные строительные материалы (гипсокартон, ламинат), энергосберегающие осветительные приборы и высокопроизводительные компьютеры для лабораторий.</p>
          <p><strong>Риски:</strong> возможны задержки с поставками, непредвиденные работы, влияющие на сроки и бюджет, а также влияние на учебный процесс, которое требует координации работ.</p>
        </div>
        <div class="date-selectors">
          <DateSelectorComponent label="Начало" date="25.12.2024" />
          <DateSelectorComponent label="Конец" date="24.02.2025" />
        </div>
        <ContactsComponent />
      </div>
    </main>
  </div>
</template>

<script>
import HeaderComponent from '../bars/HeaderComponent.vue';
import ProjectSidebarComponent from '../bars/ProjectSidebarComponent.vue';
import DateSelectorComponent from '../project/DateSelectorComponent.vue'
import ContactsComponent from '../project/ContactsComponent.vue'

export default {
  components: {
    HeaderComponent,
    ProjectSidebarComponent,
    DateSelectorComponent,
    ContactsComponent,
  },
};
</script>

<style scoped>
.content {
  margin-left: 150px;
  padding-top: 60px;
}

.main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  gap: 20px;
}

.project-description {
  flex: 2;
  overflow-y: auto; /* Чтобы было удобно прокручивать длинный текст */
  padding-right: 10px;
  width: 1000px;
}

.project-description p:last-child {
  background-color: #f0f0f0;
  padding: 10px;
}

.date-selectors {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.contacts {
  flex: 1;
}
</style>