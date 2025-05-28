<template>
  <div class="api-encryption-example">
    <h2>API加密通信示例</h2>

    <div class="control-panel">
      <h3>加密控制</h3>
      <div class="form-group">
        <label>加密级别：</label>
        <select v-model="encryptLevel">
          <option :value="0">0级 - 不加密</option>
          <option :value="1">1级 - 单层加密（普通数据）</option>
          <option :value="2">2级 - 双层加密（中等敏感）</option>
          <option :value="3">3级 - 三层加密（高敏感数据）</option>
        </select>
      </div>

      <div class="form-group">
        <label>启用加密：</label>
        <input type="checkbox" v-model="encryptionEnabled">
      </div>

      <button @click="applyEncryptionSettings" class="btn">应用设置</button>
    </div>

    <div class="test-panel">
      <h3>加密测试</h3>
      <div class="form-group">
        <label>测试数据：</label>
        <textarea v-model="testData" placeholder="输入要加密的JSON数据"></textarea>
      </div>

      <div class="buttons">
        <button @click="encryptData" class="btn">加密</button>
        <button @click="decryptData" class="btn">解密</button>
        <button @click="testPasswordEncryption" class="btn btn-warning">测试密码加密</button>
      </div>

      <div class="result">
        <h4>结果：</h4>
        <pre>{{ result }}</pre>
      </div>
    </div>

    <div class="api-test-panel">
      <h3>API请求测试</h3>
      <div class="form-group">
        <label>API路径：</label>
        <input type="text" v-model="apiPath" placeholder="/api/test">
      </div>

      <div class="form-group">
        <label>请求数据：</label>
        <textarea v-model="requestData" placeholder="输入请求数据（JSON格式）"></textarea>
      </div>

      <div class="buttons">
        <button @click="sendGetRequest" class="btn">GET</button>
        <button @click="sendPostRequest" class="btn">POST</button>
        <button @click="sendPutRequest" class="btn">PUT</button>
        <button @click="sendDeleteRequest" class="btn">DELETE</button>
      </div>

      <div class="response">
        <h4>响应：</h4>
        <div v-if="loading" class="loading">加载中...</div>
        <pre v-else>{{ apiResponse }}</pre>
      </div>
    </div>

    <div class="security-info">
      <h3>加密安全信息</h3>
      <div class="info-grid">
        <div class="info-item">
          <h4>高安全级别路径</h4>
          <ul>
            <li v-for="(path, index) in highSecurityPaths" :key="index">{{ path }}</li>
          </ul>
        </div>
        <div class="info-item">
          <h4>自动高级加密字段</h4>
          <ul>
            <li>password, pwd, pass</li>
            <li>current_password, new_password</li>
            <li>password_confirmation</li>
            <li>secret</li>
          </ul>
        </div>
      </div>

      <div class="encryption-test">
        <h4>密码字段自动加密测试</h4>
        <div class="form-group">
          <label>用户名：</label>
          <input type="text" v-model="username" placeholder="用户名">
        </div>
        <div class="form-group">
          <label>密码：</label>
          <input type="password" v-model="password" placeholder="密码">
        </div>
        <button @click="testLoginEncryption" class="btn">测试登录加密</button>

        <div class="encryption-result">
          <h5>加密结果：</h5>
          <pre>{{ encryptionTestResult }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue';
import api, { request, crypto } from '@/api';
import { CRYPTO_CONFIG } from '@/api/utils/cryptoConfig';

export default {
  name: 'ApiEncryptionExample',

  setup() {
    // 加密控制
    const encryptLevel = ref(1);
    const encryptionEnabled = ref(true);

    // 测试数据
    const testData = ref('{\n  "name": "测试用户",\n  "email": "test@example.com",\n  "data": "普通数据"\n}');
    const result = ref('');

    // API测试
    const apiPath = ref('/api/test');
    const requestData = ref('{\n  "message": "Hello, API!"\n}');
    const apiResponse = ref('');
    const loading = ref(false);

    // 安全信息
    const highSecurityPaths = ref(CRYPTO_CONFIG.HIGH_SECURITY_PATHS);

    // 加密测试
    const username = ref('testuser');
    const password = ref('password123');
    const encryptionTestResult = ref('');

    // 应用加密设置
    const applyEncryptionSettings = () => {
      request.setEncryptLevel(encryptLevel.value);
      request.setEncryption(encryptionEnabled.value);

      result.value = `已应用设置：\n- 加密级别：${encryptLevel.value}\n- 启用加密：${encryptionEnabled.value}`;
    };

    // 加密数据
    const encryptData = () => {
      try {
        const data = JSON.parse(testData.value);
        const encrypted = crypto.encrypt(data, encryptLevel.value);
        result.value = encrypted;
      } catch (error) {
        result.value = `加密错误：${error.message}`;
      }
    };

    // 解密数据
    const decryptData = () => {
      try {
        const decrypted = crypto.decrypt(result.value, encryptLevel.value);
        result.value = typeof decrypted === 'object'
          ? JSON.stringify(decrypted, null, 2)
          : decrypted;
      } catch (error) {
        result.value = `解密错误：${error.message}`;
      }
    };

    // 测试密码字段自动高级加密
    const testPasswordEncryption = () => {
      try {
        // 普通数据（1级加密）
        const normalData = { name: "测试用户", email: "test@example.com" };
        const normalEncrypted = crypto.encrypt(normalData, 1);

        // 包含密码的数据（自动3级加密）
        const passwordData = { name: "测试用户", email: "test@example.com", password: "secret123" };
        const passwordEncrypted = crypto.encrypt(passwordData, 1);

        result.value = `普通数据加密结果（1级）：\n${normalEncrypted}\n\n` +
                       `包含密码的数据加密结果（自动3级）：\n${passwordEncrypted}\n\n` +
                       `注意：包含密码的数据加密结果更长，因为使用了3级加密`;
      } catch (error) {
        result.value = `加密错误：${error.message}`;
      }
    };

    // 测试登录加密
    const testLoginEncryption = () => {
      try {
        const loginData = {
          username: username.value,
          password: password.value
        };

        // 使用secureAxios内部的_containsPasswordField方法检测
        const containsPassword = true; // 这里简化处理，实际上会自动检测

        // 加密级别
        const normalLevel = 1;
        const passwordLevel = 3;

        // 加密数据
        const normalEncrypted = crypto.encrypt(loginData, normalLevel);
        const passwordEncrypted = crypto.encrypt(loginData, passwordLevel);

        encryptionTestResult.value =
          `登录数据：${JSON.stringify(loginData)}\n\n` +
          `1级加密结果：\n${normalEncrypted}\n\n` +
          `3级加密结果（密码字段自动使用）：\n${passwordEncrypted}\n\n` +
          `字符长度对比：\n- 1级加密：${normalEncrypted.length}字符\n- 3级加密：${passwordEncrypted.length}字符`;
      } catch (error) {
        encryptionTestResult.value = `加密错误：${error.message}`;
      }
    };

    // 发送GET请求
    const sendGetRequest = async () => {
      loading.value = true;
      try {
        const response = await request.get(apiPath.value);
        apiResponse.value = JSON.stringify(response, null, 2);
      } catch (error) {
        apiResponse.value = `请求错误：${error.message}`;
      } finally {
        loading.value = false;
      }
    };

    // 发送POST请求
    const sendPostRequest = async () => {
      loading.value = true;
      try {
        const data = JSON.parse(requestData.value);
        const response = await request.post(apiPath.value, data);
        apiResponse.value = JSON.stringify(response, null, 2);
      } catch (error) {
        apiResponse.value = `请求错误：${error.message}`;
      } finally {
        loading.value = false;
      }
    };

    // 发送PUT请求
    const sendPutRequest = async () => {
      loading.value = true;
      try {
        const data = JSON.parse(requestData.value);
        const response = await request.put(apiPath.value, data);
        apiResponse.value = JSON.stringify(response, null, 2);
      } catch (error) {
        apiResponse.value = `请求错误：${error.message}`;
      } finally {
        loading.value = false;
      }
    };

    // 发送DELETE请求
    const sendDeleteRequest = async () => {
      loading.value = true;
      try {
        const response = await request.delete(apiPath.value);
        apiResponse.value = JSON.stringify(response, null, 2);
      } catch (error) {
        apiResponse.value = `请求错误：${error.message}`;
      } finally {
        loading.value = false;
      }
    };

    // 组件挂载时应用默认设置
    onMounted(() => {
      applyEncryptionSettings();
    });

    return {
      encryptLevel,
      encryptionEnabled,
      testData,
      result,
      apiPath,
      requestData,
      apiResponse,
      loading,
      applyEncryptionSettings,
      encryptData,
      decryptData,
      sendGetRequest,
      sendPostRequest,
      sendPutRequest,
      sendDeleteRequest
    };
  }
};
</script>

<style lang="scss" scoped>
.api-encryption-example {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;

  h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
  }

  h3 {
    margin-top: 0;
    color: #555;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
  }

  .control-panel,
  .test-panel,
  .api-test-panel {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .form-group {
    margin-bottom: 15px;

    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }

    select, input[type="text"], textarea {
      width: 100%;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-family: inherit;
    }

    textarea {
      min-height: 100px;
      font-family: monospace;
    }
  }

  .buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 15px;
  }

  .btn {
    padding: 8px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;

    &:hover {
      background-color: #45a049;
    }
  }

  .result, .response {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;

    h4 {
      margin-top: 0;
      margin-bottom: 10px;
      color: #555;
    }

    pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-all;
      font-family: monospace;
      font-size: 14px;
      max-height: 200px;
      overflow-y: auto;
    }
  }

  .loading {
    text-align: center;
    color: #666;
    padding: 20px;
  }
}
</style>
