# code-reviewer-lite

规则式**代码评审**：检查裸 eval/exec、os.system、shell=True、TODO、超长行、过短命名等，
输出问题清单与级别（high/medium/low）。零第三方依赖。

## 功能简介

- 危险调用：eval / exec / os.system / shell=True（high）；
- pickle.load（medium）；
- TODO/FIXME、超长行（>120）、过短函数名（low）；
- `review(source)` 返回 `[{line, level, message}, ...]`。

## 快速开始

```bash
python3 code_reviewer.py --file some.py
echo 'eval(x)' | python3 code_reviewer.py
```

## 无 API key 如何运行

纯规则，**不需要任何 API key**。

## 目录结构

```
code-reviewer-lite/
├── code_reviewer.py
├── tests/test_code_reviewer.py
├── README.md / LICENSE / .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## 许可证

[MIT](./LICENSE) © 2026 ljiang9
