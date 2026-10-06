#!/usr/bin/env python3
"""code_reviewer —— 规则式代码评审。

检查项（输出问题清单与级别）：
  - 裸 eval / exec；
  - 危险调用：os.system / shell=True / pickle.load；
  - TODO / FIXME 注释；
  - 超长行（>120 字符）；
  - 过短命名（单字母除 i/j/k 外）。
零第三方依赖。

用法：
    from code_reviewer import review
    for issue in review(source_code): ...
"""
from __future__ import annotations

import argparse
import re
import sys

DANGEROUS = [
    (re.compile(r"\beval\s*\("), "high", "使用了裸 eval"),
    (re.compile(r"\bexec\s*\("), "high", "使用了裸 exec"),
    (re.compile(r"\bos\.system\s*\("), "high", "os.system 调用"),
    (re.compile(r"shell\s*=\s*True"), "high", "shell=True 有注入风险"),
    (re.compile(r"\bpickle\.load"), "medium", "pickle.load 反序列化不可信数据"),
]


def review(source: str) -> list[dict]:
    issues: list[dict] = []
    lines = source.splitlines()
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 危险调用
        for pat, level, msg in DANGEROUS:
            if pat.search(line):
                issues.append({"line": i, "level": level, "message": msg})
        # TODO / FIXME
        if "TODO" in line or "FIXME" in line:
            issues.append({"line": i, "level": "low", "message": "存在 TODO/FIXME 注释"})
        # 超长行
        if len(line) > 120:
            issues.append({"line": i, "level": "low", "message": f"行过长（{len(line)} 字符）"})
        # 过短命名：def x(  单字母
        m = re.match(r"\s*def\s+([a-zA-Z])\s*\(", line)
        if m and m.group(1) not in "ijk":
            issues.append({"line": i, "level": "low", "message": f"函数名过短：{m.group(1)}"})
    return issues


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="规则式代码评审")
    p.add_argument("--file", help="评审该 Python 文件")
    args = p.parse_args(argv)
    source = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    issues = review(source)
    if not issues:
        print("未发现问题。")
        return 0
    print(f"共 {len(issues)} 条问题：")
    for it in issues:
        print(f"  [行 {it['line']}] ({it['level']}) {it['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
