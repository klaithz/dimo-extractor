#!/bin/zsh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/extract_dimo_quotes.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "未找到处理脚本: $PYTHON_SCRIPT"
  echo
  read -r "?按回车键退出..."
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "请把一个或多个滴墨书摘导出的 .txt 文件拖到这个脚本上。"
  echo
  read -r "?按回车键退出..."
  exit 1
fi

args=()
for file_path in "$@"; do
  if [[ ! -f "$file_path" ]]; then
    echo "已跳过不存在的项目或非文件项目: $file_path"
  elif [[ "${file_path:l}" == *.txt ]]; then
    args+=("$file_path")
  else
    echo "已跳过非 .txt 文件: $file_path"
  fi
done

if [ "${#args[@]}" -eq 0 ]; then
  echo "没有收到可处理的 .txt 文件。"
  echo
  read -r "?按回车键退出..."
  exit 1
fi

python3 "$PYTHON_SCRIPT" "${args[@]}"
exit_code=$?

echo
if [ "$exit_code" -eq 0 ]; then
  echo "处理完成。输出文件已生成在原始文本所在目录。"
else
  echo "处理过程中有错误，请看上面的提示。"
fi

read -r "?按回车键退出..."
exit "$exit_code"
