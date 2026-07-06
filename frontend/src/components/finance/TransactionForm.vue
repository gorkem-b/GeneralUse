<template>
  <div class="bg-slate/80 backdrop-blur-xl p-8 rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.5)] ring-1 ring-white/10 relative overflow-hidden">
    <!-- Subtle background gradient -->
    <div class="absolute inset-0 bg-gradient-to-br from-electric/10 to-transparent pointer-events-none -z-10"></div>
    <h3 class="mt-0 mb-6 text-[#F0F0F0] text-2xl font-bold tracking-tight">{{ isEditing ? 'Edit Transaction' : 'Add Transaction' }}</h3>
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Amount</label>
        <input type="number" v-model="amount" step="0.01" min="0.01" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Date</label>
        <input type="date" v-model="date" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Category</label>
        <select v-model="category" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner">
          <option value="" disabled>Select a category</option>
          <option v-for="cat in financeStore.categories" :key="cat.id" :value="cat.id">
            {{ cat.name }} ({{ cat.type }})
          </option>
        </select>
      </div>
      <div class="flex flex-col gap-2">
        <label class="text-gray-300 font-medium text-sm tracking-wide">Description (Optional)</label>
        <input type="text" v-model="description" class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
      </div>
      <div class="flex gap-4 mt-4">
        <button type="submit" class="flex-1 bg-gradient-to-r from-electric to-[#1c65d9] text-white px-8 py-3.5 border-none rounded-lg cursor-pointer font-bold transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_8px_20px_rgba(41,121,255,0.4)]">Save</button>
        <button type="button" @click="$emit('cancel')" class="flex-1 bg-transparent text-[#F0F0F0] border border-white/10 px-8 py-3.5 rounded-lg cursor-pointer transition-all duration-300 hover:bg-white/5 hover:border-white/20 hover:-translate-y-1">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
/**
 * TransactionForm Component
 * Allows users to add a new transaction or edit an existing one.
 */
import { ref, onMounted } from 'vue';
import { useFinanceStore } from '../../stores/financeStore';

const props = defineProps({
  transaction: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['save', 'cancel']);
const financeStore = useFinanceStore();

const amount = ref('');
const date = ref('');
const category = ref('');
const description = ref('');
const isEditing = ref(false);

onMounted(() => {
  if (financeStore.categories.length === 0) {
    financeStore.fetchCategories();
  }
  
  if (props.transaction) {
    isEditing.value = true;
    amount.value = props.transaction.amount;
    date.value = props.transaction.date;
    category.value = props.transaction.category;
    description.value = props.transaction.description || '';
  } else {
    // Default to today
    date.value = new Date().toISOString().split('T')[0];
  }
});

const handleSubmit = async () => {
  if (!amount.value || !date.value || !category.value) return;
  
  const payload = {
    amount: amount.value,
    date: date.value,
    category: category.value,
    description: description.value
  };

  if (isEditing.value) {
    await financeStore.updateTransaction(props.transaction.id, payload);
  } else {
    await financeStore.addTransaction(payload);
  }
  
  emit('save');
};
</script>
