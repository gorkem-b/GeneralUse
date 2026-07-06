/**
 * ============================================================================
 * FINANCE STORE (PINIA)
 * ============================================================================
 * This is the "global brain" specifically for the financial data.
 * It holds the list of transactions, categories, and calculates the totals!
 */
import { defineStore } from 'pinia';
import api from '../services/api';

export const useFinanceStore = defineStore('finance', {
  // 1. STATE: The raw data variables.
  state: () => ({
    transactions: [], // Holds the array of transaction objects we get from the backend
    categories: [],   // Holds the array of category objects
    isLoading: false, // A boolean we turn to 'true' while waiting for the API to respond
    error: null,      // Holds any error messages if an API call fails
    paginationMeta: { // Since the API sends transactions in pages (e.g., 10 at a time), we store the page info here
      count: 0,       // Total number of transactions in the database
      next: null,     // URL to get the next page
      previous: null, // URL to get the previous page
    },
    
    // --- UI State ---
    isTransactionModalOpen: false,
    editingTransaction: null,
    
    // --- Global Date Filters ---
    dateFilter: 'ALL', // 'ALL', 'THIS_MONTH', 'LAST_30', 'THIS_YEAR'
  }),
  
  // 2. GETTERS: Think of getters like computed properties. 
  // They take the raw state data and calculate something new automatically.
  getters: {
    /**
     * Calculates the Total Income.
     * It goes through every transaction, checks if its category is an "INCOME" category,
     * and adds up the amounts!
     */
    totalIncome: (state) => {
      // .filter() keeps only the transactions that match our rule (is it INCOME?)
      return state.transactions
        .filter(t => state.categories.find(c => c.id === t.category)?.type === 'INCOME')
        // .reduce() adds up all the amounts from the filtered list into a single number
        .reduce((sum, t) => sum + parseFloat(t.amount), 0);
    },
    
    /**
     * Calculates the Total Expense using the exact same logic as Total Income.
     */
    totalExpense: (state) => {
      return state.transactions
        .filter(t => state.categories.find(c => c.id === t.category)?.type === 'EXPENSE')
        .reduce((sum, t) => sum + parseFloat(t.amount), 0);
    },
    
    /**
     * Calculates the Net Balance simply by subtracting Expenses from Income.
     * Because this is a getter, if ANY transaction changes, this updates instantly!
     */
    netBalance() {
      return this.totalIncome - this.totalExpense;
    }
  },
  
  // 3. ACTIONS: Functions that fetch data from or send data to the backend.
  actions: {
    // ========================================================================
    // CATEGORY ACTIONS
    // ========================================================================
    
    // Fetch all categories from the API and save them to the state.
    async fetchCategories() {
      try {
        const response = await api.get('/api/categories/');
        this.categories = response.data; // Save the JSON data into our state variable
      } catch (error) {
        this.error = error; // If something breaks, save the error so the UI can show it
      }
    },
    
    // Create a new category
    async createCategory(payload) {
      await api.post('/api/categories/', payload);
      // After successfully creating it on the backend, we fetch the whole list again to update the UI.
      await this.fetchCategories(); 
    },
    
    // Update an existing category
    async updateCategory(id, payload) {
      await api.put(`/api/categories/${id}/`, payload);
      await this.fetchCategories();
    },
    
    // Delete a category
    async deleteCategory(id) {
      await api.delete(`/api/categories/${id}/`);
      await this.fetchCategories();
    },

    // ========================================================================
    // TRANSACTION ACTIONS
    // ========================================================================
    
    // Fetch transactions, supporting pagination (e.g., params = { limit: 10 })
    async fetchTransactions(params = {}) {
      try {
        this.isLoading = true; // Turn on the loading spinner!
        
        // Calculate dynamic date ranges based on the global filter
        const today = new Date();
        let start_date = null;
        let end_date = null;

        if (this.dateFilter === 'THIS_MONTH') {
          start_date = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
          // End of month (technically day 0 of next month)
          end_date = new Date(today.getFullYear(), today.getMonth() + 1, 0).toISOString().split('T')[0];
        } else if (this.dateFilter === 'LAST_30') {
          const thirtyDaysAgo = new Date();
          thirtyDaysAgo.setDate(today.getDate() - 30);
          start_date = thirtyDaysAgo.toISOString().split('T')[0];
        } else if (this.dateFilter === 'THIS_YEAR') {
          start_date = new Date(today.getFullYear(), 0, 1).toISOString().split('T')[0];
          end_date = new Date(today.getFullYear(), 11, 31).toISOString().split('T')[0];
        }

        // Merge standard params with date filters if they exist
        const queryParams = { ...params };
        if (start_date) queryParams.start_date = start_date;
        if (end_date) queryParams.end_date = end_date;
        
        // Make the GET request to the backend. We pass params like ?limit=10 in the URL.
        const response = await api.get('/api/transactions/', { params: queryParams });
        
        // The backend uses DRF Pagination, so the data is wrapped in an object containing
        // "results", "count", "next", and "previous".
        if (response.data.results) {
          this.transactions = response.data.results; // Extract the actual array of data
          this.paginationMeta = { // Extract the pagination URLs
            count: response.data.count,
            next: response.data.next,
            previous: response.data.previous
          };
        } else {
          // Fallback just in case pagination gets turned off on the backend
          this.transactions = response.data;
        }
      } catch (error) {
        this.error = error;
      } finally {
        this.isLoading = false; // Turn off the loading spinner, no matter what happens
      }
    },
    
    // Add a new transaction
    async addTransaction(payload) {
      await api.post('/api/transactions/', payload);
      // Fetch the first page again to show the newly added transaction
      await this.fetchTransactions({ limit: 10 }); 
    },
    
    // Update an existing transaction
    async updateTransaction(id, payload) {
      await api.put(`/api/transactions/${id}/`, payload);
      await this.fetchTransactions({ limit: 10 });
    },
    
    // Delete a transaction
    async deleteTransaction(id) {
      await api.delete(`/api/transactions/${id}/`);
      await this.fetchTransactions({ limit: 10 });
    },

    // ========================================================================
    // UI ACTIONS
    // ========================================================================
    openTransactionModal(transaction = null) {
      this.editingTransaction = transaction;
      this.isTransactionModalOpen = true;
    },
    
    closeTransactionModal() {
      this.editingTransaction = null;
      this.isTransactionModalOpen = false;
    },

    async setDateFilter(filterType) {
      this.dateFilter = filterType;
      // Re-fetch transactions with the new filter
      await this.fetchTransactions({ limit: 10 });
    }
  }
});
