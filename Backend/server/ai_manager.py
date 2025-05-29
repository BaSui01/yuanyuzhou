import asyncio
from typing import Dict, Any, List, Optional, Type
from .ai_providers.base import BaseAIProvider, MultiModalProvider, AgentProvider
from .ai_providers.siliconflow import SiliconFlowProvider
from .ai_providers.alibaba_bailian import AlibabaBailianProvider
from .ai_providers.openrouter import OpenRouterProvider
from .ai_providers.volcengine_ark import VolcengineArkProvider
from .ai_providers.baidu_qianfan import BaiduQianfanProvider
import logging

logger = logging.getLogger(__name__)


class AIManager:
    """AI服务管理器"""

    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.provider_classes = {
            'SILICONFLOW': SiliconFlowProvider,
            'ALIBABA_BAILIAN': AlibabaBailianProvider,
            'OPENROUTER': OpenRouterProvider,
            'VOLCENGINE_ARK': VolcengineArkProvider,
            'BAIDU_QIANFAN': BaiduQianfanProvider
        }

    def register_provider(self, provider_name: str, api_key: str, api_url: str, **kwargs) -> bool:
        """注册AI服务提供商"""
        try:
            if provider_name not in self.provider_classes:
                logger.error(f"不支持的AI服务提供商: {provider_name}")
                return False

            provider_class = self.provider_classes[provider_name]
            provider = provider_class(api_key, api_url, **kwargs)

            if provider.validate_config():
                self.providers[provider_name] = provider
                logger.info(f"成功注册AI服务提供商: {provider_name}")
                return True
            else:
                logger.error(f"AI服务提供商配置验证失败: {provider_name}")
                return False

        except Exception as e:
            logger.error(f"注册AI服务提供商失败: {provider_name} - {str(e)}")
            return False

    def get_provider(self, provider_name: str) -> Optional[BaseAIProvider]:
        """获取AI服务提供商"""
        return self.providers.get(provider_name)

    def list_providers(self) -> List[str]:
        """列出所有已注册的提供商"""
        return list(self.providers.keys())

    async def chat_completion(self, provider_name: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        provider = self.get_provider(provider_name)
        if not provider:
            return {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }

        return await provider.chat_completion(messages, **kwargs)

    async def stream_chat_completion(self, provider_name: str, messages: List[Dict[str, str]], **kwargs):
        """流式聊天完成"""
        provider = self.get_provider(provider_name)
        if not provider:
            yield {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }
            return

        async for chunk in provider.stream_chat_completion(messages, **kwargs):
            yield chunk

    async def speech_to_text(self, provider_name: str, audio_file: bytes, **kwargs) -> Dict[str, Any]:
        """语音转文字"""
        provider = self.get_provider(provider_name)
        if not provider:
            return {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }

        return await provider.speech_to_text(audio_file, **kwargs)

    async def text_to_speech(self, provider_name: str, text: str, **kwargs) -> bytes:
        """文字转语音"""
        provider = self.get_provider(provider_name)
        if not provider:
            raise Exception(f'AI服务提供商未找到: {provider_name}')

        return await provider.text_to_speech(text, **kwargs)

    async def image_generation(self, provider_name: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像生成"""
        provider = self.get_provider(provider_name)
        if not provider:
            return {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }

        return await provider.image_generation(prompt, **kwargs)

    async def image_analysis(self, provider_name: str, image_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像分析"""
        provider = self.get_provider(provider_name)
        if not provider:
            return {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }

        return await provider.image_analysis(image_data, prompt, **kwargs)

    async def multimodal_completion(self, provider_name: str, inputs: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """多模态完成"""
        provider = self.get_provider(provider_name)
        if not provider or not isinstance(provider, MultiModalProvider):
            return {
                'error': True,
                'message': f'多模态AI服务提供商未找到或不支持: {provider_name}'
            }

        return await provider.multimodal_completion(inputs, **kwargs)

    async def video_analysis(self, provider_name: str, video_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频分析"""
        provider = self.get_provider(provider_name)
        if not provider or not isinstance(provider, MultiModalProvider):
            return {
                'error': True,
                'message': f'视频分析AI服务提供商未找到或不支持: {provider_name}'
            }

        return await provider.video_analysis(video_data, prompt, **kwargs)

    async def document_analysis(self, provider_name: str, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        provider = self.get_provider(provider_name)
        if not provider or not isinstance(provider, MultiModalProvider):
            return {
                'error': True,
                'message': f'文档分析AI服务提供商未找到或不支持: {provider_name}'
            }

        return await provider.document_analysis(document_data, document_type, **kwargs)

    async def embeddings(self, provider_name: str, texts: List[str], **kwargs) -> Dict[str, Any]:
        """文本嵌入"""
        provider = self.get_provider(provider_name)
        if not provider:
            return {
                'error': True,
                'message': f'AI服务提供商未找到: {provider_name}'
            }

        return await provider.embeddings(texts, **kwargs)


class AIAgent:
    """AI智能体"""

    def __init__(self, agent_id: str, name: str, description: str, provider_name: str,
                 model: str, system_prompt: str, ai_manager: AIManager, **config):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.provider_name = provider_name
        self.model = model
        self.system_prompt = system_prompt
        self.ai_manager = ai_manager
        self.config = config
        self.conversation_history: List[Dict[str, str]] = []
        self.functions: List[Dict[str, Any]] = []

    def add_function(self, function_definition: Dict[str, Any]):
        """添加函数定义"""
        self.functions.append(function_definition)

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []

    def get_messages(self, user_message: str) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = []

        # 添加系统提示
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })

        # 添加历史对话
        messages.extend(self.conversation_history)

        # 添加用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages

    async def chat(self, user_message: str, **kwargs) -> Dict[str, Any]:
        """智能体对话"""
        try:
            messages = self.get_messages(user_message)

            # 合并配置参数
            params = {**self.config, **kwargs}
            params['model'] = self.model

            # 如果有函数定义，使用函数调用
            if self.functions and hasattr(self.ai_manager.get_provider(self.provider_name), 'function_calling'):
                provider = self.ai_manager.get_provider(self.provider_name)
                result = await provider.function_calling(messages, self.functions, **params)
            else:
                result = await self.ai_manager.chat_completion(self.provider_name, messages, **params)

            if result.get('success'):
                # 更新对话历史
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": result.get('content', '')
                })

                # 限制历史长度
                max_history = self.config.get('max_history', 20)
                if len(self.conversation_history) > max_history:
                    self.conversation_history = self.conversation_history[-max_history:]

            return result

        except Exception as e:
            logger.error(f"智能体对话失败: {self.agent_id} - {str(e)}")
            return {
                'error': True,
                'message': f'智能体对话失败: {str(e)}'
            }

    async def stream_chat(self, user_message: str, **kwargs):
        """智能体流式对话"""
        try:
            messages = self.get_messages(user_message)

            # 合并配置参数
            params = {**self.config, **kwargs}
            params['model'] = self.model

            full_response = ""
            async for chunk in self.ai_manager.stream_chat_completion(self.provider_name, messages, **params):
                if chunk.get('success') and chunk.get('delta', {}).get('content'):
                    full_response += chunk['delta']['content']
                yield chunk

            # 更新对话历史
            if full_response:
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": full_response
                })

                # 限制历史长度
                max_history = self.config.get('max_history', 20)
                if len(self.conversation_history) > max_history:
                    self.conversation_history = self.conversation_history[-max_history:]

        except Exception as e:
            logger.error(f"智能体流式对话失败: {self.agent_id} - {str(e)}")
            yield {
                'error': True,
                'message': f'智能体流式对话失败: {str(e)}'
            }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'description': self.description,
            'provider_name': self.provider_name,
            'model': self.model,
            'system_prompt': self.system_prompt,
            'config': self.config,
            'functions_count': len(self.functions),
            'history_length': len(self.conversation_history)
        }


class AgentManager:
    """智能体管理器"""

    def __init__(self, ai_manager: AIManager):
        self.ai_manager = ai_manager
        self.agents: Dict[str, AIAgent] = {}

    def create_agent(self, agent_id: str, name: str, description: str,
                    provider_name: str, model: str, system_prompt: str, **config) -> AIAgent:
        """创建智能体"""
        agent = AIAgent(
            agent_id=agent_id,
            name=name,
            description=description,
            provider_name=provider_name,
            model=model,
            system_prompt=system_prompt,
            ai_manager=self.ai_manager,
            **config
        )

        self.agents[agent_id] = agent
        logger.info(f"创建智能体: {agent_id} - {name}")
        return agent

    def get_agent(self, agent_id: str) -> Optional[AIAgent]:
        """获取智能体"""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有智能体"""
        return [agent.to_dict() for agent in self.agents.values()]

    def delete_agent(self, agent_id: str) -> bool:
        """删除智能体"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"删除智能体: {agent_id}")
            return True
        return False

    async def agent_chat(self, agent_id: str, user_message: str, **kwargs) -> Dict[str, Any]:
        """智能体对话"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {
                'error': True,
                'message': f'智能体未找到: {agent_id}'
            }

        return await agent.chat(user_message, **kwargs)

    async def agent_stream_chat(self, agent_id: str, user_message: str, **kwargs):
        """智能体流式对话"""
        agent = self.get_agent(agent_id)
        if not agent:
            yield {
                'error': True,
                'message': f'智能体未找到: {agent_id}'
            }
            return

        async for chunk in agent.stream_chat(user_message, **kwargs):
            yield chunk

    def clear_agent_history(self, agent_id: str) -> bool:
        """清除智能体对话历史"""
        agent = self.get_agent(agent_id)
        if agent:
            agent.clear_history()
            return True
        return False


# 全局AI管理器实例
ai_manager = AIManager()
agent_manager = AgentManager(ai_manager)


def get_ai_manager() -> AIManager:
    """获取AI管理器实例"""
    return ai_manager


def get_agent_manager() -> AgentManager:
    """获取智能体管理器实例"""
    return agent_manager
