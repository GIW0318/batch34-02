# GSB Bugfix Task
## 题面
每局开局随机生成洞穴，用 cellular automata 跑完以后经常出现玩家出生在封闭小洞里、地图只剩几堵墙、同一个种子重开却是另一张图的情况，策划没法复现关卡。procedural_cave.py 的 CaveMap(width, height, seed, fill) 需要用 seed 固定随机序列，generate(steps, birth, death) 反复统计八邻域墙数更新内部格子，四周边界永远保持墙体，相同 seed 必须得到完全相同的网格；connected 判断所有地板是否四连通，components 按面积从大到小返回各地板连通块的格子数；repair 在未连通时按固定顺序从最大块向其他块凿 L 形通道，返回被改成地板的墙格数量，已经连通返回 0，修完 connected 必须为真；state 返回包含 width、height 和 grid 的快照，修改快照不能影响地图；宽或高小于 5、fill 不在 0 到 1 之间、steps 为负、birth 与 death 取值不合法时抛 ValueError。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：游戏开发
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
