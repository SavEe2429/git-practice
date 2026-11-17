#!/usr/bin/env python3
"""
Generate editable Microsoft Word (.docx) Lab Sheets (LAB00..LAB06) into docs/labs/
matching LAB00..LAB06.pdf, with student info header, copy-paste ready
code boxes, editable answer/screenshot paste boxes, and reference images.
"""

import html
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_labs import DOCS_DIR, LABS, LABS_DIR  # noqa: E402

STRONG_RE = re.compile(r"(<strong>.*?</strong>)", re.DOTALL)
CODE_RE = re.compile(r"(<code>.*?</code>)", re.DOTALL)


def _emit_code_aware(paragraph, fragment: str, base_size: float, color, bold: bool) -> None:
    for sub in CODE_RE.split(fragment):
        if not sub:
            continue
        if sub.startswith("<code>") and sub.endswith("</code>"):
            run = paragraph.add_run(html.unescape(sub[6:-7]))
            run.bold = bold
            run.font.name = "Consolas"
            run.font.size = Pt(base_size - 1.0)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        else:
            run = paragraph.add_run(html.unescape(sub))
            run.bold = bold
            run.font.name = "Leelawadee UI"
            run.font.size = Pt(base_size)
            run.font.color.rgb = color


def add_rich_runs(paragraph, html_text: str, base_size: float = 10.5, base_color=None) -> None:
    color = base_color or RGBColor(0x00, 0x00, 0x00)
    for part in STRONG_RE.split(html_text):
        if not part:
            continue
        if part.startswith("<strong>") and part.endswith("</strong>"):
            _emit_code_aware(paragraph, part[8:-9], base_size, color, bold=True)
        else:
            _emit_code_aware(paragraph, part, base_size, color, bold=False)


def set_cell_shading(cell, fill_hex: str) -> None:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_borders(cell, color: str = "475569", sz: str = "6") -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tcPr.append(borders)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_row_min_height(row, height_twips: int) -> None:
    trPr = row._tr.get_or_add_trPr()
    trHeight = OxmlElement("w:trHeight")
    trHeight.set(qn("w:val"), str(height_twips))
    trHeight.set(qn("w:hRule"), "atLeast")
    trPr.append(trHeight)


def add_section_heading(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Leelawadee UI"
    run.font.size = Pt(11.5)
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)


def _trailing_blank_paragraphs(doc: Document) -> int:
    count = 0
    for el in reversed(doc.element.body):
        if el.tag.endswith("}p"):
            text = "".join(el.itertext()).strip()
            if text or el.xpath(".//*[local-name()='drawing']"):
                break
            count += 1
        else:
            break
    return count


def _ensure_blank_lines(doc: Document, count: int = 2) -> None:
    missing = max(0, count - _trailing_blank_paragraphs(doc))
    for _ in range(missing):
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(2)


def add_code_box(doc: Document, code_text: str, dark: bool = False) -> None:
    """Insert generous two-line blank spacing before and after every code block."""
    _ensure_blank_lines(doc, 2)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.7)
    set_cell_shading(cell, "0F172A" if dark else "F8FAD2")
    set_cell_borders(cell, color="334155" if dark else "475569", sz="6")
    set_cell_margins(cell, top=110, bottom=110, left=140, right=140)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0) if dark else RGBColor(0x0F, 0x17, 0x2A)
    _ensure_blank_lines(doc, 2)


def add_picture_block(doc: Document, img_path: Path, caption: str, width_inches: float = 6.4) -> None:
    """Insert generous two-line blank spacing before and after every screenshot."""
    _ensure_blank_lines(doc, 2)

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(0)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(str(img_path), width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(2)
    rc = p_cap.add_run(caption)
    rc.italic = True
    rc.font.name = "Leelawadee UI"
    rc.font.size = Pt(9)
    rc.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    _ensure_blank_lines(doc, 2)


def add_paste_box(doc: Document, placeholder: str, min_height_inches: float = 0.9) -> None:
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_row_min_height(tbl.rows[0], int(min_height_inches * 1440))
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.7)
    set_cell_shading(cell, "FFFFFF")
    set_cell_borders(cell, color="333333", sz="6")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(placeholder)
    run.italic = True
    run.font.name = "Leelawadee UI"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)


