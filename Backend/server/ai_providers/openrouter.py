import aiohttp
import json
from typing import Dict, Any, List, AsyncIterator
from .base import BaseAIProvider, MultiModalProvider
import logging

logger = logging.getLogger(__name__)


class OpenRouterProvider(BaseAIProvider, MultiModalProvider):
    """OpenRouter AI服务提供商"""

    def __init__(self, api_key: str, api_url: str = "https://openrouter.ai/api/v1", **kwargs):
        super().__init__(api_key, api_url, **kwargs)
        self.timeout = kwargs.get('timeout', 60)
        self.app_name = kwargs.get('app_name', 'AI-Platform')

    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': 'https://ai-platform.com',
            'X-Title': self.app_name
        }

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        try:
            model = kwargs.get('model', 'mistralai/devstral-small:free')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 32768)
            top_p = kwargs.get('top_p', 0.9)

            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": False
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result,
                            'content': result['choices'][0]['message']['content'],
                            'usage': result.get('usage', {}),
                            'model': model
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"API请求失败: {response.status} - {error_text}"),
                            "chat_completion"
                        )

        except Exception as e:
            return await self.handle_error(e, "chat_completion")

    async def stream_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[Dict[str, Any]]:
        """流式聊天完成"""
        try:
            model = kwargs.get('model', 'mistralai/devstral-small:free')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 32768)
            top_p = kwargs.get('top_p', 0.9)

            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": True
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            line_text = line.decode('utf-8').strip()
                            if line_text.startswith('data: '):
                                data_text = line_text[6:]
                                if data_text == '[DONE]':
                                    break
                                try:
                                    data = json.loads(data_text)
                                    yield {
                                        'success': True,
                                        'data': data,
                                        'delta': data['choices'][0]['delta'] if data['choices'] else {},
                                        'model': model
                                    }
                                except json.JSONDecodeError:
                                    continue
                    else:
                        error_text = await response.text()
                        yield await self.handle_error(
                            Exception(f"流式API请求失败: {response.status} - {error_text}"),
                            "stream_chat_completion"
                        )

        except Exception as e:
            yield await self.handle_error(e, "stream_chat_completion")

    async def text_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """文本生成"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, **kwargs)

    async def speech_to_text(self, audio_file: bytes, **kwargs) -> Dict[str, Any]:
        """语音转文字"""
        try:
            model = kwargs.get('model', 'openai/whisper-1')
            language = kwargs.get('language', 'zh')

            form_data = aiohttp.FormData()
            form_data.add_field('file', audio_file, filename='audio.wav', content_type='audio/wav')
            form_data.add_field('model', model)
            if language != 'auto':
                form_data.add_field('language', language)

            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'HTTP-Referer': 'https://ai-platform.com',
                'X-Title': self.app_name
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/audio/transcriptions",
                    headers=headers,
                    data=form_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result,
                            'text': result.get('text', ''),
                            'language': result.get('language', language),
                            'model': model
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"语音转文字失败: {response.status} - {error_text}"),
                            "speech_to_text"
                        )

        except Exception as e:
            return await self.handle_error(e, "speech_to_text")

    async def text_to_speech(self, text: str, **kwargs) -> bytes:
        """文字转语音"""
        try:
            model = kwargs.get('model', 'openai/tts-1')
            voice = kwargs.get('voice', 'alloy')
            speed = kwargs.get('speed', 1.0)

            payload = {
                "model": model,
                "input": text,
                "voice": voice,
                "speed": speed
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/audio/speech",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        error_text = await response.text()
                        raise Exception(f"文字转语音失败: {response.status} - {error_text}")

        except Exception as e:
            logger.error(f"文字转语音失败: {str(e)}")
            raise e

    async def image_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像生成"""
        try:
            model = kwargs.get('model', 'openai/dall-e-3')
            size = kwargs.get('size', '1024x1024')
            quality = kwargs.get('quality', 'standard')
            n = kwargs.get('n', 1)

            payload = {
                "model": model,
                "prompt": prompt,
                "size": size,
                "quality": quality,
                "n": n
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/images/generations",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result,
                            'images': result.get('data', []),
                            'model': model
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"图像生成失败: {response.status} - {error_text}"),
                            "image_generation"
                        )

        except Exception as e:
            return await self.handle_error(e, "image_generation")

    async def image_analysis(self, image_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像分析"""
        try:
            model = kwargs.get('model', 'google/gemini-2.5-pro-exp-03-25')

            # 将图片转换为base64
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]

            return await self.chat_completion(messages, model=model, **kwargs)

        except Exception as e:
            return await self.handle_error(e, "image_analysis")

    async def embeddings(self, texts: List[str], **kwargs) -> Dict[str, Any]:
        """文本嵌入"""
        try:
            model = kwargs.get('model', 'openai/text-embedding-3-small')

            payload = {
                "model": model,
                "input": texts
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/embeddings",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result,
                            'embeddings': [item['embedding'] for item in result['data']],
                            'model': model
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"文本嵌入失败: {response.status} - {error_text}"),
                            "embeddings"
                        )

        except Exception as e:
            return await self.handle_error(e, "embeddings")

    async def multimodal_completion(self, inputs: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """多模态完成"""
        try:
            model = kwargs.get('model', 'google/gemini-2.5-pro-exp-03-25')

            content_list = []
            for input_item in inputs:
                if input_item['type'] == 'text':
                    content_list.append({
                        "type": "text",
                        "text": input_item['content']
                    })
                elif input_item['type'] == 'image':
                    # 处理图像输入
                    import base64
                    if isinstance(input_item['content'], bytes):
                        image_base64 = base64.b64encode(input_item['content']).decode('utf-8')
                    else:
                        image_base64 = input_item['content']

                    content_list.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    })

            messages = [
                {
                    "role": "user",
                    "content": content_list
                }
            ]

            return await self.chat_completion(messages, model=model, **kwargs)

        except Exception as e:
            return await self.handle_error(e, "multimodal_completion")

    async def video_analysis(self, video_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频分析"""
        try:
            # 使用支持视频的模型
            model = kwargs.get('model', 'google/gemini-2.5-pro-exp-03-25')

            # 将视频转换为base64
            import base64
            video_base64 = base64.b64encode(video_data).decode('utf-8')

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "video_url",
                            "video_url": {
                                "url": f"data:video/mp4;base64,{video_base64}"
                            }
                        }
                    ]
                }
            ]

            return await self.chat_completion(messages, model=model, **kwargs)

        except Exception as e:
            return await self.handle_error(e, "video_analysis")

    async def document_analysis(self, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        try:
            model = kwargs.get('model', 'google/gemini-2.5-pro-exp-03-25')
            prompt = kwargs.get('prompt', '请分析这份文档的内容')

            # 将文档转换为base64
            import base64
            doc_base64 = base64.b64encode(document_data).decode('utf-8')

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{document_type};base64,{doc_base64}"
                            }
                        }
                    ]
                }
            ]

            return await self.chat_completion(messages, model=model, **kwargs)

        except Exception as e:
            return await self.handle_error(e, "document_analysis")

    async def get_available_models(self) -> Dict[str, Any]:
        """获取可用模型列表"""
        try:
            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(
                    f"{self.api_url}/models",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result,
                            'models': result.get('data', [])
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"获取模型列表失败: {response.status} - {error_text}"),
                            "get_available_models"
                        )

        except Exception as e:
            return await self.handle_error(e, "get_available_models")

    async def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """获取模型信息"""
        try:
            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(
                    f"{self.api_url}/models/{model_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            'success': True,
                            'data': result
                        }
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"获取模型信息失败: {response.status} - {error_text}"),
                            "get_model_info"
                        )

        except Exception as e:
            return await self.handle_error(e, "get_model_info")
