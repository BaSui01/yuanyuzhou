"""
加密中间件
处理传输层和应用层的加密/解密功能
"""

import json
import time
import logging
from typing import Dict, Any, Optional, Tuple
from django.http import JsonResponse, HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.cache import cache
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import secrets
import base64
import hashlib
import hmac

logger = logging.getLogger(__name__)


class TransportEncryptionConfig:
    """传输层加密配置"""

    # 传输层密钥（应从环境变量获取）
    TRANSPORT_KEY = getattr(settings, 'TRANSPORT_KEY', 'transport-layer-secure-key-2024')

    # 会话密钥生存时间（秒）
    SESSION_KEY_TTL = getattr(settings, 'SESSION_KEY_TTL', 300)  # 5分钟

    # 时间窗口容忍度（秒）
    TIME_WINDOW = getattr(settings, 'TIME_WINDOW', 30)

    # 启用防重放攻击
    ANTI_REPLAY = getattr(settings, 'ANTI_REPLAY', True)

    # 启用完整性校验
    INTEGRITY_CHECK = getattr(settings, 'INTEGRITY_CHECK', True)

    # 压缩阈值（字节）
    COMPRESSION_THRESHOLD = getattr(settings, 'COMPRESSION_THRESHOLD', 1024)

    # RSA密钥长度
    RSA_KEY_SIZE = 2048

    # AES密钥长度
    AES_KEY_SIZE = 32  # 256位


class AdvancedCryptoUtils:
    """高级加密工具类"""

    def __init__(self):
        self.backend = default_backend()
        self.config = TransportEncryptionConfig()

    def generate_rsa_keypair(self) -> Tuple[bytes, bytes]:
        """生成RSA密钥对"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.config.RSA_KEY_SIZE,
            backend=self.backend
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem, public_pem

    def rsa_encrypt(self, data: bytes, public_key_pem: bytes) -> bytes:
        """RSA加密"""
        public_key = serialization.load_pem_public_key(public_key_pem, backend=self.backend)
        encrypted = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def rsa_decrypt(self, encrypted_data: bytes, private_key_pem: bytes) -> bytes:
        """RSA解密"""
        private_key = serialization.load_pem_private_key(
            private_key_pem, password=None, backend=self.backend
        )
        decrypted = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted

    def derive_key(self, password: str, salt: bytes, length: int = 32) -> bytes:
        """使用PBKDF2派生密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())

    def aes_encrypt_gcm(self, data: bytes, key: bytes) -> Dict[str, str]:
        """AES-GCM加密"""
        iv = secrets.token_bytes(12)  # GCM推荐12字节IV
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(data) + encryptor.finalize()

        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }

    def aes_decrypt_gcm(self, encrypted_data: Dict[str, str], key: bytes) -> bytes:
        """AES-GCM解密"""
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['tag'])

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=self.backend)
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext

    def generate_hmac(self, data: bytes, key: bytes) -> str:
        """生成HMAC签名"""
        h = hmac.new(key, data, hashlib.sha256)
        return h.hexdigest()

    def verify_hmac(self, data: bytes, signature: str, key: bytes) -> bool:
        """验证HMAC签名"""
        expected = self.generate_hmac(data, key)
        return hmac.compare_digest(expected, signature)


