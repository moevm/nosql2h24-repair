<template>
    <div class="date-selector">
      <label>{{ label }}</label>
      <div class="date-display">{{ date }}</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      label: String,
      date: String,
    },
  }
  </script>
  
  <style>
  .date-selector {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .date-display {
    padding: 5px;
    background-color: #f0f0f0;
    border-radius: 5px;
    text-align: center;
    width: 100px;
  }
  </style>  