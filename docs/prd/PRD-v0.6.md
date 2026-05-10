# Interview Bible v0.6 PRD：Print Pack + PDF导出

> 目标：把结构化的卡片内容导出成可打印、可分享的PDF

---

## 0. 核心思路：分步生成，脚本合并

### 为什么不一次性生成PDF？
- 内容太长 → LLM上下文不够
- 容易乱 → 目录和内容对应不上
- 复用性差 → 单独一篇文章改了又要重新生成全本

### 正确步骤
```text
1. 生成目录（大纲）
   ↓
2. 按目录里的每一章，分别生成对应的篇章PDF
   ↓
3. 脚本把所有篇章PDF + 目录PDF合并成完整PDF
```

---

## 1. 文件结构

```text
exports/
  {session}/
    00-目录.pdf
    01-编程语言.pdf
    02-数据结构与算法.pdf
    ...
    {session}-完整.pdf
    markdown/
      00-目录.md
      01-编程语言.md
      ...
      {session}-完整.md
```

---

## 2. 新增脚本

### scripts/build-print-pack.py
```python
输入：exports/{session}/cards/目录，或用户指定的主题列表
输出：markdown完整包 + 完整目录.md
```

### scripts/build-pdf.py
```python
输入：markdown目录
输出：单页PDF + 完整PDF
```

支持中文显示，支持分页，支持目录跳转。

---

## 3. 目录模板

### 小白版Go后端PDF目录示例
```
# Go后端面试备考手册（小白版）

## 目录
1. 编程语言：Go基础
   - goroutine/channel
   - context
   - defer/panic/recover

2. 数据结构与算法
   - 常见排序算法
   - 链表/树/哈希表
   - LeetCode高频题

3. 数据库
   - MySQL索引
   - MVCC
   - 事务隔离级别

...
```

---

## 4. 技术选型

- Markdown → PDF：用 `pandoc` + LaTeX 引擎
- 合并PDF：用 `pypdf`
- 中文支持：用 `ctex` 宏包

---

## 5. v0.6验收标准

- ✅ 能从cards目录生成完整Markdown包
- ✅ 能从Markdown生成单页PDF
- ✅ 能合并成完整PDF（目录+各章节）
- ✅ 中文正常显示
- ✅ 目录有跳转链接
- ✅ 分页合理
- ✅ 脚本化一键生成
```