class TransportEncryptionService:
    """传输层加密服务"""

    def __init__(self):
        self.crypto = AdvancedCryptoUtils()
        self.config = TransportEncryptionConfig()
        self.session_cache_prefix = 'transport_session:'
        self.nonce_cache_prefix = 'transport_nonce:'

    def generate_session_key(self, client_id: str) -> Dict[str, Any]:
        """生成会话密钥"""
        session_id = secrets.token_urlsafe(16)
        salt = secrets.token_bytes(16)

        # 使用PBKDF2派生会话密钥
        key_material = f"{self.config.TRANSPORT_KEY}:{client_id}:{session_id}:{int(time.time())}"
        session_key = self.crypto.derive_key(key_material, salt)

        # 生成服务器RSA密钥对
        server_private_key, server_public_key = self.crypto.generate_rsa_keypair()

        session_info = {
            'session_id': session_id,
            'key': base64.b64encode(session_key).decode(),
            'salt': base64.b64encode(salt).decode(),
            'server_private_key': base64.b64encode(server_private_key).decode(),
            'server_public_key': base64.b64encode(server_public_key).decode(),
            'client_id': client_id,
            'created_at': int(time.time()),
            'expires_at': int(time.time()) + self.config.SESSION_KEY_TTL
        }

        # 缓存会话信息
        cache_key = f"{self.session_cache_prefix}{session_id}"
        cache.set(cache_key, session_info, self.config.SESSION_KEY_TTL)

        # 返回公钥和会话ID给客户端
        return {
            'session_id': session_id,
            'server_public_key': server_public_key.decode(),
            'expires_at': session_info['expires_at'],
            'key_hash': hashlib.sha256(session_key).hexdigest()[:16]
        }

    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取会话信息"""
        cache_key = f"{self.session_cache_prefix}{session_id}"
        session_info = cache.get(cache_key)

        if not session_info:
            return None

        # 检查是否过期
        if int(time.time()) > session_info['expires_at']:
            cache.delete(cache_key)
            return None

        return session_info

    def encrypt_transport(self, payload: Dict[str, Any], session_id: str, sequence: int = 0) -> Dict[str, Any]:
        """传输层数据加密"""
        session_info = self.get_session_info(session_id)
        if not session_info:
            raise ValueError('无效的会话ID或会话已过期')

        # 生成传输包元数据
        timestamp = int(time.time())
        nonce = secrets.token_urlsafe(12)

        # 准备传输数据
        transport_data = {
            'payload': payload,
            'timestamp': timestamp,
            'nonce': nonce,
            'sequence': sequence,
            'version': '2.0'  # 升级版本号
        }

        # 数据压缩（如果需要）
        serialized_data = json.dumps(transport_data, separators=(',', ':'))
        if len(serialized_data) > self.config.COMPRESSION_THRESHOLD:
            import gzip
            compressed_data = gzip.compress(serialized_data.encode())
            transport_data['compressed'] = True
            data_to_encrypt = compressed_data
        else:
            data_to_encrypt = serialized_data.encode()

        # 使用AES-GCM加密
        session_key = base64.b64decode(session_info['key'])
        encrypted_result = self.crypto.aes_encrypt_gcm(data_to_encrypt, session_key)

        # 生成完整性校验
        hmac_data = f"{encrypted_result['ciphertext']}:{encrypted_result['iv']}:{timestamp}:{nonce}".encode()
        hmac_key = hashlib.sha256(session_key + b'hmac').digest()
        hmac_signature = self.crypto.generate_hmac(hmac_data, hmac_key)

        # 构造传输包
        transport_packet = {
            'session_id': session_id,
            'data': encrypted_result['ciphertext'],
            'iv': encrypted_result['iv'],
            'tag': encrypted_result['tag'],
            'timestamp': timestamp,
            'nonce': nonce,
            'sequence': sequence,
            'hmac': hmac_signature,
            'version': '2.0',
            'compressed': transport_data.get('compressed', False)
        }

        logger.info(f"[传输加密] 数据包已加密 - 会话: {session_id[:8]}..., 大小: {len(serialized_data)}")

        return transport_packet

    def decrypt_transport(self, transport_packet: Dict[str, Any]) -> Dict[str, Any]:
        """传输层数据解密"""
        session_id = transport_packet.get('session_id')
        if not session_id:
            raise ValueError('缺少会话ID')

        session_info = self.get_session_info(session_id)
        if not session_info:
            raise ValueError('无效的会话ID或会话已过期')

        # 提取传输包数据
        ciphertext = transport_packet['data']
        iv = transport_packet['iv']
        tag = transport_packet['tag']
        timestamp = transport_packet['timestamp']
        nonce = transport_packet['nonce']
        sequence = transport_packet['sequence']
        hmac_signature = transport_packet['hmac']
        compressed = transport_packet.get('compressed', False)

        # 时间窗口验证
        current_time = int(time.time())
        if abs(current_time - timestamp) > self.config.TIME_WINDOW:
            raise ValueError('传输包时间戳超出允许窗口')

        # 防重放攻击检查
        if self.config.ANTI_REPLAY:
            nonce_key = f"{self.nonce_cache_prefix}{session_id}:{nonce}:{timestamp}"
            if cache.get(nonce_key):
                raise ValueError('检测到重放攻击')
            cache.set(nonce_key, True, self.config.TIME_WINDOW)

        # 完整性校验
        if self.config.INTEGRITY_CHECK:
            session_key = base64.b64decode(session_info['key'])
            hmac_data = f"{ciphertext}:{iv}:{timestamp}:{nonce}".encode()
            hmac_key = hashlib.sha256(session_key + b'hmac').digest()

            if not self.crypto.verify_hmac(hmac_data, hmac_signature, hmac_key):
                raise ValueError('数据完整性校验失败')

        # 解密数据
        encrypted_data = {
            'ciphertext': ciphertext,
            'iv': iv,
            'tag': tag
        }

        session_key = base64.b64decode(session_info['key'])
        decrypted_data = self.crypto.aes_decrypt_gcm(encrypted_data, session_key)

        # 数据解压缩
        if compressed:
            import gzip
            decompressed_data = gzip.decompress(decrypted_data).decode()
            transport_data = json.loads(decompressed_data)
        else:
            transport_data = json.loads(decrypted_data.decode())

        logger.info(f"[传输解密] 数据包已解密 - 会话: {session_id[:8]}..., 序列: {sequence}")

        return {
            'payload': transport_data['payload'],
            'metadata': {
                'timestamp': transport_data['timestamp'],
                'nonce': transport_data['nonce'],
                'sequence': transport_data['sequence'],
                'version': transport_data['version']
            }
        }

    def revoke_session(self, session_id: str):
        """撤销会话"""
        cache_key = f"{self.session_cache_prefix}{session_id}"
        cache.delete(cache_key)
        logger.info(f"[传输加密] 会话已撤销: {session_id[:8]}...")


class ApplicationCryptoUtils:
    """应用层加密工具"""

    def __init__(self):
        self.key = getattr(settings, 'CRYPTO_KEY', 'yuanyuzhou-metaverse-platform-secure-key')
        self.iv = getattr(settings, 'CRYPTO_IV', 'metaverse-iv-16ch')

    def encrypt(self, data: Any, level: int = 1) -> str:
        """应用层数据加密"""
        if level == 0:
            return json.dumps(data) if isinstance(data, (dict, list)) else str(data)

        json_str = json.dumps(data) if isinstance(data, (dict, list)) else str(data)

        # 多层加密
        encrypted = json_str
        for i in range(level):
            # 生成随机盐
            salt = secrets.token_bytes(16)

            # 派生密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=1000,
                backend=default_backend()
            )
            key = kdf.derive(self.key.encode())

            # 使用Fernet加密
            f = Fernet(base64.urlsafe_b64encode(key))
            ciphertext = f.encrypt(encrypted.encode())

            # 组合盐和密文
            encrypted = base64.b64encode(salt + ciphertext).decode()

        return encrypted

    def decrypt(self, encrypted_data: str, level: int = 1) -> Any:
        """应用层数据解密"""
        if level == 0:
            try:
                return json.loads(encrypted_data)
            except:
                return encrypted_data

        decrypted = encrypted_data
        for i in range(level):
            # 解码数据
            data = base64.b64decode(decrypted)
            salt = data[:16]
            ciphertext = data[16:]

            # 派生密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=1000,
                backend=default_backend()
            )
            key = kdf.derive(self.key.encode())

            # 解密
            f = Fernet(base64.urlsafe_b64encode(key))
            decrypted = f.decrypt(ciphertext).decode()

        try:
            return json.loads(decrypted)
        except:
            return decrypted


class EncryptionMiddleware(MiddlewareMixin):
    """加密中间件"""

    def __init__(self, get_response):
        super().__init__(get_response)
        self.transport_service = TransportEncryptionService()
        self.app_crypto = ApplicationCryptoUtils()
        self.excluded_paths = [
            '/admin/',
            '/api/docs/',
            '/api/schema/',
            '/health/',
            '/api/v1/auth/session/create/',  # 会话创建不需要解密
        ]

    def process_request(self, request: HttpRequest):
        """处理请求 - 解密数据"""
        # 检查是否需要解密
        if not self._should_decrypt(request):
            return None

        try:
            # 检查传输层加密
            if request.headers.get('X-Transport-Encrypted') == 'true':
                self._decrypt_transport_layer(request)

            # 检查应用层加密
            if hasattr(request, 'content_type') and 'application/json' in request.content_type:
                self._decrypt_application_layer(request)

        except Exception as e:
            logger.error(f"请求解密失败: {e}")
            return JsonResponse({
                'error': 'DECRYPTION_FAILED',
                'message': '请求解密失败',
                'code': 400
            }, status=400)

        return None

    def process_response(self, request: HttpRequest, response):
        """处理响应 - 加密数据"""
        # 检查是否需要加密响应
        if not self._should_encrypt_response(request, response):
            return response

        try:
            # 获取响应数据
            if hasattr(response, 'data'):
                response_data = response.data
            else:
                try:
                    response_data = json.loads(response.content.decode())
                except:
                    return response

            # 应用层加密
            encrypt_level = getattr(request, '_encrypt_level', 1)
            if encrypt_level > 0:
                encrypted_data = self.app_crypto.encrypt(response_data, encrypt_level)
                response_data = {
                    'encrypted_data': encrypted_data,
                    'encrypt_level': encrypt_level,
                    'encrypted': True
                }

            # 传输层加密
            session_id = getattr(request, '_session_id', None)
            if session_id:
                sequence = getattr(request, '_sequence', 0)
                transport_packet = self.transport_service.encrypt_transport(
                    response_data, session_id, sequence
                )
                response_data = transport_packet
                response['X-Transport-Encrypted'] = 'true'

            # 更新响应内容
            response.content = json.dumps(response_data, separators=(',', ':')).encode()
            response['Content-Length'] = len(response.content)

        except Exception as e:
            logger.error(f"响应加密失败: {e}")

        return response

    def _should_decrypt(self, request: HttpRequest) -> bool:
        """判断是否需要解密"""
        # 检查排除路径
        for path in self.excluded_paths:
            if request.path.startswith(path):
                return False

        # 检查请求方法
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return False

        # 检查加密标头
        if not (request.headers.get('X-Transport-Encrypted') or
                request.headers.get('X-Encrypt-Level')):
            return False

        return True

    def _should_encrypt_response(self, request: HttpRequest, response) -> bool:
        """判断是否需要加密响应"""
        # 检查排除路径
        for path in self.excluded_paths:
            if request.path.startswith(path):
                return False

        # 检查响应状态码
        if response.status_code >= 400:
            return False

        # 检查内容类型
        content_type = response.get('Content-Type', '')
        if 'application/json' not in content_type:
            return False

        return True

    def _decrypt_transport_layer(self, request: HttpRequest):
        """解密传输层数据"""
        try:
            # 解析请求体
            if request.body:
                transport_packet = json.loads(request.body.decode())

                # 解密传输包
                decrypted_result = self.transport_service.decrypt_transport(transport_packet)

                # 更新请求数据
                request._session_id = transport_packet['session_id']
                request._sequence = transport_packet['sequence']

                # 重新设置请求体
                new_body = json.dumps(decrypted_result['payload']).encode()
                request._body = new_body

        except Exception as e:
            logger.error(f"传输层解密失败: {e}")
            raise

    def _decrypt_application_layer(self, request: HttpRequest):
        """解密应用层数据"""
        try:
            if request.body:
                data = json.loads(request.body.decode())

                # 检查是否有加密数据
                if isinstance(data, dict) and data.get('encrypted_data'):
                    encrypt_level = data.get('encrypt_level', 1)
                    decrypted_data = self.app_crypto.decrypt(
                        data['encrypted_data'], encrypt_level
                    )

                    # 更新请求数据
                    request._encrypt_level = encrypt_level
                    new_body = json.dumps(decrypted_data).encode()
                    request._body = new_body

        except Exception as e:
            logger.error(f"应用层解密失败: {e}")
            raise
