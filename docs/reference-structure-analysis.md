# Reference Repository Structure Analysis

研究对象：[WHFB 6th Definitive Edition](https://github.com/lexicanum-imperialis/Warhammer-Fantasy-Battles-6th-Definitive-edition)。

## 可复用的实现模式

- 根目录保留 `.gst` 与各阵营 `.cat`。
- `.gst` 负责 cost types、profile types、跨阵营 categories、shared profiles、shared rules、shared selection entries 与 shared selection entry groups。
- `.cat` 负责阵营 publications、units、options、阵营共享对象和 force entries。
- 单位数量使用 selection constraints；按模型成本使用 modifier + repeat；条件显示使用 hidden modifier + condition。
- 条件改类使用 `add` / `remove` / `set-primary` category modifiers。
- 条件上限修改直接针对 constraint ID，避免只写说明文字。

## 未复用的规则内容

- Lord / Hero / Core / Special / Rare 类别。
- 参考仓库的点数、属性、装备、法术、特殊规则、军队数量配额和 Border Patrol 规则。
- 参考仓库的任何阵营列表或社区裁定。

## 本项目的结构选择

- 使用人物 / 核心 / 特殊 / 劫掠者 / 兽栏的点数百分比约束。
- 通过对子选择分类来只把特定坐骑成本计入兽栏。
- 通过条件 category modifiers 处理 `[R]` 替换分类与恐惧之主核心转换。
- 使用永久内部 key 生成稳定 ID，减少手工 ID 碰撞和无意义 ID 变动。

