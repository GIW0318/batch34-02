# GSB Bugfix Task
## 题面
角色伸手抓取场景里的把手时，两段手臂用 FABRIK 解算，结果骨头被拉长、手掌永远差一点够不到目标、目标太远时整条手臂缩成一团，迭代次数也没人管，低帧率机器上每帧耗时忽高忽低。fabrik_ik.py 的 FabrikChain 用 lengths 与 base 构造，solve(target, tolerance, max_iterations) 返回从根部到末端的关节坐标列表；求解前先把链条沿 +x 方向按段长依次排开，够得到目标时末端要落进 tolerance，够不到时沿 base 到 target 的方向完全伸直、末端停在 reach 处；每轮先从末端向根部回推、再从根部向末端前推，任何时刻每段长度保持不变；last_iterations 记录实际轮数且不得超过 max_iterations；空 lengths、非正段长、非二维 base 或 target、非正 tolerance、max_iterations 小于 1、target 与 base 重合都抛 ValueError。

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
