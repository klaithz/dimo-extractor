# Dimo Extractor

`Dimo Extractor` 是一个用于提取滴墨书摘导出 `.txt` 文件中“纯书摘内容”的小工具。

它会自动去掉导出文件里的头部说明、分隔线、日期和尾部声明，并在原文件目录生成一个只保留书摘的新文本文件。

## 功能

- 支持一次处理一个或多个滴墨导出的 `.txt` 文件
- 支持 Finder 拖拽使用
- 支持命令行批量处理
- 输出文件保存在原文件所在目录

## 环境要求

- macOS
- Python 3

大多数 macOS 环境已经自带 `python3`。如果你的系统里没有，可以先安装 Python 3 再使用。

## 文件说明

- `extract_dimo_quotes.py`：核心提取脚本
- `Drag TXT Here.app`：适合 Finder 拖拽使用的应用
- `Drag TXT Here.js`：`Drag TXT Here.app` 的源码（JXA）
- `Drag TXT Here.command`：命令行/脚本入口

## 安装

1. 下载或克隆这个仓库
2. 确认系统中可以运行 `python3`
3. 直接使用 `Drag TXT Here.app`，或者在终端里运行 Python 脚本

## 使用方法

### 方式一：Finder 拖拽

把一个或多个滴墨导出的 `.txt` 文件拖到 `Drag TXT Here.app` 上。

处理完成后，会在原文件所在目录生成新文件：

```text
原文件名_仅书摘.txt
```

### 方式二：命令行

处理单个文件：

```bash
python3 extract_dimo_quotes.py /path/to/input.txt
```

处理多个文件：

```bash
python3 extract_dimo_quotes.py /path/to/one.txt /path/to/two.txt
```

也可以手动指定输出路径：

```bash
python3 extract_dimo_quotes.py /path/to/input.txt -o /path/to/output.txt
```

## 输出示例

输入文件：

```text
书名等头部信息
- - - -

第一条书摘
2026-01-02
- - - -

第二条书摘
2026-01-03
- - - -
*此文档通过 滴墨书摘 导出
```

输出文件：

```text
第一条书摘

第二条书摘
```

## 注意事项

- 当前按滴墨现有导出格式进行提取
- 输入文件应为 UTF-8 编码文本
- 如果滴墨后续修改导出格式，脚本可能需要一起调整
