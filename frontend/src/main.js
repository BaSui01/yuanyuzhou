import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from '@/modules/navigation'

// 导入模块
import AdminModule from '@/modules/features/admin'

// 导入样式
import 'primevue/resources/themes/lara-dark-teal/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import './assets/styles/main.scss'

// 导入PrimeVue组件
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'
import Dropdown from 'primevue/dropdown'
import Menu from 'primevue/menu'
import Calendar from 'primevue/calendar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'
import Sidebar from 'primevue/sidebar'
import Dialog from 'primevue/dialog'
import Avatar from 'primevue/avatar'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Slider from 'primevue/slider'
import Tooltip from 'primevue/tooltip'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'

// 导入模拟服务（开发环境）
/*
if (import.meta.env.DEV) {
  import('./mocks/browser').then(({ worker }) => {
    worker.start({
      onUnhandledRequest: 'bypass',
    })
    console.log('模拟API服务已启动')
  })
}
*/

// 创建应用实例
const app = createApp(App)

// 注册插件
app.use(createPinia())
app.use(router)
app.use(PrimeVue, { ripple: true })
app.use(ToastService)
app.use(AdminModule)  // 注册管理后台模块

// 注册全局指令
app.directive('scroll-reveal', {
  mounted: (el, binding) => {
    const options = binding.value || {};
    const delay = options.delay || 0;
    const duration = options.duration || 800;

    // 设置初始状态
    el.style.opacity = '0';
    el.style.transform = options.transform || 'translateY(20px)';
    el.style.transition = `opacity ${duration}ms ease-out, transform ${duration}ms ease-out`;

    // 创建观察者
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
          }, delay);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.1 });

    observer.observe(el);
  }
});

// 注册全局组件
app.component('Button', Button)
app.component('InputText', InputText)
app.component('Password', Password)
app.component('Checkbox', Checkbox)
app.component('Dropdown', Dropdown)
app.component('Menu', Menu)
app.component('Calendar', Calendar)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ProgressSpinner', ProgressSpinner)
app.component('Sidebar', Sidebar)
app.component('Dialog', Dialog)
app.component('Avatar', Avatar)
app.component('Tag', Tag)
app.component('Textarea', Textarea)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Slider', Slider)
app.component('Toast', Toast)

// 注册指令
app.directive('tooltip', Tooltip)

// 挂载应用
app.mount('#app')
