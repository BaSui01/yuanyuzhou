from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncIterator
import logging

logger = logging.getLogger(__name__)


class BaseAIProvider(ABC):
    """AI服务提供商基础抽象类"""

    def __init__(self, api_key: str, api_url: str, **kwargs):
        self.api_key = api_key
        self.api_url = api_url
        self.config = kwargs

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        pass

    @abstractmethod
    async def text_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """文本生成"""
        pass

    @abstractmethod
    async def speech_to_text(self, audio_file: bytes, **kwargs) -> Dict[str, Any]:
        """语音转文字"""
        pass

    @abstractmethod
    async def text_to_speech(self, text: str, **kwargs) -> bytes:
        """文字转语音"""
        pass

    @abstractmethod
    async def image_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像生成"""
        pass

    @abstractmethod
    async def image_analysis(self, image_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像分析"""
        pass

    @abstractmethod
    async def embeddings(self, texts: List[str], **kwargs) -> Dict[str, Any]:
        """文本嵌入"""
        pass

    @abstractmethod
    async def stream_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[Dict[str, Any]]:
        """流式聊天完成"""
        pass

    def validate_config(self) -> bool:
        """验证配置"""
        return bool(self.api_key and self.api_url)

    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    async def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """处理错误"""
        logger.error(f"AI Provider Error in {context}: {str(error)}")
        return {
            'error': True,
            'message': str(error),
            'context': context
        }


class MultiModalProvider(BaseAIProvider):
    """多模态AI服务提供商"""

    @abstractmethod
    async def multimodal_completion(self, inputs: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """多模态完成"""
        pass

    @abstractmethod
    async def video_analysis(self, video_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频分析"""
        pass

    @abstractmethod
    async def document_analysis(self, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        pass


class AgentProvider(BaseAIProvider):
    """AI智能体服务提供商"""

    @abstractmethod
    async def create_agent(self, agent_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """创建智能体"""
        pass

    @abstractmethod
    async def agent_chat(self, agent_id: str, message: str, **kwargs) -> Dict[str, Any]:
        """智能体对话"""
        pass

    @abstractmethod
    async def agent_function_call(self, agent_id: str, function_name: str, parameters: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """智能体函数调用"""
        pass

    @abstractmethod
    async def list_agents(self, **kwargs) -> List[Dict[str, Any]]:
        """列出智能体"""
        pass

    @abstractmethod
    async def delete_agent(self, agent_id: str, **kwargs) -> bool:
        """删除智能体"""
        pass
