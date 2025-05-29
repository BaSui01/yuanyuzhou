<template>
  <div class="analytics-view">
    <div class="analytics-header">
      <div class="header-left">
        <h2>数据分析</h2>
        <p>查看和分析系统使用数据</p>
      </div>
      <div class="header-right">
        <Button label="导出报告" icon="pi pi-download" @click="exportReportDialog = true" />
      </div>
    </div>

    <div class="analytics-filters">
      <div class="filter-group">
        <Dropdown v-model="selectedPeriod" :options="periodOptions" optionLabel="name" placeholder="选择周期" class="filter-dropdown" />
      </div>

      <div class="filter-group">
        <Calendar v-model="dateRange" selectionMode="range" placeholder="自定义日期范围" :showIcon="true" class="date-range-picker" />
      </div>

      <div class="filter-group">
        <MultiSelect v-model="selectedMetrics" :options="metricOptions" optionLabel="name" placeholder="选择指标" class="metrics-dropdown" />
      </div>

      <div class="filter-group ml-auto">
        <Button icon="pi pi-cog" @click="showSettings = true" class="p-button-text" />
        <Button icon="pi pi-refresh" @click="refreshData" class="p-button-text" />
      </div>
    </div>

    <div class="analytics-metrics">
      <div class="metric-card">
        <div class="metric-icon">
          <i class="pi pi-users"></i>
        </div>
        <div class="metric-content">
          <h3>活跃用户</h3>
          <div class="metric-value">{{ formatNumber(metrics.activeUsers) }}</div>
          <div class="metric-trend" :class="{ 'positive': metrics.activeUsersTrend > 0, 'negative': metrics.activeUsersTrend < 0 }">
            <i :class="metrics.activeUsersTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(metrics.activeUsersTrend) }}% 较上期</span>
          </div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">
          <i class="pi pi-comments"></i>
        </div>
        <div class="metric-content">
          <h3>AI对话数</h3>
          <div class="metric-value">{{ formatNumber(metrics.conversations) }}</div>
          <div class="metric-trend" :class="{ 'positive': metrics.conversationsTrend > 0, 'negative': metrics.conversationsTrend < 0 }">
            <i :class="metrics.conversationsTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(metrics.conversationsTrend) }}% 较上期</span>
          </div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">
          <i class="pi pi-globe"></i>
        </div>
        <div class="metric-content">
          <h3>空间访问量</h3>
          <div class="metric-value">{{ formatNumber(metrics.spaceVisits) }}</div>
          <div class="metric-trend" :class="{ 'positive': metrics.spaceVisitsTrend > 0, 'negative': metrics.spaceVisitsTrend < 0 }">
            <i :class="metrics.spaceVisitsTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(metrics.spaceVisitsTrend) }}% 较上期</span>
          </div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">
          <i class="pi pi-clock"></i>
        </div>
        <div class="metric-content">
          <h3>平均使用时长</h3>
          <div class="metric-value">{{ metrics.avgUsageTime }}分钟</div>
          <div class="metric-trend" :class="{ 'positive': metrics.avgUsageTimeTrend > 0, 'negative': metrics.avgUsageTimeTrend < 0 }">
            <i :class="metrics.avgUsageTimeTrend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(metrics.avgUsageTimeTrend) }}% 较上期</span>
          </div>
        </div>
      </div>
    </div>

    <div class="analytics-charts">
      <div class="chart-card">
        <div class="chart-header">
          <h3>用户活跃度趋势</h3>
          <div class="chart-actions">
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('userActivity')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="userActivityChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>设备使用分布</h3>
          <div class="chart-actions">
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('deviceUsage')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="deviceUsageChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>AI助手使用情况</h3>
          <div class="chart-actions">
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('aiUsage')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="aiUsageChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>用户留存率</h3>
          <div class="chart-actions">
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('retention')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="retentionChart"></canvas>
        </div>
      </div>
    </div>

    <div class="analytics-tables">
      <div class="table-card">
        <div class="table-header">
          <h3>热门对话主题</h3>
        </div>
        <DataTable :value="topConversationTopics" :paginator="true" :rows="5" stripedRows>
          <Column field="rank" header="排名" style="width: 10%"></Column>
          <Column field="topic" header="主题" style="width: 30%"></Column>
          <Column field="count" header="对话数量" style="width: 20%"></Column>
          <Column field="percentage" header="占比" style="width: 20%">
            <template #body="slotProps">
              <div class="percentage-bar">
                <div class="percentage-value">{{ slotProps.data.percentage }}%</div>
                <div class="progress-bar">
                  <div class="progress-value" :style="{ width: slotProps.data.percentage + '%' }"></div>
                </div>
              </div>
            </template>
          </Column>
          <Column field="growth" header="增长率" style="width: 20%">
            <template #body="slotProps">
              <div class="trend" :class="{ 'positive': slotProps.data.growth > 0, 'negative': slotProps.data.growth < 0 }">
                <i :class="slotProps.data.growth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                <span>{{ Math.abs(slotProps.data.growth) }}%</span>
              </div>
            </template>
          </Column>
        </DataTable>
      </div>

      <div class="table-card">
        <div class="table-header">
          <h3>热门场景</h3>
        </div>
        <DataTable :value="topSpaceScenes" :paginator="true" :rows="5" stripedRows>
          <Column field="rank" header="排名" style="width: 10%"></Column>
          <Column field="scene" header="场景" style="width: 30%"></Column>
          <Column field="visits" header="访问量" style="width: 20%"></Column>
          <Column field="percentage" header="占比" style="width: 20%">
            <template #body="slotProps">
              <div class="percentage-bar">
                <div class="percentage-value">{{ slotProps.data.percentage }}%</div>
                <div class="progress-bar">
                  <div class="progress-value" :style="{ width: slotProps.data.percentage + '%' }"></div>
                </div>
              </div>
            </template>
          </Column>
          <Column field="growth" header="增长率" style="width: 20%">
            <template #body="slotProps">
              <div class="trend" :class="{ 'positive': slotProps.data.growth > 0, 'negative': slotProps.data.growth < 0 }">
                <i :class="slotProps.data.growth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
                <span>{{ Math.abs(slotProps.data.growth) }}%</span>
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <Dialog v-model:visible="showSettings" header="图表设置" :style="{ width: '500px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="chartType">图表类型</label>
          <Dropdown id="chartType" v-model="chartSettings.type" :options="chartTypeOptions" optionLabel="name" />
        </div>
        <div class="p-field-checkbox mb-3">
          <Checkbox v-model="chartSettings.showLegend" :binary="true" id="showLegend" />
          <label for="showLegend" class="ml-2">显示图例</label>
        </div>
        <div class="p-field-checkbox mb-3">
          <Checkbox v-model="chartSettings.stacked" :binary="true" id="stacked" />
          <label for="stacked" class="ml-2">堆叠显示</label>
        </div>
        <div class="p-field mb-3">
          <label for="dataPoints">数据点数量</label>
          <InputNumber id="dataPoints" v-model="chartSettings.dataPoints" :min="5" :max="30" />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showSettings = false" />
        <Button label="应用" icon="pi pi-check" @click="applySettings" />
      </template>
    </Dialog>

    <Dialog v-model:visible="exportReportDialog" header="导出分析报告" :style="{ width: '500px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="exportFormat">导出格式</label>
          <Dropdown id="exportFormat" v-model="exportFormat" :options="exportFormatOptions" optionLabel="name" />
        </div>
        <div class="p-field mb-3">
          <label>包含指标</label>
          <div class="metrics-checkboxes">
            <div class="p-field-checkbox mb-2" v-for="metric in metricOptions" :key="metric.value">
              <Checkbox v-model="exportMetrics" :value="metric" :binary="false" :inputId="'export_' + metric.value" />
              <label :for="'export_' + metric.value" class="ml-2">{{ metric.name }}</label>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="exportReportDialog = false" />
        <Button label="导出" icon="pi pi-download" @click="exportReport" :loading="loading" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useAdminAnalytics } from './composables/useAdminAnalytics'

