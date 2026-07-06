<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Finance Center</h2>
      <div class="flex items-center gap-4">
        <select :value="financeStore.dateFilter" @change="financeStore.setDateFilter($event.target.value)" class="px-4 py-2 bg-charcoal/80 text-[#F0F0F0] border border-white/10 rounded-xl cursor-pointer font-inherit outline-none transition-all duration-200 hover:border-electric focus:ring-2 focus:ring-electric/50 shadow-inner">
          <option value="ALL">All Time</option>
          <option value="THIS_MONTH">This Month</option>
          <option value="LAST_30">Last 30 Days</option>
          <option value="THIS_YEAR">This Year</option>
        </select>
        <router-link to="/transactions" class="text-electric no-underline text-sm font-bold tracking-wider uppercase transition-opacity duration-200 hover:opacity-80">View All Transactions &rarr;</router-link>
      </div>
    </header>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="flex flex-col gap-8">
        <SummaryWidget 
          :total-income="financeStore.totalIncome"
          :total-expense="financeStore.totalExpense"
          :net-balance="financeStore.netBalance"
        />
        <ChartsWidget 
          :total-income="financeStore.totalIncome"
          :total-expense="financeStore.totalExpense"
          :transactions="financeStore.transactions"
          :categories="financeStore.categories"
        />
      </div>
      <div>
        <div class="bg-slate/40 backdrop-blur-md p-6 rounded-2xl shadow-xl ring-1 ring-white/10 relative overflow-hidden">
          <h3 class="mt-0 mb-4 text-[#F0F0F0] font-bold tracking-tight">Recent Transactions</h3>
          <div v-if="financeStore.isLoading" class="p-8 text-center text-gray-400">Loading ledger...</div>
          <div v-else>
            <TransactionTable 
              :transactions="financeStore.transactions"
              :categories="financeStore.categories"
              @edit="navigateToTransactions"
              @delete="handleDelete"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Local Floating Action Button -->
    <button 
      class="fixed bottom-8 right-8 w-[60px] h-[60px] rounded-full bg-electric text-white border-none text-3xl flex justify-center items-center cursor-pointer shadow-[0_0_20px_rgba(41,121,255,0.4)] transition-all duration-300 hover:scale-110 hover:-translate-y-2 hover:bg-[#1c65d9] hover:shadow-[0_0_30px_rgba(41,121,255,0.6)] z-50 ring-2 ring-white/20" 
      @click="financeStore.openTransactionModal()" 
      aria-label="Add Transaction">
      +
    </button>

    <!-- Local Transaction Form Modal -->
    <div v-if="financeStore.isTransactionModalOpen" class="fixed inset-0 bg-black/50 backdrop-blur-md flex justify-center items-center z-[100] animate-fade-in">
      <div class="w-full max-w-[500px] animate-slide-up">
        <TransactionForm 
          :transaction="financeStore.editingTransaction" 
          @save="financeStore.closeTransactionModal()" 
          @cancel="financeStore.closeTransactionModal()" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useFinanceStore } from '../stores/financeStore';

import SummaryWidget from '../components/finance/SummaryWidget.vue';
import ChartsWidget from '../components/finance/ChartsWidget.vue';
import TransactionTable from '../components/finance/TransactionTable.vue';
import TransactionForm from '../components/finance/TransactionForm.vue';

const financeStore = useFinanceStore();
const router = useRouter();

onMounted(async () => {
  await financeStore.fetchCategories();
  await financeStore.fetchTransactions({ limit: 5 });
});

const navigateToTransactions = () => {
  router.push('/transactions');
};

const handleDelete = async (id) => {
  if (confirm('Delete this transaction?')) {
    await financeStore.deleteTransaction(id);
  }
};
</script>
