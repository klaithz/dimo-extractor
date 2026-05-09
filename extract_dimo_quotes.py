#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SEPARATOR = "- - - -"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FOOTER_RE = re.compile(r"^\*此文档通过 .* 导出$")


def extract_quotes(text: str) -> str:
    lines = text.splitlines()

    try:
        first_sep = lines.index(SEPARATOR)
    except ValueError as exc:
        raise ValueError("未找到正文起始分隔线 '- - - -'") from exc

    content_lines = lines[first_sep + 1 :]
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in content_lines:
        if line == SEPARATOR:
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line)

    if current:
        blocks.append(current)

    quotes: list[str] = []
    for block in blocks:
        trimmed = [line.rstrip() for line in block]
        while trimmed and trimmed[0] == "":
            trimmed.pop(0)
        while trimmed and trimmed[-1] == "":
            trimmed.pop()

        if not trimmed:
            continue
        if len(trimmed) == 1 and FOOTER_RE.match(trimmed[0]):
            continue
        if DATE_RE.match(trimmed[-1]):
            trimmed = trimmed[:-1]
            while trimmed and trimmed[-1] == "":
                trimmed.pop()

        if not trimmed:
            continue
        quotes.append("\n".join(trimmed))

    if not quotes:
        raise ValueError("未提取到书摘，请确认文件格式是否仍与当前样本一致")

    return "\n\n".join(quotes) + "\n"


def build_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_仅书摘{input_path.suffix}")


def process_file(input_path: Path, output_path: Path | None = None) -> Path:
    resolved_input = input_path.expanduser().resolve()
    resolved_output = output_path.expanduser().resolve() if output_path else build_output_path(resolved_input)

    text = resolved_input.read_text(encoding="utf-8")
    result = extract_quotes(text)
    resolved_output.write_text(result, encoding="utf-8")
    return resolved_output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="提取滴墨书摘导出文本中的书摘正文，去掉头部、日期、分隔线和尾部声明。"
    )
    parser.add_argument("input", nargs="+", type=Path, help="输入的滴墨书摘导出 .txt 文件，可一次传入多个")
    parser.add_argument("-o", "--output", type=Path, help="输出文件路径")
    args = parser.parse_args()

    if args.output and len(args.input) > 1:
        parser.error("一次传入多个输入文件时，不能同时指定单个 --output 路径")

    had_error = False
    for index, input_path in enumerate(args.input):
        output_path = args.output if index == 0 else None
        try:
            written_path = process_file(input_path, output_path)
            print(f"已生成: {written_path}")
        except FileNotFoundError:
            had_error = True
            print(f"处理失败: {input_path} -> 文件不存在或无法访问", file=sys.stderr)
        except UnicodeDecodeError:
            had_error = True
            print(f"处理失败: {input_path} -> 不是 UTF-8 编码文本，请先转换编码后再试", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            had_error = True
            print(f"处理失败: {input_path} -> {exc}", file=sys.stderr)

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
