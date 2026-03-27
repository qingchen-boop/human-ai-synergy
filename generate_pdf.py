#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《人机共智：AI时代的协作思维与实践》PDF教材"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
# STHeiti not available, skip

# 颜色定义
PRIMARY = colors.HexColor('#2B5C9E')
SECONDARY = colors.HexColor('#4A90D9')
ACCENT = colors.HexColor('#F5A623')
LIGHT_BG = colors.HexColor('#F5F7FA')
TEXT = colors.HexColor('#333333')

def create_pdf():
    """创建 PDF 教材"""
    doc = SimpleDocTemplate(
        "/home/xiaoxi/.openclaw/workspace/projects/human-ai-synergy/人机共智-教材.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    FONT_NAME = 'STSong-Light'
    FONT_NAME_BOLD = 'STSong-Light'
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=FONT_NAME_BOLD,
        fontSize=28,
        textColor=PRIMARY,
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName=FONT_NAME_BOLD,
        fontSize=18,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=12,
    )
    
    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=FONT_NAME_BOLD,
        fontSize=14,
        textColor=SECONDARY,
        spaceBefore=15,
        spaceAfter=8,
    )
    
    heading3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontName=FONT_NAME_BOLD,
        fontSize=12,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=6,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=TEXT,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        textColor=TEXT,
        spaceAfter=3,
        leftIndent=15,
        leading=13
    )
    
    story = []
    
    # ===== 封面 =====
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("人机共智：AI时代的协作思维与实践", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Personal Empowerment in the AI Era", 
        ParagraphStyle('Subtitle', fontName=FONT_NAME, fontSize=14, textColor=SECONDARY, alignment=TA_CENTER)))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("AI时代个人能力提升指南", 
        ParagraphStyle('Desc', fontName=FONT_NAME, fontSize=11, textColor=TEXT, alignment=TA_CENTER)))
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("小曦 设计 | 2026年3月", 
        ParagraphStyle('Credit', fontName=FONT_NAME, fontSize=10, textColor=TEXT, alignment=TA_CENTER)))
    story.append(PageBreak())
    
    # ===== 目录 =====
    story.append(Paragraph("目录", heading1_style))
    story.append(Spacer(1, 0.3*cm))
    toc_items = [
        "第一章：学科纲要",
        "第二章：AI能力与局限",
        "第三章：人机协作策略",
        "第四章：AI批判与伦理",
        "第五章：AI时代个人发展",
        "第六章：前沿与未来",
        "第七章：实践练习集",
        "第八章：评估体系",
        "附录A：常见问题FAQ",
        "附录B：习题答案",
        "附录C：配套学习资源",
        "附录D：逻辑学基础（从零自学）",
    ]
    for item in toc_items:
        story.append(Paragraph(item, bullet_style))
    story.append(PageBreak())
    
    # ===== 文件读取函数 =====
    def read_md(filename):
        path = f"/home/xiaoxi/.openclaw/workspace/projects/human-ai-synergy/{filename}"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def md_to_text(md_content):
        """简单的 Markdown 转文本处理"""
        lines = md_content.split('\n')
        result = []
        in_code_block = False
        
        for line in lines:
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if line.startswith('> ') or line.startswith('# ') and '---' in line:
                continue
            if line.startswith('### '):
                result.append(('h3', line[4:].strip()))
            elif line.startswith('## '):
                result.append(('h2', line[3:].strip()))
            elif line.startswith('# '):
                result.append(('h1', line[2:].strip()))
            elif line.startswith('- [x]') or line.startswith('- [ ]'):
                continue
            elif line.startswith('- '):
                result.append(('bullet', line[2:].strip()))
            elif line.startswith('| '):
                continue
            elif line.strip() == '' or line.startswith('---'):
                result.append(('spacer', ''))
            elif line.startswith('*') and line.endswith('*'):
                result.append(('italic', line[1:-1].strip()))
            else:
                clean = line.replace('**', '').replace('*', '').replace('`', '').strip()
                if clean:
                    result.append(('para', clean))
        
        return result
    
    def add_md_file(filename):
        """添加一个 Markdown 文件到 PDF"""
        content = read_md(filename)
        if not content:
            return
        
        parts = md_to_text(content)
        
        for part in parts:
            if part[0] == 'h1':
                story.append(Paragraph(part[1], heading1_style))
            elif part[0] == 'h2':
                story.append(Paragraph(part[1], heading2_style))
            elif part[0] == 'h3':
                story.append(Paragraph(part[1], heading3_style))
            elif part[0] == 'bullet':
                story.append(Paragraph("· " + part[1], bullet_style))
            elif part[0] == 'para':
                story.append(Paragraph(part[1], body_style))
            elif part[0] == 'spacer':
                story.append(Spacer(1, 0.2*cm))
    
    # ===== 第一章：学科纲要 =====
    story.append(Paragraph("第一章：学科纲要", heading1_style))
    add_md_file("1-学科纲要.md")
    story.append(PageBreak())
    
    # ===== 第二章：AI能力与局限 =====
    story.append(Paragraph("第二章：AI能力与局限", heading1_style))
    add_md_file("2-模块一：AI能力与局限.md")
    story.append(Spacer(1, 0.3*cm))
    add_md_file("模块一补充案例.md")
    story.append(PageBreak())
    
    # ===== 第三章：人机协作策略 =====
    story.append(Paragraph("第三章：人机协作策略", heading1_style))
    add_md_file("3-模块二：人机协作策略.md")
    story.append(Spacer(1, 0.3*cm))
    add_md_file("模块二补充-提示工程模板库.md")
    story.append(PageBreak())
    
    # ===== 第四章：AI批判与伦理 =====
    story.append(Paragraph("第四章：AI批判与伦理", heading1_style))
    add_md_file("4-模块三：AI批判与伦理.md")
    story.append(Spacer(1, 0.3*cm))
    add_md_file("模块三补充-AI偏见真实案例库.md")
    story.append(PageBreak())
    
    # ===== 第五章：AI时代个人发展 =====
    story.append(Paragraph("第五章：AI时代个人发展", heading1_style))
    add_md_file("5-模块四：AI时代个人发展.md")
    story.append(Spacer(1, 0.3*cm))
    add_md_file("模块四补充-各职业的AI工作流示例.md")
    story.append(PageBreak())
    
    # ===== 第六章：前沿与未来 =====
    story.append(Paragraph("第六章：前沿与未来", heading1_style))
    add_md_file("6-模块五：前沿与未来.md")
    story.append(Spacer(1, 0.3*cm))
    add_md_file("模块五补充-AI最新动态与前沿案例.md")
    story.append(PageBreak())
    
    # ===== 第七章：实践练习集 =====
    story.append(Paragraph("第七章：实践练习集", heading1_style))
    add_md_file("7-实践练习集.md")
    story.append(PageBreak())
    
    # ===== 第八章：评估体系 =====
    story.append(Paragraph("第八章：评估体系", heading1_style))
    add_md_file("8-评估体系.md")
    story.append(PageBreak())
    
    # ===== 附录A：常见问题FAQ =====
    story.append(Paragraph("附录A：常见问题FAQ", heading1_style))
    add_md_file("常见问题FAQ.md")
    story.append(PageBreak())
    
    # ===== 附录B：习题答案 =====
    story.append(Paragraph("附录B：习题答案", heading1_style))
    add_md_file("习题答案.md")
    story.append(PageBreak())
    
    # ===== 附录C：配套学习资源 =====
    story.append(Paragraph("附录C：配套学习资源", heading1_style))
    add_md_file("配套学习资源.md")
    story.append(PageBreak())
    
    # ===== 附录D：逻辑学基础 =====
    story.append(Paragraph("附录D：逻辑学基础（从零自学）", heading1_style))
    add_md_file("7-模块六：逻辑思维基础.md")
    story.append(PageBreak())
    
    # ===== 结束页 =====
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("谢谢！", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("AI会越来越强，但你的判断力、创造力、同理心，", body_style))
    story.append(Paragraph("以及作为人的独特价值，永远不会被取代。", body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("学会与AI协作，成为更好的自己。", body_style))
    
    # 构建 PDF
    doc.build(story)
    print("PDF 教材已生成：人机共智-教材.pdf")

if __name__ == "__main__":
    create_pdf()
