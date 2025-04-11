import io
import json
import re
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.history import History


def _register_fonts():
    """获取字体文件的绝对路径"""
    current_dir = Path(__file__).parent  # services目录
    project_root = current_dir.parent.parent  # 假设services在app/下
    font_path = project_root / "app" / "fonts" / "simsun.ttf"

    if not font_path.exists():
        raise FileNotFoundError(f"字体文件不存在于: {font_path}")

    """ 注册中文字体（单例初始化）"""
    pdfmetrics.registerFont(TTFont('SimSun', font_path))


def _create_styles():
    """样式工厂方法"""
    return {
        "normal": ParagraphStyle(
            "Normal",
            fontName="SimSun",
            fontSize=12,
            leading=14,
            textColor=colors.black,
            wordWrap='CJK',
        ),
        "fake": ParagraphStyle(
            "Fake",
            fontName="SimSun",
            fontSize=12,
            leading=14,
            textColor=colors.black,
            backColor=colors.yellow,
            borderPadding=(2, 2, 2, 2),
        )
    }


def process_text(text: str):
    return re.sub(
        r'<fake>(.*?)</fake>',
        r'<span backcolor="yellow">\1</span>',
        text,
        flags=re.DOTALL
    )


class ReportService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        _register_fonts()
        self.styles = _create_styles()
        self.db = db

    async def get_pdf(self, text_id: int):
        # 假设通过数据库会话获取 item
        result = self.db.query(History.detail).filter(History.id == text_id).scalar()

        data_dict = json.loads(result)  # 解析 JSON 字符串为字典

        # 提取目标值
        marked_text = data_dict.get("marked_text")

        # 创建PDF字节流
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm
        )

        # 构建内容
        content = process_text(marked_text)
        story = [Paragraph(content, self.styles['normal'])]
        doc.build(story)

        # 准备响应
        buffer.seek(0)
        return buffer
