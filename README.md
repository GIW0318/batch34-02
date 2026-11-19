# GSB Bugfix Task
## 题面
塔防地图上几百个小兵同时追同一个基地，每个单位单独跑 A* 直接把 CPU 吃满；改成从基地倒推一张流场后，障碍格没挡住、绕路时累计代价算少、两个方向代价一样时不同小兵选的格子不同导致队伍分叉、基地放在石头上照样能算、被墙隔开的区域还给出了方向。flow_field.py 的 FlowField(width, height, blocked, costs) 需要实现 set_goal、compute、distance、direction 和 path：compute 从 goal 出发用 Dijkstra 反向松弛，只走四邻接，进入一格的代价为 1 加上 costs 中该格的额外费用，障碍格不可通行；distance 返回累计代价，不可达返回 None，goal 自身为 0；direction 返回通往代价更小邻格的单位步长，代价相同时先比行号再比列号，goal、障碍和不可达格返回 (0, 0)；path 从起点沿流场走到 goal，不可达返回空列表；宽高非正、障碍越界、goal 越界或落在障碍上、查询坐标越界都抛 ValueError。

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
