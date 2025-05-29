import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@views': resolve(__dirname, 'src/views'),
      '@stores': resolve(__dirname, 'src/stores'),
      '@composables': resolve(__dirname, 'src/composables'),
      '@styles': resolve(__dirname, 'src/assets/styles'),
      '@assets': resolve(__dirname, 'src/assets'),
      '@modules': resolve(__dirname, 'src/modules'),

    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@styles/_variables.scss" as *;`,
        api: 'modern-compiler' // 使用现代 Sass 编译器
      }
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    open: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    }
  },
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'axios',
      'three',
      'gsap',
      'crypto-js',
      'primevue/config',
      'primevue/button',
      'primevue/inputtext',
      'primevue/toast',
      'primevue/progressbar',
      'primevue/dialog',
      'primevue/sidebar',
      'primevue/dropdown',
      'primevue/slider',
      'primevue/checkbox',
      'primevue/avatar',
      'primevue/tooltip'
    ]
  }
})
