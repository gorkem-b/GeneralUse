<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Tasks Workspace</h2>
    </header>
    
    <div class="max-w-3xl w-full mx-auto mt-8">
      <TaskWidget 
        :tasks="tasksStore.collection" 
        :loading="tasksStore.loading" 
        @add="handleAdd" 
        @toggle="handleToggle" 
        @delete="handleDelete" 
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useTasksStore } from '../stores/tasksStore';
import TaskWidget from '../components/dashboard/TaskWidget.vue';

const tasksStore = useTasksStore();

onMounted(() => {
  tasksStore.fetchTasks();
});

const handleAdd = (taskData) => {
  tasksStore.addTask(taskData);
};

const handleToggle = (t) => {
  tasksStore.updateTask(t.id, { 
    ...t, 
    status: t.status === 'completed' ? 'pending' : 'completed' 
  });
};

const handleDelete = (id) => {
  tasksStore.deleteTask(id);
};
</script>
