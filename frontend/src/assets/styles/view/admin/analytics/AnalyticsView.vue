<template>
  <div class="admin-analytics">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-white">数据分析</h1>
      <div class="flex gap-2">
        <Button label="导出报表" icon="pi pi-download" class="p-button-outlined" @click="exportReport" />
        <Button label="刷新数据" icon="pi pi-refresh" @click="refreshData" />
      </div>
    </div>

    <!-- 日期范围选择器 -->
    <div class="filters bg-gray-800 p-4 rounded-xl mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="date-range-picker md:col-span-2">
          <label class="block text-sm font-medium text-gray-300 mb-2">日期范围</label>
          <Calendar v-model="dateRange" selectionMode="range" :showIcon="true" :showButtonBar="true" class="w-full" />
        </div>

        <div class="filter-item">
          <label class="block text-sm font-medium text-gray-300 mb-2">数据类型</label>
          <Dropdown
            v-model="selectedDataType"
            :options="dataTypes"
            placeholder="选择数据类型"
            class="w-full"
            optionLabel="label"
            optionValue="value"
          />
        </div>

        <div class="filter-actions flex items-end">
          <Button label="应用筛选" icon="pi pi-filter" class="w-full" @click="applyFilters" />
        </div>
      </div>
    </div>

    <!-- 数据概览卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <div
        v-for="(stat, index) in overviewStats"
        :key="index"
        class="stat-card bg-gray-800 rounded-xl p-6"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-gray-400 text-sm mb-1">{{ stat.title }}</h3>
            <div class="text-2xl font-bold text-white">{{ stat.value }}</div>
            <div class="text-xs mt-2" :style="{ color: stat.trendColor }">
              <i :class="stat.trendIcon"></i>
              {{ stat.trend }}
            </div>
          </div>
          <div class="stat-icon w-12 h-12 rounded-full flex items-center justify-center" :style="{ backgroundColor: stat.iconBg }">
            <i :class="stat.icon + ' text-xl'" :style="{ color: stat.color }"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 用户增长趋势图 -->
      <div class="chart-card bg-gray-800 rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">用户增长趋势</h2>
          <div class="chart-actions flex">
            <Button
              v-for="period in ['日', '周', '月']"
              :key="period"
              :label="period"
              class="p-button-text p-button-sm"
              :class="{ 'p-button-outlined': selectedPeriod === period }"
              @click="selectedPeriod = period"
            />
          </div>
        </div>

        <div class="chart-container h-80 flex items-center justify-center">
          <div v-if="loadingChart" class="text-center">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载图表数据...</p>
          </div>
          <div v-else class="w-full h-full">
            <!-- 这里将来放置实际的图表组件 -->
            <div class="mock-chart w-full h-full bg-gray-700/20 rounded-lg flex items-center justify-center">
              <p class="text-gray-400">用户增长趋势图表</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 活跃用户分布图 -->
      <div class="chart-card bg-gray-800 rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">活跃用户分布</h2>
          <Button icon="pi pi-refresh" class="p-button-text p-button-rounded p-button-sm" @click="refreshChart" />
        </div>

        <div class="chart-container h-80 flex items-center justify-center">
          <div v-if="loadingChart" class="text-center">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载图表数据...</p>
          </div>
          <div v-else class="w-full h-full">
            <!-- 这里将来放置实际的图表组件 -->
            <div class="mock-chart w-full h-full bg-gray-700/20 rounded-lg flex items-center justify-center">
              <p class="text-gray-400">活跃用户分布饼图</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 更多图表 -->
    <div class="grid grid-cols-1 gap-6 mb-6">
      <!-- 用户行为分析 -->
      <div class="chart-card bg-gray-800 rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">用户行为分析</h2>
          <div class="chart-actions flex">
            <Dropdown
              v-model="selectedBehavior"
              :options="behaviorTypes"
              placeholder="选择行为类型"
              class="mr-2"
              optionLabel="label"
              optionValue="value"
            />
            <Button icon="pi pi-refresh" class="p-button-text p-button-rounded p-button-sm" @click="refreshChart" />
          </div>
        </div>

        <div class="chart-container h-96 flex items-center justify-center">
          <div v-if="loadingChart" class="text-center">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载图表数据...</p>
          </div>
          <div v-else class="w-full h-full">
            <!-- 这里将来放置实际的图表组件 -->
            <div class="mock-chart w-full h-full bg-gray-700/20 rounded-lg flex items-center justify-center">
              <p class="text-gray-400">用户行为分析图表</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 详细数据表格 -->
    <div class="data-table bg-gray-800 rounded-xl overflow-hidden">
      <div class="p-4 border-b border-gray-700">
        <h2 class="text-lg font-semibold text-white">详细数据</h2>
      </div>

      <DataTable
        :value="detailedData"
        :paginator="true"
        :rows="10"
        :loading="loadingTable"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[10, 20, 50]"
        currentPageReportTemplate="显示第 {first} 至 {last} 条，共 {totalRecords} 条"
        responsiveLayout="scroll"
        stripedRows
      >
        <template #empty>
          <div class="text-center p-4">
            <p class="text-gray-400">暂无数据</p>
          </div>
        </template>

        <template #loading>
          <div class="text-center p-4">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载数据...</p>
          </div>
        </template>

        <Column field="date" header="日期" sortable>
          <template #body="{ data }">
            <span class="text-gray-300">{{ data.date }}</span>
          </template>
        </Column>

        <Column field="newUsers" header="新增用户" sortable>
          <template #body="{ data }">
            <span class="text-cyan-400">{{ data.newUsers }}</span>
          </template>
        </Column>

        <Column field="activeUsers" header="活跃用户" sortable>
          <template #body="{ data }">
            <span class="text-purple-400">{{ data.activeUsers }}</span>
          </template>
        </Column>

        <Column field="aiInteractions" header="AI互动" sortable>
          <template #body="{ data }">
            <span class="text-pink-400">{{ data.aiInteractions }}</span>
          </template>
        </Column>

        <Column field="metaverseVisits" header="元宇宙访问" sortable>
          <template #body="{ data }">
            <span class="text-amber-400">{{ data.metaverseVisits }}</span>
          </template>
        </Column>

        <Column field="revenue" header="收入(¥)" sortable>
          <template #body="{ data }">
            <span class="text-green-400">{{ data.revenue }}</span>
          </template>
        </Column>

        <Column field="retention" header="留存率" sortable>
          <template #body="{ data }">
            <div class="w-full bg-gray-700 rounded-full h-2.5">
              <div class="bg-cyan-500 h-2.5 rounded-full" :style="{ width: `${data.retention}%` }"></div>
            </div>
            <span class="text-xs text-gray-400">{{ data.retention }}%</span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import AnalyticsViews from '@/server/view/admin/analytics/AnalyticsView'
</script>

<style>
@use '../../styles/view/admin/dashboard.scss'
</style>
