<template>
  <div class="flex flex-col gap-6">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0]">Transactions</h2>
    </header>

    <div>
      <!-- Edit events are also passed directly to the store -->
      <TransactionTable @edit="financeStore.openTransactionModal" />
      
      <!-- Basic Pagination Controls -->
      <div class="flex justify-between items-center mt-4 p-4 bg-slate rounded-lg" v-if="financeStore.paginationMeta.count > 10">
        <button 
          class="bg-[#333] text-white border-none px-4 py-2 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!financeStore.paginationMeta.previous"
          @click="loadPage(financeStore.paginationMeta.previous)"
        >Previous</button>
        <span class="text-[#F0F0F0]">Total: {{ financeStore.paginationMeta.count }}</span>
        <button 
          class="bg-[#333] text-white border-none px-4 py-2 rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!financeStore.paginationMeta.next"
          @click="loadPage(financeStore.paginationMeta.next)"
        >Next</button>
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
/**
 * TransactionsView Component
 * Manages the layout for viewing transactions. 
 */
import { onMounted } from 'vue';
import { useFinanceStore } from '../stores/financeStore';
import TransactionTable from '../components/finance/TransactionTable.vue';
import TransactionForm from '../components/finance/TransactionForm.vue';
import api from '../services/api';

const financeStore = useFinanceStore();

onMounted(async () => {
  await financeStore.fetchCategories();
  await financeStore.fetchTransactions({ limit: 10 });
});

const loadPage = async (url) => {
  if (!url) return;
  try {
    financeStore.isLoading = true;
    const response = await api.get(url);
    if (response.data.results) {
      financeStore.transactions = response.data.results;
      financeStore.paginationMeta = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous
      };
    }
  } catch (error) {
    financeStore.error = error;
  } finally {
    financeStore.isLoading = false;
  }
};
</script>
