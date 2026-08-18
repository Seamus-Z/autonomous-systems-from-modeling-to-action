# 统一知识地图

## 系统主线

物理世界 → 建模 → 估计 → 规划 → 控制 → 执行 → 物理世界

反馈闭合整个循环；学习横跨建模、估计、规划与控制。

## 传统输入输出路线

物理模型 → 微分方程 → Laplace → 传递函数 → 极点 / 零点 → 时域 / 频域 → 经典控制

## 现代状态空间路线

物理模型 → 状态空间 → 稳定性 / 可控性 / 可观性 → 状态反馈 / 状态估计 → 最优控制 → MPC

## 估计路线

Sensor → Filtering → Observer → Bayes → Kalman → Sensor Fusion

## 规划路线

Geometry → Configuration Space → Search → Sampling → Kinodynamic Planning → Trajectory Optimization

## 最优决策路线

Optimization → Dynamic Programming → LQR → iLQR / DDP → MPC → RL

## 三条横向数学语言

- 动力学（Dynamics）：世界怎样变化？
- 概率（Probability）：我们知道多少？
- 优化（Optimization）：未来应该怎样选择？