def build_docx(lab: dict) -> Path:
    doc = Document()

    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # Header & Footer
    hdr = section.header.paragraphs[0]
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hdr.add_run("DOIT ESP32 DevKit v1 • PlatformIO Workshop | Git, Pre-commit, Testing & CI/CD")
    hrun.font.name = "Leelawadee UI"
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    ftr = section.footer.paragraphs[0]
    ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    frun = ftr.add_run(f"{lab['slug']} — Student Worksheet (.docx)")
    frun.font.name = "Leelawadee UI"
    frun.font.size = Pt(8.5)
    frun.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(2)
    title_p.paragraph_format.space_after = Pt(10)
    trun = title_p.add_run(html.unescape(lab["title"]))
    trun.bold = True
    trun.underline = True
    trun.font.name = "Leelawadee UI"
    trun.font.size = Pt(14)
    trun.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Student Info Table
    info_tbl = doc.add_table(rows=4, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_rows = [
        ("ชื่อ-นามสกุล (Student Name):", ""),
        ("รหัสนักศึกษา (Student ID):", ""),
        ("วันที่ปฏิบัติการ (Date):", ""),
        ("GitHub Repository URL:", "https://github.com/<your-username>/git-practice"),
    ]
    for idx, (label, default_val) in enumerate(info_rows):
        c0, c1 = info_tbl.rows[idx].cells
        c0.width = Inches(2.3)
        c1.width = Inches(4.4)
        set_cell_shading(c0, "FFFFFF")
        set_cell_shading(c1, "FFFFFF")
        set_cell_borders(c0, color="000000", sz="4")
        set_cell_borders(c1, color="000000", sz="4")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = "Leelawadee UI"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(default_val)
        r1.font.name = "Leelawadee UI"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x44, 0x44, 0x44) if default_val else RGBColor(0x00, 0x00, 0x00)

    # 1. Objectives
    add_section_heading(doc, "1. วัตถุประสงค์การเรียนรู้ (Objective)")
    for i, obj in enumerate(lab["objectives"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        add_rich_runs(p, f"{i}. {obj}")

    # 2. Learning Outcomes
    add_section_heading(doc, "2. ผลลัพธ์การเรียนรู้ (Learning Outcomes)")
    for i, out in enumerate(lab["outcomes"], 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        add_rich_runs(p, f"{i}. {out}")

    # 3. Tools
    add_section_heading(doc, "3. เครื่องมือและไฟล์ที่ต้องเตรียม (Tools & Prerequisites)")
    for tool in lab["tools"]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        add_rich_runs(p, f"• {tool}")

    # 4. Experiments
    add_section_heading(doc, "4. การทดลอง (Experiments)")
    for code, desc in lab["experiments"]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"{code}: ")
        r.bold = True
        r.underline = True
        r.font.name = "Leelawadee UI"
        r.font.size = Pt(10.5)
        add_rich_runs(p, desc)

    # 5. Step-by-Step Details (Split Code Parts + Inline How-to Screenshots)
    add_section_heading(doc, "5. รายละเอียดการทดลองและขั้นตอนปฏิบัติ (Step-by-Step Guide & Code)")
    for item in lab["details"]:
        if isinstance(item, dict):
            heading = item["heading"]
            desc = item.get("desc", "")
            code = item.get("code", "")
            imgs = item.get("images", [])
        else:
            heading, code = item
            desc, imgs = "", []
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(html.unescape(heading))
        r.bold = True
        r.font.name = "Leelawadee UI"
        r.font.size = Pt(10)
        if desc:
            p_desc = doc.add_paragraph()
            p_desc.paragraph_format.left_indent = Inches(0.15)
            p_desc.paragraph_format.space_before = Pt(0)
            p_desc.paragraph_format.space_after = Pt(3)
            p_desc.paragraph_format.keep_with_next = True
            add_rich_runs(p_desc, desc, base_size=9.5, base_color=RGBColor(0x33, 0x41, 0x55))
        if code:
            add_code_box(doc, code, dark=False)
        for rel_src, cap in imgs:
            img_path = (DOCS_DIR / "labs_html" / rel_src).resolve()
            if img_path.exists():
                add_picture_block(doc, img_path, cap, width_inches=6.4)

    # 6. Expected Output
    add_section_heading(doc, "6. ตัวอย่างผลลัพธ์ใน Terminal (Expected Output)")
    add_code_box(doc, lab["expected_output"], dark=True)

    # 7. Student Results & Screenshots
    add_section_heading(doc, "7. บันทึกผลการทดลองของนักเรียน (Results & Screenshots)")
    for res in lab["results"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        add_rich_runs(p, res)
        add_paste_box(doc, "[วางผลลัพธ์ Terminal หรือข้อความคำตอบที่นี่]", min_height_inches=0.85)

    p_shot = doc.add_paragraph()
    p_shot.paragraph_format.space_after = Pt(3)
    p_shot.paragraph_format.keep_with_next = True
    r_shot = p_shot.add_run("ภาพหน้าจอหลักฐานการปฏิบัติการของนักเรียน (Student Screenshot):")
    r_shot.bold = True
    r_shot.font.name = "Leelawadee UI"
    r_shot.font.size = Pt(10)
    add_paste_box(doc, "[วางภาพหน้าจอ / Paste Screenshot ผลลัพธ์ของนักเรียนที่นี่]", min_height_inches=1.6)

    # 8. Observation and Questions
    add_section_heading(doc, "8. การสังเกตและตอบคำถาม (Observation and Questions)")
    for q in lab["questions"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        add_rich_runs(p, q)
        add_paste_box(doc, "[พิมพ์คำตอบของนักเรียนที่นี่]", min_height_inches=0.75)

    # 9. Exercise
    add_section_heading(doc, "9. แบบฝึกหัด (Exercise)")
    p_ex = doc.add_paragraph()
    p_ex.paragraph_format.space_after = Pt(3)
    r_ex = p_ex.add_run(f"{lab['exercise']['code']}: ")
    r_ex.bold = True
    r_ex.underline = True
    r_ex.font.name = "Leelawadee UI"
    r_ex.font.size = Pt(10.5)
    add_rich_runs(p_ex, lab["exercise"]["desc"])
    add_code_box(doc, lab["exercise"]["snippet"], dark=False)
    add_paste_box(doc, "[วางผลลัพธ์ verify.py หรือภาพหน้าจอส่งงานที่นี่]", min_height_inches=0.9)

    # 10. Reference Screenshots (1 per row, full width)
    add_section_heading(doc, "10. ภาพประกอบผลลัพธ์จริงสำหรับเทียบผล (Reference Screenshots)")
    for rel_src, cap in lab["screenshots"]:
        img_path = (DOCS_DIR / "labs_html" / rel_src).resolve()
        if img_path.exists():
            add_picture_block(doc, img_path, cap, width_inches=6.5)

    out_path = LABS_DIR / f"{lab['slug']}.docx"
    doc.save(out_path)
    print(f"Generated: labs/{out_path.name} ({out_path.stat().st_size} bytes)")
    return out_path


def main() -> None:
    for lab in LABS:
        build_docx(lab)


if __name__ == "__main__":
    main()
