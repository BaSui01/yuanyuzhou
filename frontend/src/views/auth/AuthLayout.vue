<template>
  <div class="auth-layout">
    <!-- 3D 背景画布 -->
    <canvas ref="babylonCanvas" class="babylon-canvas"></canvas>

    <!-- 认证内容区域 -->
    <main class="auth-main">
      <router-view />

      <!-- 版权信息 -->
      <footer class="auth-copyright">
        <p>&copy; {{ currentYear }} 元宇宙社交空间. 保留所有权利.</p>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as BABYLON from '@babylonjs/core'
import '@babylonjs/loaders'

const currentYear = computed(() => new Date().getFullYear())
const babylonCanvas = ref(null)

let engine, scene, camera, animationId

// 初始化 Babylon.js 3D 背景
const initBabylonBackground = () => {
  // 创建引擎和场景
  engine = new BABYLON.Engine(babylonCanvas.value, true, { preserveDrawingBuffer: true, stencil: true })
  scene = new BABYLON.Scene(engine)
  scene.clearColor = new BABYLON.Color4(0.05, 0.05, 0.1, 1)

  // 创建相机
  camera = new BABYLON.ArcRotateCamera(
    'camera',
    -Math.PI / 2,
    Math.PI / 2.5,
    15,
    new BABYLON.Vector3(0, 0, 0),
    scene
  )
  camera.lowerRadiusLimit = 10
  camera.upperRadiusLimit = 20
  camera.wheelDeltaPercentage = 0.01
  camera.minZ = 0.1

  // 禁用相机控制，使其只作为观赏视角
  camera.inputs.clear()

  // 添加光源
  const hemiLight = new BABYLON.HemisphericLight('hemiLight', new BABYLON.Vector3(0, 1, 0), scene)
  hemiLight.intensity = 0.5
  hemiLight.diffuse = new BABYLON.Color3(0.6, 0.5, 1)
  hemiLight.groundColor = new BABYLON.Color3(0.3, 0.2, 0.5)

  // 添加点光源
  const pointLight = new BABYLON.PointLight('pointLight', new BABYLON.Vector3(5, 5, -5), scene)
  pointLight.intensity = 0.7
  pointLight.diffuse = new BABYLON.Color3(0.8, 0.5, 1)

  // 创建粒子系统
  createParticleSystem()

  // 创建几何体
  createGeometries()

  // 添加后处理效果
  addPostProcessing()

  // 启动渲染循环
  engine.runRenderLoop(() => {
    scene.render()

    // 轻微旋转相机，创造动态效果
    camera.alpha += 0.0005

    // 根据时间变化调整相机高度，创造轻微起伏
    camera.beta = Math.PI / 2.5 + Math.sin(Date.now() * 0.0002) * 0.05
  })

  // 处理窗口大小调整
  window.addEventListener('resize', handleResize)
}

// 创建粒子系统
const createParticleSystem = () => {
  // 创建粒子系统
  const particleSystem = new BABYLON.ParticleSystem('particles', 2000, scene)

  // 设置粒子纹理
  particleSystem.particleTexture = new BABYLON.Texture('/assets/textures/particle.png', scene)

  // 粒子发射器设置
  particleSystem.emitter = new BABYLON.Vector3(0, 0, 0)
  particleSystem.minEmitBox = new BABYLON.Vector3(-10, -10, -10)
  particleSystem.maxEmitBox = new BABYLON.Vector3(10, 10, 10)

  // 粒子颜色
  particleSystem.color1 = new BABYLON.Color4(0.7, 0.5, 1.0, 1.0)
  particleSystem.color2 = new BABYLON.Color4(0.5, 0.7, 1.0, 1.0)
  particleSystem.colorDead = new BABYLON.Color4(0, 0, 0.2, 0.0)

  // 粒子大小
  particleSystem.minSize = 0.1
  particleSystem.maxSize = 0.2

  // 粒子生命周期
  particleSystem.minLifeTime = 8.0
  particleSystem.maxLifeTime = 10.0

  // 发射速率
  particleSystem.emitRate = 100

  // 混合模式
  particleSystem.blendMode = BABYLON.ParticleSystem.BLENDMODE_ADD

  // 重力
  particleSystem.gravity = new BABYLON.Vector3(0, 0, 0)

  // 方向
  particleSystem.direction1 = new BABYLON.Vector3(-0.5, -0.5, -0.5)
  particleSystem.direction2 = new BABYLON.Vector3(0.5, 0.5, 0.5)

  // 角速度
  particleSystem.minAngularSpeed = 0
  particleSystem.maxAngularSpeed = Math.PI

  // 速度
  particleSystem.minEmitPower = 0.5
  particleSystem.maxEmitPower = 1.5
  particleSystem.updateSpeed = 0.005

  // 启动粒子系统
  particleSystem.start()
}

