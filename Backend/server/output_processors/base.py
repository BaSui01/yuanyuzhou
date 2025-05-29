from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class BaseOutputProcessor(ABC):
    """输出处理器基础抽象类"""

    def __init__(self, **config):
        self.config = config

    @abstractmethod
    def process(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bytes:
        """处理内容并生成输出"""
        pass

    @abstractmethod
    def get_content_type(self) -> str:
        """获取内容类型"""
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """获取文件扩展名"""
        pass

    def validate_content(self, content: str) -> bool:
        """验证内容"""
        return bool(content and content.strip())

    def prepare_metadata(self, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """准备元数据"""
        default_metadata = {
            'title': '文档',
            'author': 'AI助手',
            'created_at': None,
            'description': ''
        }

        if metadata:
            default_metadata.update(metadata)

        return default_metadata


class StructuredOutputProcessor(BaseOutputProcessor):
    """结构化输出处理器基类"""

    @abstractmethod
    def process_table(self, data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> bytes:
        """处理表格数据"""
        pass

    @abstractmethod
    def process_list(self, items: List[str], ordered: bool = False) -> bytes:
        """处理列表数据"""
        pass

    @abstractmethod
    def process_key_value(self, data: Dict[str, Any]) -> bytes:
        """处理键值对数据"""
        pass


class DocumentOutputProcessor(BaseOutputProcessor):
    """文档输出处理器基类"""

    @abstractmethod
    def add_heading(self, text: str, level: int = 1) -> str:
        """添加标题"""
        pass

    @abstractmethod
    def add_paragraph(self, text: str) -> str:
        """添加段落"""
        pass

    @abstractmethod
    def add_code_block(self, code: str, language: str = '') -> str:
        """添加代码块"""
        pass

    @abstractmethod
    def add_table(self, data: List[List[str]], headers: Optional[List[str]] = None) -> str:
        """添加表格"""
        pass

    @abstractmethod
    def add_list(self, items: List[str], ordered: bool = False) -> str:
        """添加列表"""
        pass

    def format_document(self, sections: List[Dict[str, Any]]) -> str:
        """格式化文档"""
        document_parts = []

        for section in sections:
            section_type = section.get('type', 'paragraph')
            content = section.get('content', '')

            if section_type == 'heading':
                level = section.get('level', 1)
                document_parts.append(self.add_heading(content, level))
            elif section_type == 'paragraph':
                document_parts.append(self.add_paragraph(content))
            elif section_type == 'code':
                language = section.get('language', '')
                document_parts.append(self.add_code_block(content, language))
            elif section_type == 'table':
                data = section.get('data', [])
                headers = section.get('headers')
                document_parts.append(self.add_table(data, headers))
            elif section_type == 'list':
                items = section.get('items', [])
                ordered = section.get('ordered', False)
                document_parts.append(self.add_list(items, ordered))
            else:
                document_parts.append(content)

        return '\n\n'.join(document_parts)


class ContentParser:
    """内容解析器"""

    @staticmethod
    def parse_ai_response(content: str) -> List[Dict[str, Any]]:
        """解析AI响应内容为结构化数据"""
        sections = []
        lines = content.split('\n')
        current_section = {'type': 'paragraph', 'content': ''}

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 检测标题（以#开头）
            if line.startswith('#'):
                if current_section['content']:
                    sections.append(current_section)

                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                current_section = {'type': 'heading', 'content': title, 'level': level}
                sections.append(current_section)
                current_section = {'type': 'paragraph', 'content': ''}

            # 检测代码块（以```开头和结尾）
            elif line.startswith('```'):
                if current_section['content']:
                    sections.append(current_section)

                language = line[3:].strip()
                code_lines = []
                i += 1

                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1

                sections.append({
                    'type': 'code',
                    'content': '\n'.join(code_lines),
                    'language': language
                })
                current_section = {'type': 'paragraph', 'content': ''}

            # 检测列表项（以-或*开头，或数字.开头）
            elif line.startswith(('-', '*')) or (line and line[0].isdigit() and '.' in line[:5]):
                if current_section['content']:
                    sections.append(current_section)

                list_items = []
                ordered = line[0].isdigit()

                while i < len(lines):
                    line = lines[i].strip()
                    if line.startswith(('-', '*')):
                        list_items.append(line[1:].strip())
                    elif line and line[0].isdigit() and '.' in line[:5]:
                        list_items.append(line.split('.', 1)[1].strip())
                    elif line == '':
                        break
                    else:
                        i -= 1
                        break
                    i += 1

                if list_items:
                    sections.append({
                        'type': 'list',
                        'items': list_items,
                        'ordered': ordered
                    })

                current_section = {'type': 'paragraph', 'content': ''}
                continue

            # 普通文本段落
            else:
                if line:
                    if current_section['content']:
                        current_section['content'] += '\n' + line
                    else:
                        current_section['content'] = line
                elif current_section['content']:
                    sections.append(current_section)
                    current_section = {'type': 'paragraph', 'content': ''}

            i += 1

        # 添加最后一个段落
        if current_section['content']:
            sections.append(current_section)

        return sections

    @staticmethod
    def extract_tables_from_markdown(content: str) -> List[Dict[str, Any]]:
        """从Markdown内容中提取表格"""
        tables = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 检测表格（包含|字符的行）
            if '|' in line and line.count('|') >= 2:
                table_lines = []

                # 收集表格行
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i].strip())
                    i += 1

                if len(table_lines) >= 2:
                    # 解析表格
                    headers = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]

                    # 跳过分隔符行
                    data_start = 1
                    if len(table_lines) > 1 and all(c in '-|: ' for c in table_lines[1]):
                        data_start = 2

                    data = []
                    for line in table_lines[data_start:]:
                        row = [cell.strip() for cell in line.split('|')[1:-1]]
                        if len(row) == len(headers):
                            data.append(row)

                    if data:
                        tables.append({
                            'type': 'table',
                            'headers': headers,
                            'data': data
                        })

                continue

            i += 1

        return tables
