<template>
  <div class="overflow-x-auto bg-slate/50 backdrop-blur-md rounded-2xl shadow-lg ring-1 ring-white/5 animate-slide-up" style="animation-delay: 0.5s; opacity: 0; animation-fill-mode: forwards;">
    <table class="w-full border-collapse" v-if="transactions.length > 0">
      <thead>
        <tr>
          <th class="p-5 text-left border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-xs bg-black/20">Date</th>
          <th class="p-5 text-left border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-xs bg-black/20">Category</th>
          <th class="p-5 text-left border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-xs bg-black/20">Description</th>
          <th class="p-5 text-left border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-xs bg-black/20 text-right">Amount</th>
          <th class="p-5 text-left border-b border-white/10 text-gray-400 font-semibold uppercase tracking-wider text-xs bg-black/20 text-right">Actions</th>
        </tr>
      </thead>
      <TransitionGroup name="list" tag="tbody">
        <tr v-for="t in transactions" :key="t.id" class="transition-colors duration-200 hover:bg-white/5">
          <td class="p-5 text-left border-b border-white/5">{{ t.date }}</td>
          <td class="p-5 text-left border-b border-white/5">
            <span :class="['text-xs px-3 py-1.5 rounded-full font-bold shadow-sm', getCategory(t.category)?.type === 'INCOME' ? 'bg-[#00E676]/20 text-mint ring-1 ring-[#00E676]/30' : 'bg-[#FF5252]/20 text-coral ring-1 ring-[#FF5252]/30']">
              {{ getCategory(t.category)?.name || 'Unknown' }}
            </span>
          </td>
          <td class="p-5 text-left border-b border-white/5">{{ t.description || '-' }}</td>
          <td class="p-5 text-left border-b border-white/5 text-right font-mono text-lg font-bold" :class="getCategory(t.category)?.type === 'INCOME' ? 'text-mint' : 'text-coral'">
            {{ getCategory(t.category)?.type === 'INCOME' ? '+' : '-' }}${{ t.amount }}
          </td>
          <td class="p-5 text-left border-b border-white/5 text-right flex gap-3 justify-end items-center">
            <button @click="$emit('edit', t)" class="bg-transparent text-[#F0F0F0] border border-white/10 px-3 py-1.5 rounded-lg cursor-pointer text-sm transition-all duration-300 hover:bg-white/10 hover:-translate-y-0.5 hover:shadow-md">Edit</button>
            <button @click="$emit('delete', t.id)" class="bg-transparent text-coral border border-coral/30 px-3 py-1.5 rounded-lg cursor-pointer text-sm transition-all duration-300 hover:bg-coral hover:text-white hover:-translate-y-0.5 hover:shadow-[0_4px_10px_rgba(255,82,82,0.4)]">Delete</button>
          </td>
        </tr>
      </TransitionGroup>
    </table>
    <div v-else class="p-12 text-center text-gray-400 italic">
      No transactions found.
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  transactions: {
    type: Array,
    required: true,
    default: () => []
  },
  categories: {
    type: Array,
    required: true,
    default: () => []
  }
});

const emit = defineEmits(['edit', 'delete']);

const getCategory = (id) => {
  return props.categories.find(c => c.id === id);
};
</script>
