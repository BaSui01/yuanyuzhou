<template>
  <div class="loading-spinner" :class="[`size-${size}`, `variant-${variant}`]">
    <div v-if="variant === 'default'" class="spinner-default">
      <div class="spinner-ring"></div>
    </div>

    <div v-else-if="variant === 'dots'" class="spinner-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>

    <div v-else-if="variant === 'orbit'" class="spinner-orbit">
      <div class="orbit-center"></div>
      <div class="orbit-ring"></div>
    </div>

    <!-- 加载文本 -->
    <div v-if="text" class="loading-text">{{ text }}</div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'dots', 'orbit'].includes(value)
  },
  text: {
    type: String,
    default: ''
  }
});
</script>

<style scoped>
.loading-spinner {
  --primary-color: #4DBA87;
  --secondary-color: #42b983;
  --text-color-secondary: #64748b;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

/* 尺寸变体 */
.loading-spinner.size-xs { --spinner-size: 16px; --text-size: 0.75rem; }
.loading-spinner.size-sm { --spinner-size: 24px; --text-size: 0.875rem; }
.loading-spinner.size-md { --spinner-size: 32px; --text-size: 1rem; }
.loading-spinner.size-lg { --spinner-size: 48px; --text-size: 1.25rem; }
.loading-spinner.size-xl { --spinner-size: 64px; --text-size: 1.5rem; }

.loading-text {
  font-size: var(--text-size);
  color: var(--text-color-secondary);
  font-weight: 500;
}

/* 默认加载器 */
.spinner-default {
  position: relative;
  width: var(--spinner-size);
  height: var(--spinner-size);
}

.spinner-ring {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top: 2px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 点状加载器 */
.spinner-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
}

.dot {
  width: calc(var(--spinner-size) / 4);
  height: calc(var(--spinner-size) / 4);
  background-color: var(--primary-color);
  border-radius: 50%;
  animation: dot-bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
.dot:nth-child(3) { animation-delay: 0s; }

/* 轨道加载器 */
.spinner-orbit {
  position: relative;
  width: var(--spinner-size);
  height: var(--spinner-size);
}

.orbit-center {
  position: absolute;
  width: 30%;
  height: 30%;
  background-color: var(--primary-color);
  border-radius: 50%;
  top: 35%;
  left: 35%;
}

.orbit-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(77, 186, 135, 0.2);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