export default {
  name: 'AnalyticsView',
  setup() {
    const {
      metrics,
      topConversationTopics,
      topSpaceScenes,
      loading,
      charts,
      periodOptions,
      selectedPeriod,
      dateRange,
      metricOptions,
      selectedMetrics,
      chartSettings,
      getAnalyticsData,
      initCharts,
      refreshData: apiRefreshData,
      applyChartSettings,
      exportReport: apiExportReport,
      downloadChart: apiDownloadChart,
      formatNumber
    } = useAdminAnalytics()

    // 图表引用
    const userActivityChart = ref(null)
    const deviceUsageChart = ref(null)
    const aiUsageChart = ref(null)
    const retentionChart = ref(null)

    // 设置对话框
    const showSettings = ref(false)

    // 导出对话框
    const exportReportDialog = ref(false)
    const exportFormat = ref({ name: 'PDF', value: 'pdf' })
    const exportMetrics = ref([])

    // 图表类型选项
    const chartTypeOptions = [
      { name: '线图', value: 'line' },
      { name: '柱状图', value: 'bar' },
      { name: '面积图', value: 'area' }
    ]

    // 导出格式选项
    const exportFormatOptions = [
      { name: 'PDF', value: 'pdf' },
      { name: 'Excel', value: 'xlsx' },
      { name: 'CSV', value: 'csv' }
    ]

    // 获取图表元素
    const getChartElements = () => {
      return {
        userActivity: userActivityChart.value,
        deviceUsage: deviceUsageChart.value,
        aiUsage: aiUsageChart.value,
        retention: retentionChart.value
      }
    }

    // 刷新数据
    const refreshData = async () => {
      await apiRefreshData(getChartElements())
    }

    // 应用设置
    const applySettings = async () => {
      await applyChartSettings(getChartElements())
      showSettings.value = false
    }

    // 下载图表
    const downloadChart = (chartId) => {
      apiDownloadChart(chartId)
    }

    // 导出报告
    const exportReport = async () => {
      await apiExportReport(exportFormat.value.value)
      exportReportDialog.value = false
    }

    // 监听周期变化
    watch(selectedPeriod, async () => {
      await refreshData()
    })

    // 监听日期范围变化
    watch(dateRange, async () => {
      if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
        await refreshData()
      }
    })

    // 初始化
    onMounted(async () => {
      // 设置默认导出指标
      exportMetrics.value = [...metricOptions]

      // 获取数据并初始化图表
      const response = await getAnalyticsData()
      if (response && response.charts) {
        initCharts(response.charts, getChartElements())
      }
    })

    return {
      metrics,
      topConversationTopics,
      topSpaceScenes,
      loading,
      userActivityChart,
      deviceUsageChart,
      aiUsageChart,
      retentionChart,
      periodOptions,
      selectedPeriod,
      dateRange,
      metricOptions,
      selectedMetrics,
      chartSettings,
      showSettings,
      chartTypeOptions,
      exportReportDialog,
      exportFormat,
      exportFormatOptions,
      exportMetrics,
      refreshData,
      applySettings,
      downloadChart,
      exportReport,
      formatNumber
    }
  }
}
</script>

