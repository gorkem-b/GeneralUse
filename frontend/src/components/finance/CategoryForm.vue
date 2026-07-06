<template>
  <div class="bg-slate/50 backdrop-blur-md p-8 rounded-2xl shadow-lg ring-1 ring-white/5">
    <h3 class="mt-0 mb-6 text-[#F0F0F0] text-xl font-bold tracking-tight">Add Category</h3>
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Name</label>
        <input type="text" v-model="name" required placeholder="e.g. Groceries" class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Type</label>
        <select v-model="type" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner">
          <option value="EXPENSE">Expense</option>
          <option value="INCOME">Income</option>
        </select>
      </div>
      <button type="submit" class="mt-2 bg-gradient-to-r from-electric to-[#1c65d9] text-white p-3.5 border-none rounded-lg cursor-pointer font-bold transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_8px_20px_rgba(41,121,255,0.4)]">Save Category</button>
    </form>
  </div>
</template>

<script setup>
/**
 * CategoryForm Component
 * Allows users to add a new category.
 */
import { ref } from 'vue';
import { useFinanceStore } from '../../stores/financeStore';

const financeStore = useFinanceStore();
const name = ref('');
const type = ref('EXPENSE');

const handleSubmit = async () => {
  if (!name.value) return;
  await financeStore.createCategory({ name: name.value, type: type.value });
  name.value = '';
  type.value = 'EXPENSE';
};
</script>