// 创建几何体
const createGeometries = () => {
  // 创建多面几何体
  const polyhedron = BABYLON.MeshBuilder.CreatePolyhedron('polyhedron', {
    type: 3,
    size: 2.5
  }, scene)

  polyhedron.position = new BABYLON.Vector3(-5, 0, 0)

  // 创建几何体材质
  const polyMaterial = new BABYLON.StandardMaterial('polyMaterial', scene)
  polyMaterial.diffuseColor = new BABYLON.Color3(0.6, 0.4, 1)
  polyMaterial.specularColor = new BABYLON.Color3(0.2, 0.2, 0.8)
  polyMaterial.emissiveColor = new BABYLON.Color3(0.2, 0.1, 0.4)
  polyMaterial.alpha = 0.8
  polyMaterial.wireframe = true

  polyhedron.material = polyMaterial

  // 添加旋转动画
  scene.registerBeforeRender(() => {
    polyhedron.rotation.y += 0.005
    polyhedron.rotation.x += 0.003
  })

  // 创建环面结
  const torus = BABYLON.MeshBuilder.CreateTorus('torus', {
    diameter: 5,
    thickness: 0.5,
    tessellation: 32
  }, scene)

  torus.position = new BABYLON.Vector3(5, 0, 0)

  // 创建环面材质
  const torusMaterial = new BABYLON.StandardMaterial('torusMaterial', scene)
  torusMaterial.diffuseColor = new BABYLON.Color3(0.4, 0.6, 1)
  torusMaterial.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.5)
  torusMaterial.alpha = 0.6
  torusMaterial.wireframe = true

  torus.material = torusMaterial

  // 添加旋转动画
  scene.registerBeforeRender(() => {
    torus.rotation.x += 0.002
    torus.rotation.z += 0.004
  })

  // 创建球体背景
  const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {
    diameter: 30,
    segments: 32
  }, scene)

  // 创建球体材质
  const sphereMaterial = new BABYLON.StandardMaterial('sphereMaterial', scene)
  sphereMaterial.diffuseColor = new BABYLON.Color3(0.2, 0.2, 0.4)
  sphereMaterial.emissiveColor = new BABYLON.Color3(0.05, 0.05, 0.1)
  sphereMaterial.alpha = 0.1
  sphereMaterial.wireframe = true
  sphereMaterial.backFaceCulling = false

  sphere.material = sphereMaterial

  // 添加缓慢旋转
  scene.registerBeforeRender(() => {
    sphere.rotation.y += 0.0003
  })
}

// 添加后处理效果
const addPostProcessing = () => {
  // 添加景深效果
  const depthOfField = new BABYLON.DepthOfFieldPostProcess(
    'depthOfField',
    1.0,
    camera,
    null,
    undefined,
    undefined,
    undefined,
    engine
  )
  depthOfField.focalLength = 150
  depthOfField.fStop = 1.4
  depthOfField.focusDistance = 2000

  // 添加辉光效果
  const defaultPipeline = new BABYLON.DefaultRenderingPipeline(
    'defaultPipeline',
    true,
    scene,
    [camera]
  )

  defaultPipeline.bloomEnabled = true
  defaultPipeline.bloomThreshold = 0.2
  defaultPipeline.bloomWeight = 0.5
  defaultPipeline.bloomKernel = 64
  defaultPipeline.bloomScale = 0.5

  // 添加色彩校正
  defaultPipeline.imageProcessing.contrast = 1.1
  defaultPipeline.imageProcessing.exposure = 1.1
  defaultPipeline.imageProcessing.toneMappingEnabled = true

  // 添加色差效果
  defaultPipeline.chromaticAberrationEnabled = true
  defaultPipeline.chromaticAberration.aberrationAmount = 1
  defaultPipeline.chromaticAberration.radialIntensity = 0.5
}

// 处理窗口大小调整
const handleResize = () => {
  if (engine) {
    engine.resize()
  }
}

// 清理 Babylon.js 资源
const cleanup = () => {
  if (engine) {
    window.removeEventListener('resize', handleResize)
    scene.dispose()
    engine.dispose()
  }
}

onMounted(() => {
  initBabylonBackground()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style lang="scss">
.auth-layout {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #1a103d 0%, #2c1a5a 100%);

  .babylon-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    touch-action: none;
    outline: none;
  }

  .auth-main {
    position: relative;
    z-index: 2;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: clamp(1rem, 5vw, 2rem);

    .auth-copyright {
      position: fixed;
      bottom: 1rem;
      left: 50%;
      transform: translateX(-50%);
      text-align: center;
      z-index: 3;

      p {
        color: rgba(255, 255, 255, 0.7);
        font-size: clamp(0.75rem, 2vw, 0.875rem);
        margin: 0;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;

        &:hover {
          background: rgba(255, 255, 255, 0.15);
          border-color: rgba(255, 255, 255, 0.3);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
      }
    }
  }

  @media (max-width: 768px) {
    .auth-main {
      padding: 1rem;
    }

    .auth-copyright {
      position: relative;
      bottom: auto;
      left: auto;
      transform: none;
      margin-top: 2rem;
    }
  }
}
</style>
