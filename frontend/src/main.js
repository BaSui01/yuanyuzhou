import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

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

// 创建应用实例
const app = createApp(App)

// 注册插件
app.use(createPinia())
app.use(router)
app.use(PrimeVue, { ripple: true })

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

// 挂载应用
app.mount('#app')
