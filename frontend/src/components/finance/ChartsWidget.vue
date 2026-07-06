<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-slide-up" style="animation-delay: 0.4s; opacity: 0; animation-fill-mode: forwards;">
    <!-- Cash Flow Bar Chart -->
    <div class="bg-slate/50 backdrop-blur-md p-6 rounded-2xl shadow-lg ring-1 ring-white/5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:ring-white/10">
      <h4 class="mt-0 mb-6 text-[#F0F0F0] font-medium text-center tracking-wide">Cash Flow (Income vs Expense)</h4>
      <div class="relative h-[300px] w-full">
        <Bar :data="barChartData" :options="barChartOptions" />
      </div>
    </div>

    <!-- Spending Distribution Donut Chart -->
    <div class="bg-slate/50 backdrop-blur-md p-6 rounded-2xl shadow-lg ring-1 ring-white/5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:ring-white/10">
      <h4 class="mt-0 mb-6 text-[#F0F0F0] font-medium text-center tracking-wide">Spending by Category</h4>
      <div class="relative h-[300px] w-full" v-if="hasExpenseData">
        <Doughnut :data="donutChartData" :options="donutChartOptions" />
      </div>
      <div v-else class="text-center text-gray-400 py-12 italic">
        No expense data available for chart.
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * ChartsWidget Component
 * Visualizes financial data using Chart.js
 * 1. Cash Flow Bar Chart (Income vs Expense)
 * 2. Expense Distribution Donut Chart
 */
import { computed } from 'vue';
import { Doughnut, Bar } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
import { useFinanceStore } from '../../stores/financeStore';

// Register Chart.js components
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const financeStore = useFinanceStore();

// ============================================================================
// CASH FLOW BAR CHART LOGIC
// ============================================================================
const barChartData = computed(() => {
  return {
    labels: ['Cash Flow'],
    datasets: [
      {
        label: 'Income',
        backgroundColor: '#00E676', // Neon Mint
        data: [financeStore.totalIncome],
        borderWidth: 0,
        borderRadius: 4,
      },
      {
        label: 'Expense',
        backgroundColor: '#FF5252', // Coral Red
        data: [financeStore.totalExpense],
        borderWidth: 0,
        borderRadius: 4,
      }
    ]
  };
});

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y', // Makes the bar chart horizontal
  scales: {
    x: {
      stacked: true,
      grid: { color: '#333' },
      ticks: { color: '#A0A0A0' }
    },
    y: {
      stacked: true,
      grid: { display: false },
      ticks: { display: false } // Hide the 'Cash Flow' label
    }
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: '#F0F0F0', font: { family: "'Inter', sans-serif" } }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: $${context.parsed.x.toFixed(2)}`;
        }
      }
    }
  }
};

// ============================================================================
// SPENDING DONUT CHART LOGIC
// ============================================================================
const backgroundColors = [
  '#FF5252', '#FF4081', '#E040FB', '#7C4DFF', 
  '#536DFE', '#448AFF', '#40C4FF', '#18FFFF', 
  '#64FFDA', '#69F0AE', '#B2FF59', '#EEFF41', 
  '#FFFF00', '#FFD740', '#FFAB40', '#FF6E40'
];

const expenseSummary = computed(() => {
  const summary = {};
  const expenses = financeStore.transactions.filter(t => {
    const cat = financeStore.categories.find(c => c.id === t.category);
    return cat && cat.type === 'EXPENSE';
  });
  
  expenses.forEach(t => {
    const cat = financeStore.categories.find(c => c.id === t.category);
    const catName = cat ? cat.name : 'Unknown';
    if (!summary[catName]) summary[catName] = 0;
    summary[catName] += parseFloat(t.amount);
  });
  
  return summary;
});

const hasExpenseData = computed(() => {
  return Object.keys(expenseSummary.value).length > 0;
});

const donutChartData = computed(() => {
  const labels = Object.keys(expenseSummary.value);
  const data = Object.values(expenseSummary.value);
  return {
    labels: labels,
    datasets: [{
      backgroundColor: backgroundColors.slice(0, labels.length),
      data: data,
      borderWidth: 1,
      borderColor: '#1E1E1E'
    }]
  };
});

const donutChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: { color: '#F0F0F0', font: { family: "'Inter', sans-serif" } }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) label += ': ';
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed);
          }
          return label;
        }
      }
    }
  }
};
</script>
