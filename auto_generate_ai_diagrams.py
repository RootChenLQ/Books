#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为所有缺少示意图的案例自动生成AI风格的系统配图，并将图片嵌入README。

设计目标：
1. 扫描 books/*/code/examples 下的所有案例
2. 判断README是否已有可用的本地图片引用
3. 读取案例文档，提取标题、关键段落、加粗关键词
4. 使用Matplotlib生成结构化信息图（含背景/模型/控制/结果等模块）
5. 在README标题后插入“系统示意图（AI自动生成）”板块
6. 输出处理报告，方便复验
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  # isort:skip
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402  # isort:skip

# 全局字体设置，兼容常见中文字体并回落到DejaVu Sans
FONT_CANDIDATES = [
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "Microsoft YaHei",
    "PingFang SC",
    "SimHei",
    "WenQuanYi Zen Hei",
    "WenQuanYi Micro Hei",
    "Arial Unicode MS",
    "DejaVu Sans",
]
plt.rcParams["font.sans-serif"] = FONT_CANDIDATES
plt.rcParams["axes.unicode_minus"] = False

MD_IMAGE_PATTERN = re.compile(r"!\[[^\]]*?\]\(([^)]+)\)")
HTML_IMAGE_PATTERN = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)

COLOR_PALETTES = [
    ("#e0f2ff", "#0369a1"),
    ("#f1f5f9", "#0f172a"),
    ("#fef3c7", "#b45309"),
    ("#f3e8ff", "#6b21a8"),
    ("#fdf2f8", "#be185d"),
    ("#dcfce7", "#15803d"),
    ("#fff7ed", "#9a3412"),
    ("#e0f7fa", "#006064"),
]


@dataclass
class CaseSnippet:
    """存放从README提取的核心信息"""

    book_slug: str
    book_display: str
    case_name: str
    readme_path: Path
    title: str
    sections: List[dict]
    keywords: List[str]
    summary: str


def shorten(text: str, limit: int = 140) -> str:
    """压缩文本长度，移除多余空白"""
    clean = re.sub(r"`+", "", text)
    clean = re.sub(r"[<>#]", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1].rstrip() + "…"


def wrap_lines(text: str, width: int = 26) -> str:
    """为图表文本进行自动换行"""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    return textwrap.fill(text, width=width)


def clean_bullet(text: str) -> str:
    """生成README侧栏要点"""
    text = re.sub(r"^[\-\*\d\.\)\s]+", "", text.strip())
    text = re.sub(r"`+", "", text)
    text = text.replace("|", "｜")
    return text.strip()


class CaseDiagramGenerator:
    """核心执行器"""

    def __init__(
        self,
        books_root: Path,
        book_filters: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.books_root = books_root
        self.book_filters = set(book_filters or [])
        self.limit = limit
        self.processed: List[dict] = []
        self.skipped: List[dict] = []
        self.failed: List[dict] = []

    def run(self) -> dict:
        """执行批处理"""
        cases = self._discover_cases()
        count = 0

        for case in cases:
            if self.limit and count >= self.limit:
                break

            needs_diagram = self._needs_diagram(case["readme"])
            if not needs_diagram:
                self.skipped.append(
                    self._case_record(
                        case, reason="已有图片或无法解析README"
                    )
                )
                continue

            try:
                snippet = self._extract_snippet(case)
                diagram_name = f"{case['dir'].name}_ai_diagram.png"
                diagram_path = case["dir"] / diagram_name

                self._create_diagram(snippet, diagram_path)
                added = self._inject_readme(snippet, diagram_name)

                self.processed.append(
                    self._case_record(
                        case,
                        diagram=diagram_name,
                        readme_updated=added,
                    )
                )
                count += 1
                print(
                    f"✅ {case['book']}/{case['dir'].name} → {diagram_name} "
                    f"({'已更新README' if added else 'README已存在AI段落'})"
                )
            except Exception as exc:  # noqa: BLE001
                self.failed.append(
                    self._case_record(case, error=repr(exc))
                )
                print(
                    f"❌ {case['book']}/{case['dir'].name} 生成失败: {exc}"
                )

        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "books_root": str(self.books_root),
            "total_cases": len(cases),
            "generated": len(self.processed),
            "skipped": len(self.skipped),
            "failed": len(self.failed),
            "details": {
                "generated": self.processed,
                "skipped": self.skipped,
                "failed": self.failed,
            },
        }
        return summary

    def _discover_cases(self) -> List[dict]:
        """遍历books目录，收集可处理的案例"""
        cases: List[dict] = []
        if not self.books_root.exists():
            return cases

        for book_dir in sorted(self.books_root.iterdir()):
            if not book_dir.is_dir():
                continue

            if self.book_filters and book_dir.name not in self.book_filters:
                continue

            examples_dir = book_dir / "code" / "examples"
            if not examples_dir.exists():
                continue

            for case_dir in sorted(examples_dir.iterdir()):
                if not case_dir.is_dir():
                    continue
                readme = case_dir / "README.md"
                if not readme.exists():
                    continue
                cases.append(
                    {
                        "book": book_dir.name,
                        "dir": case_dir,
                        "readme": readme,
                    }
                )
        return cases

    @staticmethod
    def _case_record(case: dict, **extra: dict) -> dict:
        record = {
            "book": case["book"],
            "case_dir": str(case["dir"]),
            "readme": str(case["readme"]),
        }
        record.update(extra)
        return record

    def _needs_diagram(self, readme_path: Path) -> bool:
        """判断README是否已经包含可用图片"""
        try:
            content = readme_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = readme_path.read_text(encoding="utf-8", errors="ignore")

        # 如果已经有AI段落则认为满足
        if "系统示意图（AI自动生成）" in content:
            return False

        case_dir = readme_path.parent

        def has_existing(images: List[str]) -> bool:
            for img in images:
                src = img.strip()
                if not src or src.startswith("http"):
                    continue
                candidate = (case_dir / src).resolve()
                if candidate.exists():
                    return True
            return False

        md_refs = MD_IMAGE_PATTERN.findall(content)
        html_refs = HTML_IMAGE_PATTERN.findall(content)

        return not has_existing(md_refs + html_refs)

    def _extract_snippet(self, case: dict) -> CaseSnippet:
        """从README提取标题、段落、关键词"""
        readme_path: Path = case["readme"]
        content = readme_path.read_text(encoding="utf-8", errors="ignore")

        title_match = re.search(r"^#\s+(.+)", content, flags=re.MULTILINE)
        title = (
            title_match.group(1).strip()
            if title_match
            else case["dir"].name.replace("_", " ")
        )

        sections = self._parse_sections(content)
        keywords = self._parse_keywords(content)

        summary = ""
        for section in sections:
            if section["snippet"]:
                summary = section["snippet"]
                break
        if not summary:
            summary = "参见案例正文了解模型与控制策略。"

        return CaseSnippet(
            book_slug=case["book"],
            book_display=self._display_name(case["book"]),
            case_name=case["dir"].name,
            readme_path=readme_path,
            title=title,
            sections=sections,
            keywords=keywords,
            summary=summary,
        )

    def _parse_sections(self, content: str) -> List[dict]:
        pattern = re.compile(
            r"^##\s+(.+?)\n(.*?)(?=^##\s+|^#\s+|$\Z)",
            flags=re.MULTILINE | re.DOTALL,
        )
        sections: List[dict] = []

        for heading, body in pattern.findall(content):
            snippet = self._extract_first_sentence(body)
            if snippet:
                sections.append(
                    {
                        "heading": heading.strip(),
                        "snippet": snippet,
                    }
                )
            if len(sections) >= 6:
                break

        if not sections:
            fallback = self._extract_first_sentence(content)
            sections.append({"heading": "案例概览", "snippet": fallback})
        return sections

    def _extract_first_sentence(self, block: str) -> str:
        lines = []
        inside_code = False
        for raw in block.splitlines():
            stripped = raw.strip()
            if stripped.startswith("```"):
                inside_code = not inside_code
                continue
            if inside_code or not stripped:
                continue
            if stripped.startswith("!"):
                continue
            stripped = re.sub(r"^#+\s*", "", stripped)
            stripped = re.sub(r"^[\-\*\d\.\)\(]+\s*", "", stripped)
            stripped = stripped.strip()
            if not stripped:
                continue
            lines.append(stripped)
            break

        text = " ".join(lines)
        return shorten(text)

    def _parse_keywords(self, content: str) -> List[str]:
        candidates = re.findall(r"\*\*(.+?)\*\*", content)
        cleaned = []
        seen = set()
        for keyword in candidates:
            token = re.sub(r"[:：\s]+$", "", keyword.strip())
            token = re.sub(r"^\W+|\W+$", "", token)
            if not token or len(token) > 16:
                continue
            if token in seen:
                continue
            cleaned.append(token)
            seen.add(token)
            if len(cleaned) >= 6:
                break
        return cleaned

    def _create_diagram(self, snippet: CaseSnippet, output_path: Path) -> None:
        palette = COLOR_PALETTES[
            hash(snippet.case_name) % len(COLOR_PALETTES)
        ]
        bg_color, accent = palette

        fig, ax = plt.subplots(figsize=(12, 8), dpi=220)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        # 标题与副标题
        ax.text(
            0.5,
            0.95,
            snippet.title,
            ha="center",
            va="top",
            fontsize=22,
            fontweight="bold",
            color=accent,
        )
        ax.text(
            0.5,
            0.91,
            f"{snippet.book_display} · {snippet.case_name}",
            ha="center",
            va="top",
            fontsize=12,
            color="#475569",
        )

        # 描述信息
        ax.text(
            0.5,
            0.86,
            wrap_lines(snippet.summary, width=65),
            ha="center",
            va="top",
            fontsize=11,
            color="#0f172a",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="#f8fafc",
                edgecolor="#cbd5f5",
            ),
        )

        # 模块布局
        slots = [
            (0.05, 0.55),
            (0.55, 0.55),
            (0.05, 0.23),
            (0.55, 0.23),
        ]
        width = 0.4
        height = 0.28

        for idx, slot in enumerate(slots):
            if idx >= len(snippet.sections):
                break
            heading = snippet.sections[idx]["heading"]
            text = wrap_lines(snippet.sections[idx]["snippet"], width=28)
            x, y = slot

            box = FancyBboxPatch(
                (x, y),
                width,
                height,
                boxstyle="round,pad=0.02",
                linewidth=2,
                edgecolor=accent,
                facecolor=bg_color,
                alpha=0.9,
            )
            ax.add_patch(box)
            ax.text(
                x + width / 2,
                y + height - 0.04,
                heading,
                ha="center",
                va="top",
                fontsize=13,
                fontweight="bold",
                color=accent,
            )
            ax.text(
                x + 0.02,
                y + height - 0.10,
                text,
                ha="left",
                va="top",
                fontsize=11,
                color="#0f172a",
            )

        # 箭头显示流程
        arrow_pairs = [
            ((0.45, 0.69), (0.55, 0.69)),
            ((0.45, 0.37), (0.55, 0.37)),
            ((0.25, 0.55), (0.25, 0.51)),
            ((0.75, 0.55), (0.75, 0.51)),
        ]
        for start, end in arrow_pairs:
            arrow = FancyArrowPatch(
                posA=start,
                posB=end,
                arrowstyle="->",
                color=accent,
                linewidth=2,
                mutation_scale=15,
            )
            ax.add_patch(arrow)

        # 关键词标签
        if snippet.keywords:
            keyword_y = 0.08
            keyword_x = 0.05
            for keyword in snippet.keywords[:6]:
                ax.text(
                    keyword_x,
                    keyword_y,
                    f"- {keyword}",
                    fontsize=11,
                    ha="left",
                    va="center",
                    color="#334155",
                )
                keyword_x += 0.18
                if keyword_x > 0.8:
                    keyword_x = 0.05
                    keyword_y -= 0.05

        ax.text(
            0.5,
            0.02,
            "AI Diagram Generator · 自动解析案例文档并生成结构化示意图",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#94a3b8",
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, bbox_inches="tight")
        plt.close(fig)

    def _inject_readme(
        self,
        snippet: CaseSnippet,
        diagram_filename: str,
    ) -> bool:
        """将AI示意图段落插入README"""
        readme_path = snippet.readme_path
        content = readme_path.read_text(encoding="utf-8", errors="ignore")

        if diagram_filename in content or "系统示意图（AI自动生成）" in content:
            return False

        bullets = []
        for section in snippet.sections[:4]:
            bullet = clean_bullet(
                f"{section['heading']}：{section['snippet']}"
            )
            if bullet:
                bullets.append(shorten(bullet, 110))
        if not bullets:
            bullets = [shorten(snippet.summary, 110)]

        bullet_md = "\n".join(f"- {line}" for line in bullets)

        diagram_section = f"""
## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="{diagram_filename}" alt="{snippet.title}系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

{bullet_md}

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>
""".strip()

        title_match = re.search(r"^# .+?$", content, flags=re.MULTILINE)
        insert_pos = title_match.end() if title_match else 0
        new_content = (
            content[:insert_pos]
            + "\n\n"
            + diagram_section
            + "\n\n"
            + content[insert_pos:]
        )

        readme_path.write_text(new_content, encoding="utf-8")
        return True

    @staticmethod
    def _display_name(book_slug: str) -> str:
        return book_slug.replace("-", " ").title()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="自动为缺少示意图的案例生成AI配图"
    )
    parser.add_argument(
        "--books-root",
        default="books",
        help="书稿根目录（默认：books）",
    )
    parser.add_argument(
        "--book",
        nargs="*",
        help="仅处理指定书籍（可多选）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="限制生成案例数量（调试用）",
    )
    parser.add_argument(
        "--report",
        default="ai_diagram_generation_report.json",
        help="输出报告路径",
    )
    args = parser.parse_args()

    generator = CaseDiagramGenerator(
        books_root=Path(args.books_root).resolve(),
        book_filters=args.book,
        limit=args.limit,
    )
    summary = generator.run()

    report_path = Path(args.report).resolve()
    report_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"\n📄 处理报告已写入: {report_path} "
        f"(生成 {summary['generated']} 个示意图，"
        f"跳过 {summary['skipped']} 个，失败 {summary['failed']} 个)"
    )


if __name__ == "__main__":
    main()
