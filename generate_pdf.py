#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成人机协作学 PDF 教材"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# 颜色定义
PRIMARY = colors.HexColor('#2B5C9E')
SECONDARY = colors.HexColor('#4A90D9')
ACCENT = colors.HexColor('#F5A623')
LIGHT_BG = colors.HexColor('#F5F7FA')
TEXT = colors.HexColor('#333333')

def create_pdf():
    """创建 PDF 教材"""
    doc = SimpleDocTemplate(
        "/home/xiaoxi/.openclaw/workspace/projects/human-ai-synergy/人机协作学-教材.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=PRIMARY,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=PRIMARY,
        spaceBefore=25,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=SECONDARY,
        spaceBefore=18,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=ACCENT,
        spaceBefore=12,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=16
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT,
        spaceAfter=4,
        leftIndent=20,
        leading=14
    )
    
    story = []
    
    # ===== 封面 =====
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("人机协作学", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Personal Empowerment in the AI Era", 
        ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=16, textColor=SECONDARY, alignment=TA_CENTER)))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("—— AI时代个人能力提升指南 ——", 
        ParagraphStyle('Desc', parent=styles['Normal'], fontSize=12, textColor=TEXT, alignment=TA_CENTER)))
    story.append(PageBreak())
    
    # ===== 目录 =====
    story.append(Paragraph("目录", heading1_style))
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
            # 跳过文件头部的元信息
            if line.startswith('> ') or line.startswith('# ') and '---' in line:
                continue
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            
            # 处理标题
            if line.startswith('### '):
                result.append(('h3', line[4:].strip()))
            elif line.startswith('## '):
                result.append(('h2', line[3:].strip()))
            elif line.startswith('# '):
                result.append(('h1', line[2:].strip()))
            elif line.startswith('**') and line.endswith('**'):
                result.append(('bold', line[2:-2].strip()))
            elif line.startswith('- [x]') or line.startswith('- [ ]'):
                continue  # 跳过复选框
            elif line.startswith('- '):
                result.append(('bullet', line[2:].strip()))
            elif line.startswith('| '):
                continue  # 跳过表格（简化处理）
            elif line.strip() == '' or line.startswith('---'):
                result.append(('spacer', ''))
            elif line.startswith('*') and line.endswith('*'):
                result.append(('italic', line[1:-1].strip()))
            else:
                # 清理 Markdown 特殊符号
                clean = line.replace('**', '').replace('*', '').replace('`', '').strip()
                if clean:
                    result.append(('para', clean))
        
        return result
    
    def add_md_file(filename, title_override=None):
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
            elif part[0] == 'bold':
                story.append(Paragraph(f"<b>{part[1]}</b>", body_style))
            elif part[0] == 'italic':
                story.append(Paragraph(f"<i>{part[1]}</i>", body_style))
            elif part[0] == 'bullet':
                story.append(Paragraph(f"• {part[1]}", bullet_style))
            elif part[0] == 'para':
                story.append(Paragraph(part[1], body_style))
            elif part[0] == 'spacer':
                story.append(Spacer(1, 0.3*cm))
    
    # ===== 第一章：学科纲要 =====
    story.append(Paragraph("第一章：学科纲要", heading1_style))
    add_md_file("1-学科纲要.md")
    story.append(PageBreak())
    
    # ===== 第二章：AI能力与局限 =====
    story.append(Paragraph("第二章：AI能力与局限", heading1_style))
    add_md_file("2-模块一：AI能力与局限.md")
    story.append(Spacer(1, 0.5*cm))
    add_md_file("模块一补充案例.md")
    story.append(PageBreak())
    
    # ===== 第三章：人机协作策略 =====
    story.append(Paragraph("第三章：人机协作策略", heading1_style))
    add_md_file("3-模块二：人机协作策略.md")
    story.append(Spacer(1, 0.5*cm))
    add_md_file("模块二补充-提示工程模板库.md")
    story.append(PageBreak())
    
    # ===== 第四章：AI批判与伦理 =====
    story.append(Paragraph("第四章：AI批判与伦理", heading1_style))
    add_md_file("4-模块三：AI批判与伦理.md")
    story.append(Spacer(1, 0.5*cm))
    add_md_file("模块三补充-AI偏见真实案例库.md")
    story.append(PageBreak())
    
    # ===== 第五章：AI时代个人发展 =====
    story.append(Paragraph("第五章：AI时代个人发展", heading1_style))
    add_md_file("5-模块四：AI时代个人发展.md")
    story.append(Spacer(1, 0.5*cm))
    add_md_file("模块四补充-各职业的AI工作流示例.md")
    story.append(PageBreak())
    
    # ===== 第六章：前沿与未来 =====
    story.append(Paragraph("第六章：前沿与未来", heading1_style))
    add_md_file("6-模块五：前沿与未来.md")
    story.append(Spacer(1, 0.5*cm))
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
    story.append(Spacer(1, 1*cm))
    
    # ===== 后记：学科宣言 =====
    story.append(Paragraph("后记：学科宣言", heading1_style))
    add_md_file("10-学科宣言.md")
    
    # ===== 结束页 =====
    story.append(PageBreak())
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("谢谢！", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("AI会越来越强，但你的判断力、创造力、同理心<br/>以及作为人的独特价值，永远不会被取代。<br/><br/>学会与AI协作，成为更好的自己。", 
        ParagraphStyle('EndNote', parent=styles['Normal'], fontSize=12, textColor=TEXT, alignment=TA_CENTER, leading=20)))
    
    # 构建 PDF
    doc.build(story)
    print("PDF 教材已生成：人机协作学-教材.pdf")

if __name__ == "__main__":
    create_pdf()
