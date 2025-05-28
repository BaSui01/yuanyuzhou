import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态
const users = ref([])
const selectedUsers = ref([])
const userDialog = ref(false)
const deleteUserDialog = ref(false)
const deleteUsersDialog = ref(false)
const loading = ref(true)
const editingUser = ref({
  id: null,
  name: '',
  email: '',
  password: '',
  role: '',
  status: 'active'
})

// 筛选条件
const filters = ref({
  search: '',
  role: null,
  status: null
})

const tableFilters = ref({})

// 选项
const roleOptions = [
  { label: '管理员', value: 'admin' },
  { label: '用户', value: 'user' },
  { label: 'VIP用户', value: 'vip' },
  { label: '内容创作者', value: 'creator' }
]

const statusOptions = [
  { label: '活跃', value: 'active' },
  { label: '待验证', value: 'pending' },
  { label: '已禁用', value: 'disabled' },
  { label: '已封禁', value: 'banned' }
]

// 方法
const loadUsers = async () => {
  loading.value = true

  try {
    // 模拟API请求
    setTimeout(() => {
      users.value = [
        {
          id: 1,
          name: '张小明',
          email: 'zhang@example.com',
          avatar: '/avatars/user1.jpg',
          role: 'admin',
          status: 'active',
          lastLogin: '2023-05-28 14:30',
          createdAt: '2023-01-15'
        },
        {
          id: 2,
          name: '李小华',
          email: 'li@example.com',
          avatar: '/avatars/user2.jpg',
          role: 'user',
          status: 'active',
          lastLogin: '2023-05-27 09:15',
          createdAt: '2023-02-20'
        },
        {
          id: 3,
          name: '王大力',
          email: 'wang@example.com',
          avatar: '/avatars/user3.jpg',
          role: 'vip',
          status: 'active',
          lastLogin: '2023-05-25 18:45',
          createdAt: '2023-03-10'
        },
        {
          id: 4,
          name: '赵小红',
          email: 'zhao@example.com',
          avatar: '/avatars/user4.jpg',
          role: 'creator',
          status: 'pending',
          lastLogin: '2023-05-20 11:30',
          createdAt: '2023-04-05'
        },
        {
          id: 5,
          name: '刘星星',
          email: 'liu@example.com',
          avatar: '/avatars/user5.jpg',
          role: 'user',
          status: 'disabled',
          lastLogin: '2023-05-15 16:20',
          createdAt: '2023-04-12'
        }
      ]
      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('加载用户数据失败:', error)
    loading.value = false
  }
}

const getRoleSeverity = (role) => {
  switch (role) {
    case 'admin':
      return 'danger'
    case 'vip':
      return 'warning'
    case 'creator':
      return 'info'
    default:
      return 'success'
  }
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'active':
      return 'success'
    case 'pending':
      return 'warning'
    case 'disabled':
      return 'info'
    case 'banned':
      return 'danger'
    default:
      return null
  }
}

const openNewUserDialog = () => {
  editingUser.value = {
    id: null,
    name: '',
    email: '',
    password: '',
    role: 'user',
    status: 'active'
  }
  userDialog.value = true
}

const editUser = (user) => {
  editingUser.value = { ...user }
  delete editingUser.value.password // 编辑时不显示密码
  userDialog.value = true
}

const hideDialog = () => {
  userDialog.value = false
}

const saveUser = () => {
  // 模拟保存用户
  if (editingUser.value.id) {
    // 更新现有用户
    const index = users.value.findIndex(u => u.id === editingUser.value.id)
    if (index !== -1) {
      users.value[index] = { ...users.value[index], ...editingUser.value }
    }
  } else {
    // 添加新用户
    editingUser.value.id = users.value.length + 1
    editingUser.value.avatar = '/avatars/default.jpg'
    editingUser.value.lastLogin = '-'
    editingUser.value.createdAt = new Date().toISOString().split('T')[0]
    users.value.push({ ...editingUser.value })
  }

  userDialog.value = false
}

const confirmDeleteUser = (user) => {
  editingUser.value = user
  deleteUserDialog.value = true
}

const deleteUser = () => {
  users.value = users.value.filter(u => u.id !== editingUser.value.id)
  deleteUserDialog.value = false
  editingUser.value = {}
}

const confirmDeleteSelected = () => {
  deleteUsersDialog.value = true
}

const deleteSelectedUsers = () => {
  users.value = users.value.filter(u => !selectedUsers.value.includes(u))
  deleteUsersDialog.value = false
  selectedUsers.value = []
}

const exportUserData = () => {
  // 模拟导出功能
  console.log('导出所有用户数据')
}

const exportSelected = () => {
  // 模拟导出选中用户
  console.log('导出选中用户数据:', selectedUsers.value)
}

const clearSelection = () => {
  selectedUsers.value = []
}

const viewUserDetails = (user) => {
  router.push({ name: 'AdminUserDetail', params: { id: user.id } })
}

const resetFilters = () => {
  filters.value = {
    search: '',
    role: null,
    status: null
  }
}

const applyFilters = () => {
  // 在实际应用中，这里应该调用API进行筛选
  // 这里简单模拟前端筛选
  tableFilters.value = {}

  if (filters.value.search) {
    tableFilters.value['global'] = { value: filters.value.search, matchMode: 'contains' }
  }

  if (filters.value.role) {
    tableFilters.value['role'] = { value: filters.value.role, matchMode: 'equals' }
  }

  if (filters.value.status) {
    tableFilters.value['status'] = { value: filters.value.status, matchMode: 'equals' }
  }
}

// 生命周期钩子
onMounted(() => {
  loadUsers()
})