<style lang="scss" scoped>
.analytics-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.analytics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-left {
    h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
    }

    p {
      margin: 4px 0 0;
      color: #666;
    }
  }
}

.analytics-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  background-color: #ffffff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

  .filter-group {
    .filter-dropdown {
      width: 150px;
    }

    .date-range-picker {
      width: 250px;
    }

    .metrics-dropdown {
      width: 250px;
    }
  }

  .ml-auto {
    margin-left: auto;
  }
}

.analytics-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;

  .metric-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;

    .metric-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;

      i {
        font-size: 1.8rem;
      }
    }

    &:nth-child(1) .metric-icon {
      background-color: rgba(76, 175, 80, 0.1);
      color: #4CAF50;
    }

    &:nth-child(2) .metric-icon {
      background-color: rgba(33, 150, 243, 0.1);
      color: #2196F3;
    }

    &:nth-child(3) .metric-icon {
      background-color: rgba(156, 39, 176, 0.1);
      color: #9C27B0;
    }

    &:nth-child(4) .metric-icon {
      background-color: rgba(255, 152, 0, 0.1);
      color: #FF9800;
    }

    .metric-content {
      flex: 1;

      h3 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
      }

      .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 8px 0;
      }

      .metric-trend {
        display: flex;
        align-items: center;
        font-size: 0.8rem;

        i {
          margin-right: 4px;
        }

        &.positive {
          color: #4CAF50;
        }

        &.negative {
          color: #F44336;
        }
      }
    }
  }
}

.analytics-charts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;

  .chart-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
      }

      .chart-actions {
        display: flex;
        align-items: center;
      }
    }

    .chart-content {
      height: 300px;
      position: relative;
    }
  }
}

.analytics-tables {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 24px;

  .table-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
      }
    }

    .percentage-bar {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .percentage-value {
        font-size: 0.9rem;
        font-weight: 500;
      }

      .progress-bar {
        height: 6px;
        background-color: #f0f0f0;
        border-radius: 3px;
        overflow: hidden;

        .progress-value {
          height: 100%;
          background-color: #2196F3;
        }
      }
    }

    .trend {
      display: flex;
      align-items: center;
      font-size: 0.9rem;

      i {
        margin-right: 4px;
      }

      &.positive {
        color: #4CAF50;
      }

      &.negative {
        color: #F44336;
      }
    }
  }
}

.metrics-checkboxes {
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
