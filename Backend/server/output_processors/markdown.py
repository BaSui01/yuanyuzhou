import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import DocumentOutputProcessor, ContentParser
import logging

logger = logging.getLogger(__name__)


class MarkdownProcessor(DocumentOutputProcessor):
    """Markdown文档输出处理器"""

    def __init__(self, **config):
        super().__init__(**config)
        self.toc_enabled = config.get('toc_enabled', True)
        self.code_highlight = config.get('code_highlight', True)
        self.table_alignment = config.get('table_alignment', 'left')

    def get_content_type(self) -> str:
        """获取内容类型"""
        return 'text/markdown'

    def get_file_extension(self) -> str:
        """获取文件扩展名"""
        return '.md'

    def add_heading(self, text: str, level: int = 1) -> str:
        """添加标题"""
        if level < 1:
            level = 1
        elif level > 6:
            level = 6

        return f"{'#' * level} {text}"

    def add_paragraph(self, text: str) -> str:
        """添加段落"""
        return text.strip()

    def add_code_block(self, code: str, language: str = '') -> str:
        """添加代码块"""
        return f"```{language}\n{code}\n```"

    def add_inline_code(self, code: str) -> str:
        """添加行内代码"""
        return f"`{code}`"

    def add_table(self, data: List[List[str]], headers: Optional[List[str]] = None) -> str:
        """添加表格"""
        if not data:
            return ""

        # 如果没有提供headers，使用第一行作为headers
        if headers is None and data:
            headers = data[0]
            data = data[1:]

        if not headers:
            return ""

        # 构建表格
        table_lines = []

        # 表头
        header_line = "| " + " | ".join(headers) + " |"
        table_lines.append(header_line)

        # 分隔符
        alignment_char = ':'
        if self.table_alignment == 'center':
            separator = "| " + " | ".join([f":{'-' * max(3, len(h)-2)}:" for h in headers]) + " |"
        elif self.table_alignment == 'right':
            separator = "| " + " | ".join([f"{'-' * max(3, len(h)-1)}:" for h in headers]) + " |"
        else:  # left
            separator = "| " + " | ".join(['-' * max(3, len(h)) for h in headers]) + " |"

        table_lines.append(separator)

        # 数据行
        for row in data:
            # 确保行数据与列数匹配
            padded_row = row + [''] * (len(headers) - len(row))
            padded_row = padded_row[:len(headers)]
            row_line = "| " + " | ".join(padded_row) + " |"
            table_lines.append(row_line)

        return "\n".join(table_lines)

    def add_list(self, items: List[str], ordered: bool = False) -> str:
        """添加列表"""
        if not items:
            return ""

        list_lines = []
        for i, item in enumerate(items):
            if ordered:
                list_lines.append(f"{i + 1}. {item}")
            else:
                list_lines.append(f"- {item}")

        return "\n".join(list_lines)

    def add_link(self, text: str, url: str, title: str = '') -> str:
        """添加链接"""
        if title:
            return f'[{text}]({url} "{title}")'
        return f'[{text}]({url})'

    def add_image(self, alt_text: str, url: str, title: str = '') -> str:
        """添加图片"""
        if title:
            return f'![{alt_text}]({url} "{title}")'
        return f'![{alt_text}]({url})'

    def add_blockquote(self, text: str) -> str:
        """添加引用块"""
        lines = text.split('\n')
        quoted_lines = [f"> {line}" for line in lines]
        return "\n".join(quoted_lines)

    def add_horizontal_rule(self) -> str:
        """添加水平分割线"""
        return "---"

    def add_bold(self, text: str) -> str:
        """添加粗体"""
        return f"**{text}**"

    def add_italic(self, text: str) -> str:
        """添加斜体"""
        return f"*{text}*"

    def add_strikethrough(self, text: str) -> str:
        """添加删除线"""
        return f"~~{text}~~"

    def generate_toc(self, content: str) -> str:
        """生成目录"""
        if not self.toc_enabled:
            return ""

        # 提取标题
        headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)

        if not headings:
            return ""

        toc_lines = ["## 目录", ""]

        for heading_marks, heading_text in headings:
            level = len(heading_marks)
            indent = "  " * (level - 1)
            # 生成锚点链接
            anchor = re.sub(r'[^\w\s-]', '', heading_text).strip()
            anchor = re.sub(r'[-\s]+', '-', anchor).lower()
            toc_lines.append(f"{indent}- [{heading_text}](#{anchor})")

        toc_lines.append("")
        return "\n".join(toc_lines)

    def add_metadata_header(self, metadata: Dict[str, Any]) -> str:
        """添加YAML元数据头"""
        if not metadata:
            return ""

        yaml_lines = ["---"]

        for key, value in metadata.items():
            if value is not None:
                if isinstance(value, str):
                    yaml_lines.append(f'{key}: "{value}"')
                elif isinstance(value, (list, tuple)):
                    yaml_lines.append(f'{key}:')
                    for item in value:
                        yaml_lines.append(f'  - "{item}"')
                else:
                    yaml_lines.append(f'{key}: {value}')

        yaml_lines.extend(["---", ""])
        return "\n".join(yaml_lines)

    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bytes:
        """处理内容并生成Markdown文档"""
        if not self.validate_content(content):
            raise ValueError("内容不能为空")

        # 准备元数据
        doc_metadata = self.prepare_metadata(metadata)
        if 'created_at' not in doc_metadata or not doc_metadata['created_at']:
            doc_metadata['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 构建文档
        document_parts = []

        # 添加YAML元数据头
        metadata_header = self.add_metadata_header(doc_metadata)
        if metadata_header:
            document_parts.append(metadata_header)

        # 解析内容为结构化数据
        sections = ContentParser.parse_ai_response(content)

        # 格式化文档内容
        formatted_content = self.format_document(sections)

        # 生成目录
        if self.toc_enabled:
            toc = self.generate_toc(formatted_content)
            if toc:
                document_parts.append(toc)

        # 添加主要内容
        document_parts.append(formatted_content)

        # 组合最终文档
        final_document = "\n".join(document_parts)

        return final_document.encode('utf-8')

    def process_with_custom_structure(self, sections: List[Dict[str, Any]],
                                    metadata: Optional[Dict[str, Any]] = None) -> bytes:
        """使用自定义结构处理内容"""
        # 准备元数据
        doc_metadata = self.prepare_metadata(metadata)
        if 'created_at' not in doc_metadata or not doc_metadata['created_at']:
            doc_metadata['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 构建文档
        document_parts = []

        # 添加YAML元数据头
        metadata_header = self.add_metadata_header(doc_metadata)
        if metadata_header:
            document_parts.append(metadata_header)

        # 格式化文档内容
        formatted_content = self.format_document(sections)

        # 生成目录
        if self.toc_enabled:
            toc = self.generate_toc(formatted_content)
            if toc:
                document_parts.append(toc)

        # 添加主要内容
        document_parts.append(formatted_content)

        # 组合最终文档
        final_document = "\n".join(document_parts)

        return final_document.encode('utf-8')

    def convert_html_to_markdown(self, html_content: str) -> str:
        """将HTML内容转换为Markdown（简单实现）"""
        # 这是一个简单的HTML到Markdown转换器
        # 在实际项目中，建议使用专门的库如html2text

        # 基本的HTML标签转换
        conversions = [
            (r'<h([1-6])>(.*?)</h[1-6]>', lambda m: f"{'#' * int(m.group(1))} {m.group(2)}"),
            (r'<p>(.*?)</p>', r'\1\n'),
            (r'<br\s*/?>', '\n'),
            (r'<strong>(.*?)</strong>', r'**\1**'),
            (r'<b>(.*?)</b>', r'**\1**'),
            (r'<em>(.*?)</em>', r'*\1*'),
            (r'<i>(.*?)</i>', r'*\1*'),
            (r'<code>(.*?)</code>', r'`\1`'),
            (r'<a\s+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)'),
            (r'<img\s+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)'),
            (r'<ul>', ''),
            (r'</ul>', ''),
            (r'<ol>', ''),
            (r'</ol>', ''),
            (r'<li>(.*?)</li>', r'- \1'),
            (r'<blockquote>(.*?)</blockquote>', lambda m: '\n'.join(f'> {line}' for line in m.group(1).split('\n'))),
        ]

        result = html_content
        for pattern, replacement in conversions:
            if callable(replacement):
                result = re.sub(pattern, replacement, result, flags=re.DOTALL | re.IGNORECASE)
            else:
                result = re.sub(pattern, replacement, result, flags=re.DOTALL | re.IGNORECASE)

        # 清理多余的空行
        result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)

        return result.strip()

    def process_chat_conversation(self, conversation: List[Dict[str, str]],
                                metadata: Optional[Dict[str, Any]] = None) -> bytes:
        """处理聊天对话为Markdown格式"""
        doc_metadata = self.prepare_metadata(metadata)
        doc_metadata['title'] = doc_metadata.get('title', '对话记录')

        sections = []

        # 添加标题
        sections.append({
            'type': 'heading',
            'content': doc_metadata['title'],
            'level': 1
        })

        # 添加对话内容
        for i, message in enumerate(conversation):
            role = message.get('role', 'user')
            content = message.get('content', '')

            # 角色标题
            role_name = '用户' if role == 'user' else 'AI助手'
            sections.append({
                'type': 'heading',
                'content': f"{role_name}",
                'level': 3
            })

            # 消息内容
            sections.append({
                'type': 'paragraph',
                'content': content
            })

            # 添加分隔线（除了最后一条消息）
            if i < len(conversation) - 1:
                sections.append({
                    'type': 'paragraph',
                    'content': self.add_horizontal_rule()
                })

        return self.process_with_custom_structure(sections, doc_metadata)


def create_markdown_processor(**config) -> MarkdownProcessor:
    """创建Markdown处理器实例"""
    return MarkdownProcessor(**config)
