import { ref, onUnmounted } from 'vue'
import * as THREE from 'three'

export function useThreeBackground() {
  const scene = ref(null)
  const camera = ref(null)
  const renderer = ref(null)
  const animationId = ref(null)
  const particles = ref([])
  const mouseX = ref(0)
  const mouseY = ref(0)

  // 初始化Three.js场景
  const initThreeBackground = async (containerId) => {
    try {
      const container = document.getElementById(containerId)
      if (!container) {
        console.error('Three.js容器元素未找到')
        return
      }

      // 创建场景
      scene.value = new THREE.Scene()

      // 创建相机
      camera.value = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      )
      camera.value.position.z = 30

      // 创建渲染器
      renderer.value = new THREE.WebGLRenderer({
        alpha: true,
        antialias: true
      })
      renderer.value.setSize(window.innerWidth, window.innerHeight)
      renderer.value.setClearColor(0x000000, 0)
      container.appendChild(renderer.value.domElement)

      // 创建粒子系统
      createParticleSystem()

      // 创建几何体
      createFloatingGeometry()

      // 添加光源
      addLights()

      // 启动动画循环
      animate()

      // 添加事件监听器
      addEventListeners()

      console.log('Three.js 3D背景初始化成功')
    } catch (error) {
      console.error('Three.js初始化失败:', error)
    }
  }

  // 创建粒子系统
  const createParticleSystem = () => {
    const particleCount = 500
    const positions = new Float32Array(particleCount * 3)
    const colors = new Float32Array(particleCount * 3)

    for (let i = 0; i < particleCount; i++) {
      // 位置
      positions[i * 3] = (Math.random() - 0.5) * 100
      positions[i * 3 + 1] = (Math.random() - 0.5) * 100
      positions[i * 3 + 2] = (Math.random() - 0.5) * 100

      // 颜色 - 使用青色和紫色主题
      const colorPalette = [
        new THREE.Color(0x06b6d4), // 青色
        new THREE.Color(0x3b82f6), // 蓝色
        new THREE.Color(0x8b5cf6), // 紫色
        new THREE.Color(0xec4899)  // 粉色
      ]
      const color = colorPalette[Math.floor(Math.random() * colorPalette.length)]
      colors[i * 3] = color.r
      colors[i * 3 + 1] = color.g
      colors[i * 3 + 2] = color.b
    }

    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))

    const material = new THREE.PointsMaterial({
      size: 2,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    })

    const particleSystem = new THREE.Points(geometry, material)
    scene.value.add(particleSystem)
    particles.value.push(particleSystem)
  }

  // 创建浮动几何体
  const createFloatingGeometry = () => {
    // 创建多个几何体
    const geometries = [
      new THREE.TorusGeometry(3, 1, 8, 16),
      new THREE.OctahedronGeometry(2),
      new THREE.TetrahedronGeometry(2.5),
      new THREE.IcosahedronGeometry(2)
    ]

    geometries.forEach((geometry, index) => {
      const material = new THREE.MeshPhongMaterial({
        color: [0x06b6d4, 0x8b5cf6, 0xec4899, 0x3b82f6][index],
        transparent: true,
        opacity: 0.3,
        wireframe: true
      })

      const mesh = new THREE.Mesh(geometry, material)

      // 随机位置
      mesh.position.x = (Math.random() - 0.5) * 60
      mesh.position.y = (Math.random() - 0.5) * 60
      mesh.position.z = (Math.random() - 0.5) * 60

      // 随机旋转
      mesh.rotation.x = Math.random() * Math.PI
      mesh.rotation.y = Math.random() * Math.PI

      scene.value.add(mesh)
      particles.value.push(mesh)
    })
  }

  // 添加光源
  const addLights = () => {
    // 环境光
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6)
    scene.value.add(ambientLight)

    // 点光源
    const pointLight1 = new THREE.PointLight(0x06b6d4, 1, 100)
    pointLight1.position.set(20, 20, 20)
    scene.value.add(pointLight1)

    const pointLight2 = new THREE.PointLight(0x8b5cf6, 1, 100)
    pointLight2.position.set(-20, -20, 20)
    scene.value.add(pointLight2)

    const pointLight3 = new THREE.PointLight(0xec4899, 1, 100)
    pointLight3.position.set(20, -20, -20)
    scene.value.add(pointLight3)
  }

  // 动画循环
  const animate = () => {
    animationId.value = requestAnimationFrame(animate)

    if (!scene.value || !camera.value || !renderer.value) return

    // 旋转粒子系统
    particles.value.forEach((particle, index) => {
      if (particle.type === 'Points') {
        particle.rotation.y += 0.002
        particle.rotation.x += 0.001
      } else {
        // 几何体动画
        particle.rotation.x += 0.01 * (index + 1)
        particle.rotation.y += 0.008 * (index + 1)

        // 浮动效果
        particle.position.y += Math.sin(Date.now() * 0.001 + index) * 0.02
      }
    })

    // 相机跟随鼠标
    camera.value.position.x += (mouseX.value * 0.05 - camera.value.position.x) * 0.05
    camera.value.position.y += (-mouseY.value * 0.05 - camera.value.position.y) * 0.05
    camera.value.lookAt(scene.value.position)

    // 渲染场景
    renderer.value.render(scene.value, camera.value)
  }

  // 添加事件监听器
  const addEventListeners = () => {
    // 窗口大小变化
    const handleResize = () => {
      if (!camera.value || !renderer.value) return

      camera.value.aspect = window.innerWidth / window.innerHeight
      camera.value.updateProjectionMatrix()
      renderer.value.setSize(window.innerWidth, window.innerHeight)
    }

    // 鼠标移动
    const handleMouseMove = (event) => {
      mouseX.value = (event.clientX - window.innerWidth / 2) / window.innerWidth
      mouseY.value = (event.clientY - window.innerHeight / 2) / window.innerHeight
    }

    window.addEventListener('resize', handleResize)
    window.addEventListener('mousemove', handleMouseMove)

    // 保存清理函数
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('mousemove', handleMouseMove)
    })
  }

  // 创建星空背景
  const createStarField = () => {
    const starCount = 1000
    const positions = new Float32Array(starCount * 3)

    for (let i = 0; i < starCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 200
      positions[i * 3 + 1] = (Math.random() - 0.5) * 200
      positions[i * 3 + 2] = (Math.random() - 0.5) * 200
    }

    const geometry = new THREE.BufferGeometry()
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))

    const material = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 1,
      transparent: true,
      opacity: 0.6
    })

    const stars = new THREE.Points(geometry, material)
    scene.value.add(stars)
    return stars
  }

  // 添加发光效果
  const addGlowEffect = () => {
    if (!renderer.value) return

    // 创建后期处理效果
    const composer = new THREE.EffectComposer(renderer.value)

    // 这里可以添加更多后期处理效果
    // 例如：辉光效果、景深效果等
  }

  // 创建动态波浪
  const createWaveEffect = () => {
    const waveGeometry = new THREE.PlaneGeometry(50, 50, 32, 32)
    const waveMaterial = new THREE.MeshPhongMaterial({
      color: 0x06b6d4,
      transparent: true,
      opacity: 0.1,
      wireframe: true,
      side: THREE.DoubleSide
    })

    const wave = new THREE.Mesh(waveGeometry, waveMaterial)
    wave.rotation.x = -Math.PI / 2
    wave.position.y = -10

    // 添加波浪动画
    const vertices = waveGeometry.attributes.position.array
    const originalPositions = [...vertices]

    const animateWave = () => {
      for (let i = 0; i < vertices.length; i += 3) {
        const x = originalPositions[i]
        const y = originalPositions[i + 1]
        vertices[i + 2] = Math.sin(x * 0.1 + Date.now() * 0.002) *
                          Math.cos(y * 0.1 + Date.now() * 0.002) * 2
      }
      waveGeometry.attributes.position.needsUpdate = true
    }

    // 将动画函数添加到动画循环中
    const originalAnimate = animate
    animate = () => {
      animateWave()
      originalAnimate()
    }

    scene.value.add(wave)
    return wave
  }

  // 销毁Three.js场景
  const destroyThreeBackground = () => {
    if (animationId.value) {
      cancelAnimationFrame(animationId.value)
      animationId.value = null
    }

    if (renderer.value) {
      renderer.value.dispose()
      if (renderer.value.domElement && renderer.value.domElement.parentNode) {
        renderer.value.domElement.parentNode.removeChild(renderer.value.domElement)
      }
      renderer.value = null
    }

    if (scene.value) {
      // 清理场景中的所有对象
      while (scene.value.children.length > 0) {
        const child = scene.value.children[0]
        if (child.geometry) child.geometry.dispose()
        if (child.material) {
          if (Array.isArray(child.material)) {
            child.material.forEach(material => material.dispose())
          } else {
            child.material.dispose()
          }
        }
        scene.value.remove(child)
      }
      scene.value = null
    }

    camera.value = null
    particles.value = []

    console.log('Three.js 3D背景已销毁')
  }

  // 更新粒子颜色主题
  const updateParticleTheme = (theme) => {
    const colorMaps = {
      cyber: [0x06b6d4, 0x3b82f6, 0x8b5cf6, 0xec4899],
      nature: [0x10b981, 0x059669, 0x065f46, 0x064e3b],
      sunset: [0xf59e0b, 0xd97706, 0xb45309, 0x92400e],
      ocean: [0x0ea5e9, 0x0284c7, 0x0369a1, 0x075985]
    }

    const colors = colorMaps[theme] || colorMaps.cyber

    particles.value.forEach(particle => {
      if (particle.material && particle.material.color) {
        const randomColor = colors[Math.floor(Math.random() * colors.length)]
        particle.material.color.setHex(randomColor)
      }
    })
  }

  return {
    initThreeBackground,
    destroyThreeBackground,
    updateParticleTheme,
    createStarField,
    createWaveEffect,
    addGlowEffect
  }
}
