import aiohttp
import json
from typing import Dict, Any, List, AsyncIterator
from .base import BaseAIProvider, MultiModalProvider
import logging
import hashlib
import hmac
import time
from urllib.parse import quote

logger = logging.getLogger(__name__)


class BaiduQianfanProvider(BaseAIProvider, MultiModalProvider):
    """百度千帆大模型平台AI服务提供商"""

    def __init__(self, api_key: str, api_url: str = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop", **kwargs):
        super().__init__(api_key, api_url, **kwargs)
        self.timeout = kwargs.get('timeout', 30)
        self.secret_key = kwargs.get('secret_key', '')
        self.access_token = None

    async def get_access_token(self) -> str:
        """获取访问令牌"""
        if self.access_token:
            return self.access_token

        try:
            # 使用API Key和Secret Key获取access_token
            token_url = f"https://aip.baidubce.com/oauth/2.0/token"
            params = {
                'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': self.secret_key
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(token_url, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.access_token = result['access_token']
                        return self.access_token
                    else:
                        error_text = await response.text()
                        raise Exception(f"获取访问令牌失败: {response.status} - {error_text}")

        except Exception as e:
            logger.error(f"获取百度千帆访问令牌失败: {str(e)}")
            raise e

    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            'Content-Type': 'application/json'
        }

    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """聊天完成"""
        try:
            model = kwargs.get('model', 'ERNIE-4.0-8K')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 8192)
            top_p = kwargs.get('top_p', 0.9)

            # 获取访问令牌
            access_token = await self.get_access_token()

            # 构建API端点
            model_endpoints = {
                'ERNIE-4.0-8K': 'completions_pro',
                'ERNIE-3.5-8K': 'completions',
                'ERNIE-Speed-8K': 'ernie_speed',
                'ERNIE-Speed-128K': 'ernie_speed',
                'ERNIE-Lite-8K': 'ernie-lite-8k',
                'ERNIE-Tiny-8K': 'ernie-tiny-8k',
                'ERNIE-Character-8K': 'ernie-char-8k',
                'ERNIE-Functions-8K': 'ernie-func-8k',
                'ERNIE-Bot-turbo': 'eb-instant'
            }

            endpoint = model_endpoints.get(model, 'completions_pro')

            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": top_p,
                "stream": False
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/{endpoint}?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'result' in result:
                            return {
                                'success': True,
                                'data': result,
                                'content': result['result'],
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
            model = kwargs.get('model', 'ERNIE-4.0-8K')
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', 8192)
            top_p = kwargs.get('top_p', 0.9)

            # 获取访问令牌
            access_token = await self.get_access_token()

            # 构建API端点
            model_endpoints = {
                'ERNIE-4.0-8K': 'completions_pro',
                'ERNIE-3.5-8K': 'completions',
                'ERNIE-Speed-8K': 'ernie_speed',
                'ERNIE-Speed-128K': 'ernie_speed',
                'ERNIE-Lite-8K': 'ernie-lite-8k',
                'ERNIE-Tiny-8K': 'ernie-tiny-8k',
                'ERNIE-Character-8K': 'ernie-char-8k',
                'ERNIE-Functions-8K': 'ernie-func-8k',
                'ERNIE-Bot-turbo': 'eb-instant'
            }

            endpoint = model_endpoints.get(model, 'completions_pro')

            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": top_p,
                "stream": True
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/{endpoint}?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            line_text = line.decode('utf-8').strip()
                            if line_text.startswith('data: '):
                                data_text = line_text[6:]
                                if data_text and data_text != '[DONE]':
                                    try:
                                        data = json.loads(data_text)
                                        if 'result' in data:
                                            yield {
                                                'success': True,
                                                'data': data,
                                                'delta': {
                                                    'content': data['result']
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
            # 获取访问令牌
            access_token = await self.get_access_token()

            # 百度语音识别API
            asr_url = f"https://vop.baidu.com/server_api?access_token={access_token}"

            # 构建请求数据
            import base64
            audio_base64 = base64.b64encode(audio_file).decode('utf-8')

            payload = {
                "format": "wav",
                "rate": 16000,
                "channel": 1,
                "cuid": "ai_platform",
                "token": access_token,
                "speech": audio_base64,
                "len": len(audio_file)
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    asr_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('err_no') == 0:
                            return {
                                'success': True,
                                'data': result,
                                'text': result['result'][0] if result.get('result') else '',
                                'language': 'zh',
                                'model': 'baidu-asr'
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"语音识别失败: {result.get('err_msg', '未知错误')}"),
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
            # 获取访问令牌
            access_token = await self.get_access_token()

            # 百度语音合成API
            tts_url = f"https://tsn.baidu.com/text2audio"

            voice = kwargs.get('voice', '0')  # 0-女声，1-男声，3-情感合成-度逍遥，4-情感合成-度丫丫
            speed = kwargs.get('speed', '5')  # 语速，取值0-15
            pitch = kwargs.get('pitch', '5')  # 音调，取值0-15
            volume = kwargs.get('volume', '5')  # 音量，取值0-15

            params = {
                'tok': access_token,
                'tex': text,
                'per': voice,
                'spd': speed,
                'pit': pitch,
                'vol': volume,
                'aue': '3',  # 3为mp3格式
                'cuid': 'ai_platform'
            }

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(tts_url, data=params) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if 'audio' in content_type:
                            return await response.read()
                        else:
                            # 返回的是错误信息（JSON格式）
                            error_info = await response.json()
                            raise Exception(f"文字转语音失败: {error_info}")
                    else:
                        error_text = await response.text()
                        raise Exception(f"文字转语音失败: {response.status} - {error_text}")

        except Exception as e:
            logger.error(f"文字转语音失败: {str(e)}")
            raise e

    async def image_generation(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """图像生成"""
        try:
            # 获取访问令牌
            access_token = await self.get_access_token()

            size = kwargs.get('size', '1024x1024')
            n = kwargs.get('n', 1)
            style = kwargs.get('style', '写实风格')

            payload = {
                "text": prompt,
                "style": style,
                "resolution": size,
                "num": n
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/text2image?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'data' in result:
                            return {
                                'success': True,
                                'data': result,
                                'images': [{'url': item['image']} for item in result['data']],
                                'model': 'stable-diffusion-xl'
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
            # 获取访问令牌
            access_token = await self.get_access_token()

            # 将图片转换为base64
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # 使用ERNIE-VilG进行图像理解
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "image": image_base64
                            }
                        ]
                    }
                ]
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/ernie_vilg?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'result' in result:
                            return {
                                'success': True,
                                'data': result,
                                'content': result['result'],
                                'usage': result.get('usage', {}),
                                'model': 'ernie-vilg'
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
            # 获取访问令牌
            access_token = await self.get_access_token()

            model = kwargs.get('model', 'bge_large_zh')

            payload = {
                "input": texts
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/embeddings/{model}?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'data' in result:
                            return {
                                'success': True,
                                'data': result,
                                'embeddings': [item['embedding'] for item in result['data']],
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
            # 获取访问令牌
            access_token = await self.get_access_token()

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
                        "type": "image",
                        "image": image_base64
                    })

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": content_list
                    }
                ]
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/ernie_vilg?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'result' in result:
                            return {
                                'success': True,
                                'data': result,
                                'content': result['result'],
                                'usage': result.get('usage', {}),
                                'model': 'ernie-vilg'
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
        # 百度千帆暂不支持视频分析，返回错误
        return await self.handle_error(
            Exception("百度千帆平台暂不支持视频分析功能"),
            "video_analysis"
        )

    async def document_analysis(self, document_data: bytes, document_type: str, **kwargs) -> Dict[str, Any]:
        """文档分析"""
        try:
            # 使用OCR接口进行文档分析
            access_token = await self.get_access_token()

            # 将文档转换为base64
            import base64
            doc_base64 = base64.b64encode(document_data).decode('utf-8')

            # 根据文档类型选择OCR接口
            if document_type in ['application/pdf', 'image/jpeg', 'image/png']:
                ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
                payload = {"image": doc_base64}
            else:
                return await self.handle_error(
                    Exception(f"不支持的文档类型: {document_type}"),
                    "document_analysis"
                )

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    ocr_url,
                    headers=headers,
                    data=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'words_result' in result:
                            # 提取文本内容
                            text_content = '\n'.join([item['words'] for item in result['words_result']])

                            # 使用ERNIE模型分析文档内容
                            analysis_prompt = kwargs.get('prompt', '请分析这份文档的内容') + f"\n\n文档内容:\n{text_content}"
                            analysis_result = await self.text_generation(analysis_prompt)

                            if analysis_result['success']:
                                return {
                                    'success': True,
                                    'data': {
                                        'ocr_result': result,
                                        'analysis_result': analysis_result['data']
                                    },
                                    'content': analysis_result['content'],
                                    'extracted_text': text_content,
                                    'model': 'baidu-ocr+ernie'
                                }
                            else:
                                return analysis_result
                        else:
                            return await self.handle_error(
                                Exception(f"OCR识别失败: {result}"),
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

    async def function_calling(self, messages: List[Dict[str, str]], functions: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """函数调用"""
        try:
            model = kwargs.get('model', 'ERNIE-Functions-8K')

            # 获取访问令牌
            access_token = await self.get_access_token()

            payload = {
                "messages": messages,
                "functions": functions,
                "stream": False
            }

            headers = self.get_headers()

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.api_url}/chat/ernie-func-8k?access_token={access_token}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'result' in result:
                            return {
                                'success': True,
                                'data': result,
                                'content': result.get('result', ''),
                                'function_call': result.get('function_call'),
                                'usage': result.get('usage', {}),
                                'model': model
                            }
                        else:
                            return await self.handle_error(
                                Exception(f"函数调用响应格式错误: {result}"),
                                "function_calling"
                            )
                    else:
                        error_text = await response.text()
                        return await self.handle_error(
                            Exception(f"函数调用失败: {response.status} - {error_text}"),
                            "function_calling"
                        )

        except Exception as e:
            return await self.handle_error(e, "function_calling")
