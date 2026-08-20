# 第九纪元：中古战锤 - New Recruit 数据库

本仓库把用户提供的自定义《第九纪元：中古战锤》规则实现为 BattleScribe 2.03 / New Recruit 可读取的数据文件。

当前可用内容：

- `第九纪元：中古战锤.gst`：游戏系统、分值类型、属性栏、军队分类、通用装备、通用特殊物品和法系入口。
- `黑暗精灵.cat`：黑暗精灵 2026 beta1 的完整基础军队列表，以及黑暗精灵传奇人物。
- `巴托尼亚.cat`、`木精灵.cat`、`震旦天朝.cat`、`混沌矮人.cat`、`矮人群山王国.cat`、`混沌勇士.cat`：对应 2026 beta 军书的基础军表目录。
- 另有北方混沌部落、高等精灵、古墓王、混沌恶魔、绿皮、纳迦什军团、南方王国、人类帝国、食人魔王国、斯卡文鼠人、吸血鬼伯爵、吸血鬼海岸、蜥蜴人、野兽人、战争之犬雇佣兵、阿拉比、基斯里夫及印地共 18 个 2026 军表目录。
- `tools/build_data.py`、`tools/faction_books.py` 与 `tools/faction_books_batch2.json`：确定性生成器和结构化数据。每个对象使用永久内部键生成稳定 ID；修改显示名称、点数或描述不会改变 ID。
- `tests/validate_data.py`：XML、ID、引用、游戏系统关联、数值和明显约束冲突检查。

## 使用

在 New Recruit 中导入本仓库发布地址，或在本地测试时同时载入根目录中的 `.gst` 与 `.cat` 文件。

当前版本仍需在 New Recruit UI 中进行实际导入和交互测试，重点项目见 `IMPLEMENTATION_NOTES.md`。

## 开发流程

1. 先阅读 `AGENTS.md`、`SOURCES.md`、`RULE_QUESTIONS.md`。
2. 在 `tools/build_data.py` 中修改具有永久 `key` 的数据定义；不要为了重命名而更换 `key`。
3. 重新生成根目录数据文件：

   ```powershell
   python tools/build_data.py
   ```

4. 运行验证：

   ```powershell
   python -m unittest discover -s tests -p 'test_*.py' -v
   python tests/validate_data.py
   ```

5. 在 New Recruit 中验证点数、百分比分类、条件显示与错误提示。

## 版权

规则 PDF 仅用于理解和实现。仓库不包含原始 PDF、扫描件或大段原文，只保存军表生成所需的数据、短摘要与来源定位信息。
