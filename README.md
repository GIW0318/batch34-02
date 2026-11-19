# GSB Bugfix Task
## 题面
弹幕关卡里上千颗子弹和玩家判定框每帧两两比较，帧率直接掉到个位数；换成四叉树粗筛后，子弹飞出边界删不掉，同一 id 重复插入把节点撑爆，查询结果顺序忽前忽后导致录像回放对不上，两个矩形只贴着一个角却漏配对。quadtree_broadphase.py 的 QuadtreeBroadphase 用 bounds=(x, y, w, h)、capacity 和 max_depth 建树，需要实现 insert、remove、update、query、pairs 和 state：矩形必须完整落在边界内且宽高为正，id 必须是唯一的非空字符串；一个节点超过容量且未到最大深度就四分；remove 未知 id 返回 False，update 未知 id 抛 ValueError；query 返回与查询矩形相交的全部 id，pairs 返回所有相交对象对，两者都按字典序排序，使插入顺序不影响结果；相交按闭区间计算，贴边也算命中；state 返回可以随意修改的快照。

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
