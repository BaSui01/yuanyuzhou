import aiohttp
import json
from typing import Dict, Any, List, AsyncIterator
from .base import BaseAIProvider, MultiModalProvider
import logging

logger = logging.getLogger(__name__)


class AlibabaBailianProvider(BaseAIProvider, MultiModalProvider):
    """阿里云百炼AI服务提供商"""

    def __init__(self, api_key: str, api_url: str = "https://dashscope.aliyuncs.com/api/v1", **kwargs):
        super().__init__(api_key, api_url, **kwargs)
        self.timeout = kwargs.get('timeout', 30)

    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'X-DashScope-SSE': 'enable'  # 启用SSE流式传输
        }

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        try:
            model = kwargs.get('model', 'qwen-turbo-latest')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 4096)
            top_p = kwargs.get('top_p', 0.9)

            payload = {
                "model": model,
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p,
                    "stream": False,
                    "result_format": "message"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/text-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('choices'):
                            choice = result['output']['choices'][0]
                            return {
                                'success': True,
                                'data': result,
                                'content': choice['message']['content'],
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"API响应格式错误: {result}"),
                                "chat_completion"
                            )
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
            model = kwargs.get('model', 'qwen-turbo-latest')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 4096)
            top_p = kwargs.get('top_p', 0.9)

            payload = {
                "model": model,
                "input": {
                    "messages": messages
                },
                "parameters": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p,
                    "stream": True,
                    "result_format": "message",
                    "incremental_output": True
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/text-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            line_text = line.decode('utf-8').strip()
                            if line_text.startswith('data:'):
                                data_text = line_text[5:].strip()
                                if data_text and data_text != '[DONE]':
                                    try:
                                        data = json.loads(data_text)
                                        if data.get('output') and data['output'].get('choices'):
                                            choice = data['output']['choices'][0]
                                            yield {
                                                'success': True,
                                                'data': data,
                                                'delta': {
                                                    'content': choice['message'].get('content', '')
                                                },
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
            model = kwargs.get('model', 'paraformer-realtime-v2')
            language = kwargs.get('language', 'zh')

            # 构建multipart/form-data
            form_data = aiohttp.FormData()
            form_data.add_field('model', model)
            form_data.add_field('input', audio_file, filename='audio.wav', content_type='audio/wav')
            form_data.add_field('parameters', json.dumps({
                'language': language,
                'format': 'pcm',
                'sample_rate': 16000
            }))

            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/audio/asr/transcription",
                    headers=headers,
                    data=form_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('transcription'):
                            return {
                                'success': True,
                                'data': result,
                                'text': result['output']['transcription'],
                                'language': language,
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"语音识别响应格式错误: {result}"),
                                "speech_to_text"
                            )
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
            model = kwargs.get('model', 'sambert-zhichu-v1')
            voice = kwargs.get('voice', 'zhichu')
            speed = kwargs.get('speed', 1.0)

            payload = {
                "model": model,
                "input": {
                    "text": text
                },
                "parameters": {
                    "voice": voice,
                    "speed": speed,
                    "format": "wav"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/audio/tts/synthesis",
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
            model = kwargs.get('model', 'wanx-v1')
            size = kwargs.get('size', '1024*1024')
            n = kwargs.get('n', 1)
            style = kwargs.get('style', '<auto>')

            payload = {
                "model": model,
                "input": {
                    "prompt": prompt
                },
                "parameters": {
                    "size": size,
                    "n": n,
                    "style": style
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/text2image/image-synthesis",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('results'):
                            return {
                                'success': True,
                                'data': result,
                                'images': [{'url': item['url']} for item in result['output']['results']],
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"图像生成响应格式错误: {result}"),
                                "image_generation"
                            )
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
            model = kwargs.get('model', 'qwen-vl-max')

            # 将图片转换为base64
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            payload = {
                "model": model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                },
                                {
                                    "image": f"data:image/jpeg;base64,{image_base64}"
                                }
                            ]
                        }
                    ]
                },
                "parameters": {
                    "result_format": "message"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/multimodal-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('choices'):
                            choice = result['output']['choices'][0]
                            return {
                                'success': True,
                                'data': result,
                                'content': choice['message']['content'],
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"图像分析响应格式错误: {result}"),
                                "image_analysis"
                            )
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"图像分析失败: {response.status} - {error_text}"),
                            "image_analysis"
                        )

        except Exception as e:
            return await self.handle_error(e, "image_analysis")

    async def embeddings(self, texts: List[str], **kwargs) -> Dict[str, Any]:
        """文本嵌入"""
        try:
            model = kwargs.get('model', 'text-embedding-v2')

            payload = {
                "model": model,
                "input": {
                    "texts": texts
                },
                "parameters": {
                    "text_type": "document"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/embeddings/text-embedding/text-embedding",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('embeddings'):
                            return {
                                'success': True,
                                'data': result,
                                'embeddings': [item['embedding'] for item in result['output']['embeddings']],
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"文本嵌入响应格式错误: {result}"),
                                "embeddings"
                            )
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
            model = kwargs.get('model', 'qwen-vl-max')

            content_list = []
            for input_item in inputs:
                if input_item['type'] == 'text':
                    content_list.append({
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
                        "image": f"data:image/jpeg;base64,{image_base64}"
                    })

            payload = {
                "model": model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": content_list
                        }
                    ]
                },
                "parameters": {
                    "result_format": "message"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/multimodal-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('choices'):
                            choice = result['output']['choices'][0]
                            return {
                                'success': True,
                                'data': result,
                                'content': choice['message']['content'],
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"多模态完成响应格式错误: {result}"),
                                "multimodal_completion"
                            )
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"多模态完成失败: {response.status} - {error_text}"),
                            "multimodal_completion"
                        )

        except Exception as e:
            return await self.handle_error(e, "multimodal_completion")

    async def video_analysis(self, video_data: bytes, prompt: str, **kwargs) -> Dict[str, Any]:
        """视频分析"""
        try:
            model = kwargs.get('model', 'qwen-vl-max')

            # 将视频转换为base64
            import base64
            video_base64 = base64.b64encode(video_data).decode('utf-8')

            payload = {
                "model": model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                },
                                {
                                    "video": f"data:video/mp4;base64,{video_base64}"
                                }
                            ]
                        }
                    ]
                },
                "parameters": {
                    "result_format": "message"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/multimodal-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('choices'):
                            choice = result['output']['choices'][0]
                            return {
                                'success': True,
                                'data': result,
                                'content': choice['message']['content'],
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"视频分析响应格式错误: {result}"),
                                "video_analysis"
                            )
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"视频分析失败: {response.status} - {error_text}"),
                            "video_analysis"
                        )

        except Exception as e:
            return await self.handle_error(e, "video_analysis")

    async def document_analysis(self, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        try:
            # 使用百炼的文档理解能力
            model = kwargs.get('model', 'qwen-vl-max')
            prompt = kwargs.get('prompt', '请分析这份文档的内容')

            # 将文档转换为base64
            import base64
            doc_base64 = base64.b64encode(document_data).decode('utf-8')

            payload = {
                "model": model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                },
                                {
                                    "image": f"data:{document_type};base64,{doc_base64}"
                                }
                            ]
                        }
                    ]
                },
                "parameters": {
                    "result_format": "message"
                }
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/services/aigc/multimodal-generation/generation",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('output') and result['output'].get('choices'):
                            choice = result['output']['choices'][0]
                            return {
                                'success': True,
                                'data': result,
                                'content': choice['message']['content'],
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"文档分析响应格式错误: {result}"),
                                "document_analysis"
                            )
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"文档分析失败: {response.status} - {error_text}"),
                            "document_analysis"
                        )

        except Exception as e:
            return await self.handle_error(e, "document_analysis")
