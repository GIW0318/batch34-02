# GSB Bugfix Task
## 题面
副本里的精英怪追人时总是贴着墙边走，导航网格相邻凸多边形之间的门（一组左右端点）喂给寻路后，该转的弯没转，角色先冲过头再折回来；门退化成一个点时就原地抖动；直接把起点和终点连起来又会穿墙。navmesh_funnel.py 需要提供 funnel_path(start, goal, portals)，用简单愚蠢漏斗算法做 string pulling：portals 按行进顺序给出每道门的 (left, right) 端点，维护 apex 与左右两条边界，新右端点越过左边界时把左端点收进路径并以它为新的 apex 重扫，左侧对称处理；左右端点重合的退化门照样参与收缩；空门列表返回起点到终点的直线；返回的路径只保留必要拐点，共线的中间点不要塞进去；路径首尾必须正好是 start 与 goal；起点终点重合只返回一个点；传入 None、单个点、三维点或非数字坐标时抛 ValueError。

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
