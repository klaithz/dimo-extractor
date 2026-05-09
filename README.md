# Dimo Extractor

A simple formatter for Dimo exports on macOS.

`Dimo Extractor` turns raw `.txt` files exported from 滴墨书摘 into clean, quote-only text files by removing headers, separators, trailing dates, and the export footer.

## Highlights

- Finder drag-and-drop workflow on macOS
- Command-line workflow for batch processing
- Clean source repository with rebuildable app output
- Output files are written next to the original export as `*_仅书摘.txt`

## Requirements

- macOS
- Python 3
- `osacompile` (included with macOS)

## Quick Start

### Terminal

```bash
python3 extract_dimo_quotes.py /path/to/input.txt
```

Multiple files:

```bash
python3 extract_dimo_quotes.py /path/to/one.txt /path/to/two.txt
```

Custom output path:

```bash
python3 extract_dimo_quotes.py /path/to/input.txt -o /path/to/output.txt
```

### Build the Finder App

```bash
chmod +x build_app.sh
./build_app.sh
```

This generates a standalone app bundle at:

```text
dist/Dimo Extractor.app
```

You can then drag one or more exported `.txt` files onto that app in Finder.

## Repo Layout

- `extract_dimo_quotes.py`: quote extraction logic
- `Drag TXT Here.js`: JXA source for the drag-and-drop app
- `Drag TXT Here.command`: direct shell entry point
- `build_app.sh`: one-step app build script

## Example

Input:

```text
Book metadata
- - - -

First quote
2026-01-02
- - - -

Second quote
2026-01-03
- - - -
*此文档通过 滴墨书摘 导出
```

Output:

```text
First quote

Second quote
```

## Notes

- The parser targets the current Dimo export format
- Input files should be UTF-8 encoded
- If Dimo changes its export layout, the parser may need an update

## License

MIT. See [LICENSE](./LICENSE).
