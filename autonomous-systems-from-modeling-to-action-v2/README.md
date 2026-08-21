# 从模型到行动：自主系统的统一方法

**副标题：建模、估计、规划、控制、执行与学习**

本书以自主系统闭环为最高层知识框架：

**物理世界 → 建模（Modeling）→ 估计（Estimation）→ 规划（Planning）→ 控制（Control）→ 执行（Execution）→ 物理世界**

- 反馈（Feedback）闭合整个循环。
- 学习（Learning）横跨建模、估计、规划与控制。
- 动力学（Dynamics）、概率（Probability）、优化（Optimization）构成三条横向数学语言。

传统的“信号与系统、自动控制原理、现代控制理论、机器人学、最优控制、强化学习”等知识不再作为最高层课程分类，而被重新放回它们真正解决的系统问题中。

## 阅读入口

- [前言](00-preface/00-前言.md)
- [完整目录](SUMMARY.md)
- [统一知识地图](KNOWLEDGE_MAP.md)

## 配套实验导航

实验代码已拆分到独立仓库 **`model-to-action-lab`**。以下命令都在该仓库根目录运行；
Isaac Sim 由 `./run.sh` 选择 Python 3.10 并施加内存 cgroup，产物统一写入 `outputs/`。

| Demo | 课本落点 | 回答的问题 | 入口 |
| --- | --- | --- | --- |
| d00 | [38.21 平台验证](part-09-integration/38-系统误差-接口与验证.md#exp-d00) | 仿真器、资产、轮子和退出路径真的可靠吗？ | `./run.sh -m m2a.demos.d00_smoke --stage carter` |
| d01 | [13.14 底盘非理想](part-03-modeling/13-执行器与非理想物理模型.md#exp-d01) | 摩擦、载荷和转矩怎样产生滑移与里程计误差？ | `./run.sh -m m2a.demos.d01_chassis_params` |
| d02 | [13.15 关节等效参数](part-03-modeling/13-执行器与非理想物理模型.md#exp-d02) | 惯量、摩擦、饱和、重力和负载怎样改变关节响应？ | `./run.sh -m m2a.demos.d02_joint_params` |
| d03 | [16.16 传感器能力探底](part-04-estimation/16-传感-信号与滤波.md#exp-d03) | IMU/RTX lidar 的类型、数值、频率和更新时间是真的吗？ | `./run.sh -m m2a.demos.d03_sensors` |
| d04 | [34.14 电机参数](part-07-execution/34-电机与执行器控制.md#exp-d04) | 电流上限、反电动势、母线电压和减速比怎样共同限幅？ | `./run.sh -m m2a.demos.d04_motor_params` |
| d05 | [20.13 激光、里程计与回环](part-04-estimation/20-多传感器融合与机器人状态估计.md#exp-d05) | 为什么路程几乎正确，闭环位姿仍然错误？ | `./run.sh -m m2a.demos.d05_room_lidar_odom` |
| d06 | [11.20 机械臂与 TCP 回放](part-03-modeling/11-运动学与微分运动学.md#exp-d06) | 关节、连杆世界位姿与末端轨迹如何同步变化？ | `./run.sh -m m2a.demos.d06_arm_rerun_capture` |
| l01 | [36 数据驱动建模](part-08-learning/36-数据驱动建模与学习系统.md) | 开环激励能否把 (J,b)/(Ad,Bd) 辨回来？持续激励怎样决定可辨性？ | `python3 -m m2a.demos.l01_system_identification` |
| l02 | [37 学习控制](part-08-learning/37-从最优决策到学习控制.md) | REINFORCE 回报能否逼近价值迭代最优？基线怎样降方差？ | `python3 -m m2a.demos.l02_policy_gradient` |

完整环境说明、实测表格、Rerun 用法和覆盖边界见 `model-to-action-lab/README.md`。

## 仓库结构

- `part-01-world-systems/` 世界、系统与自主闭环
- `part-02-math-language/` 数学与系统语言
- `part-03-modeling/` 建模
- `part-04-estimation/` 估计
- `part-05-planning/` 规划
- `part-06-control/` 控制
- `part-07-execution/` 执行
- `part-08-learning/` 学习与数据驱动方法
- `part-09-integration/` 系统集成与统一视角
- `assets/` 图片与图表
