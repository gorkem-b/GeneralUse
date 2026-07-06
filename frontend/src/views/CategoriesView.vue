<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Spending Categories</h2>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-8">
      <div>
        <CategoryForm />
      </div>

      <div class="bg-slate p-6 rounded-lg shadow-[0_4px_6px_rgba(0,0,0,0.2)]">
        <h3 class="mt-0 mb-4 text-[#F0F0F0]">Your Categories</h3>
        <div v-if="financeStore.categories.length === 0" class="text-gray-400 italic">
          No categories found. Create one to get started.
        </div>
        <ul v-else class="list-none p-0 m-0 flex flex-col gap-4">
          <li v-for="category in financeStore.categories" :key="category.id" class="flex justify-between items-center p-4 bg-[#2A2A2A] rounded border-l-4 border-transparent hover:bg-[#333]">
            <div class="flex items-center gap-4">
              <span class="font-medium text-[#F0F0F0]">{{ category.name }}</span>
              <span :class="['text-xs px-2 py-1 rounded-full font-bold', category.type === 'INCOME' ? 'bg-[#00E676]/20 text-mint' : 'bg-[#FF5252]/20 text-coral']">
                {{ category.type }}
              </span>
            </div>
            <button @click="deleteCategory(category.id)" class="bg-transparent text-coral border border-coral px-4 py-2 rounded cursor-pointer transition-all duration-200 hover:bg-coral hover:text-white">Delete</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * SettingsView Component
 * Displays user settings and provides an interface for managing categories.
 */
import { onMounted } from 'vue';
import { useFinanceStore } from '../stores/financeStore';
import CategoryForm from '../components/finance/CategoryForm.vue';

const financeStore = useFinanceStore();

onMounted(() => {
  financeStore.fetchCategories();
});

const deleteCategory = async (id) => {
  if (confirm('Are you sure you want to delete this category?')) {
    await financeStore.deleteCategory(id);
  }
};
</script>
