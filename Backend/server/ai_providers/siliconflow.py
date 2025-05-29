import aiohttp
import json
from typing import Dict, Any, List, AsyncIterator
from .base import BaseAIProvider, MultiModalProvider
import logging

logger = logging.getLogger(__name__)


class SiliconFlowProvider(BaseAIProvider, MultiModalProvider):
    """硅基流动AI服务提供商"""

    def __init__(self, api_key: str, api_url: str = "https://api.siliconflow.cn/v1", **kwargs):
        super().__init__(api_key, api_url, **kwargs)
        self.timeout = kwargs.get('timeout', 30)

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        try:
            model = kwargs.get('model', 'Qwen/Qwen3-30B-A3B')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 4096)
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
            model = kwargs.get('model', 'Qwen/Qwen3-30B-A3B')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 4096)
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
            model = kwargs.get('model', 'FunAudioLLM/SenseVoiceSmall')
            language = kwargs.get('language', 'auto')

            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            form_data = aiohttp.FormData()
            form_data.add_field('file', audio_file, filename='audio.wav', content_type='audio/wav')
            form_data.add_field('model', model)
            form_data.add_field('language', language)

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
            model = kwargs.get('model', 'FishAudio/fish-speech-1.4')
            voice = kwargs.get('voice', 'default')
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
            model = kwargs.get('model', 'black-forest-labs/FLUX.1-schnell')
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
            # 硅基流动支持的视觉模型
            model = kwargs.get('model', 'Qwen/Qwen2-VL-72B-Instruct')

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
            model = kwargs.get('model', 'BAAI/bge-large-zh-v1.5')

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
            model = kwargs.get('model', 'Qwen/Qwen2-VL-72B-Instruct')

            messages = []
            for input_item in inputs:
                if input_item['type'] == 'text':
                    messages.append({
                        "role": "user",
                        "content": input_item['content']
                    })
                elif input_item['type'] == 'image':
                    # 处理图像输入
                    import base64
                    if isinstance(input_item['content'], bytes):
                        image_base64 = base64.b64encode(input_item['content']).decode('utf-8')
                    else:
                        image_base64 = input_item['content']

                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    })

            return await self.chat_completion(messages, model=model, **kwargs)

        except Exception as e:
            return await self.handle_error(e, "multimodal_completion")

    async def video_analysis(self, video_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频分析"""
        # 硅基流动暂不支持视频分析，返回错误
        return await self.handle_error(
            Exception("硅基流动平台暂不支持视频分析功能"),
            "video_analysis"
        )

    async def document_analysis(self, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        try:
            # 使用OCR模型进行文档分析
            model = kwargs.get('model', 'stepfun-ai/GOT-OCR2_0')
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
