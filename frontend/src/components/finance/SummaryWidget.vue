<template>
  <div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-6">
    <div class="bg-slate/50 backdrop-blur-md p-6 rounded-2xl shadow-lg ring-1 ring-white/5 text-center animate-slide-up" style="animation-delay: 0.1s; opacity: 0; animation-fill-mode: forwards;">
      <h4 class="mt-0 mb-2 text-gray-400 font-medium text-xs uppercase tracking-wider">Total Income</h4>
      <div class="text-4xl font-bold font-mono text-mint tracking-tight">${{ totalIncome.toFixed(2) }}</div>
    </div>
    
    <div class="bg-slate/50 backdrop-blur-md p-6 rounded-2xl shadow-lg ring-1 ring-white/5 text-center animate-slide-up" style="animation-delay: 0.2s; opacity: 0; animation-fill-mode: forwards;">
      <h4 class="mt-0 mb-2 text-gray-400 font-medium text-xs uppercase tracking-wider">Total Expense</h4>
      <div class="text-4xl font-bold font-mono text-coral tracking-tight">${{ totalExpense.toFixed(2) }}</div>
    </div>

    <div class="bg-gradient-to-br from-charcoal to-[#1a1a1a] p-6 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.5)] text-center ring-1 ring-white/10 relative overflow-hidden animate-slide-up" style="animation-delay: 0.3s; opacity: 0; animation-fill-mode: forwards;">
      <div class="absolute inset-0 bg-gradient-to-t from-electric/5 to-transparent pointer-events-none"></div>
      <h4 class="mt-0 mb-2 text-gray-400 font-medium text-xs uppercase tracking-wider relative z-10">Net Balance</h4>
      <div class="text-4xl font-bold font-mono tracking-tight relative z-10" :class="netBalance >= 0 ? 'text-transparent bg-clip-text bg-gradient-to-r from-mint to-[#00b35c]' : 'text-transparent bg-clip-text bg-gradient-to-r from-coral to-[#cc0000]'">
        ${{ netBalance.toFixed(2) }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  totalIncome: {
    type: Number,
    required: true,
    default: 0
  },
  totalExpense: {
    type: Number,
    required: true,
    default: 0
  },
  netBalance: {
    type: Number,
    required: true,
    default: 0
  }
});
</script>
