# SUMMARY

# 《从模型到行动：自主系统的统一方法》

> 核心主线：**建模（Modeling）→ 估计（Estimation）→ 规划（Planning）→ 控制（Control）→ 执行（Execution）**
>
> **学习（Learning）** 横跨各层，**反馈（Feedback）** 将整个系统连接成闭环。
>
> 机械臂作为贯穿案例，不作为一级知识层级。

- [前言](./README.md)

## 第一篇 世界与系统（World and System）
- [第1章 什么是系统（What Is a System）](./01-System/01-什么是系统.md)
  - [1.1 系统、环境与边界（System, Environment and Boundary）](./01-System/01-什么是系统.md#11-系统环境与边界system-environment-and-boundary)
  - [1.2 状态（State）](./01-System/01-什么是系统.md#12-状态state)
  - [1.3 输入（Input）](./01-System/01-什么是系统.md#13-输入input)
  - [1.4 输出（Output）](./01-System/01-什么是系统.md#14-输出output)
  - [1.5 参数（Parameter）](./01-System/01-什么是系统.md#15-参数parameter)
  - [1.6 扰动（Disturbance）](./01-System/01-什么是系统.md#16-扰动disturbance)
  - [1.7 约束（Constraint）](./01-System/01-什么是系统.md#17-约束constraint)
  - [1.8 连续时间系统与离散时间系统（Continuous-Time and Discrete-Time Systems）](./01-System/01-什么是系统.md#18-连续时间系统与离散时间系统continuous-time-and-discrete-time-systems)
  - [1.9 确定性系统与随机系统（Deterministic and Stochastic Systems）](./01-System/01-什么是系统.md#19-确定性系统与随机系统deterministic-and-stochastic-systems)
  - [1.10 静态系统与动态系统（Static and Dynamic Systems）](./01-System/01-什么是系统.md#110-静态系统与动态系统static-and-dynamic-systems)
  - [1.11 线性系统与非线性系统（Linear and Nonlinear Systems）](./01-System/01-什么是系统.md#111-线性系统与非线性系统linear-and-nonlinear-systems)
  - [1.12 时不变系统与时变系统（Time-Invariant and Time-Varying Systems）](./01-System/01-什么是系统.md#112-时不变系统与时变系统time-invariant-and-time-varying-systems)
  - [1.13 全驱动系统与欠驱动系统（Fully Actuated and Underactuated Systems）](./01-System/01-什么是系统.md#113-全驱动系统与欠驱动系统fully-actuated-and-underactuated-systems)
  - [1.14 完整约束与非完整约束（Holonomic and Nonholonomic Constraints）](./01-System/01-什么是系统.md#114-完整约束与非完整约束holonomic-and-nonholonomic-constraints)
  - [1.15 一个系统的最小数学描述](./01-System/01-什么是系统.md#115-一个系统的最小数学描述)
  - [1.16 从真实对象抽象出状态、输入和输出](./01-System/01-什么是系统.md#116-从真实对象抽象出状态输入和输出)

- [第2章 自主系统的完整闭环（Complete Closed Loop of Autonomous Systems）](./01-System/02-自主系统的完整闭环.md)
  - [2.1 真实世界（World）](./01-System/02-自主系统的完整闭环.md#21-真实世界world)
  - [2.2 传感器（Sensor）](./01-System/02-自主系统的完整闭环.md#22-传感器sensor)
  - [2.3 观测（Observation）](./01-System/02-自主系统的完整闭环.md#23-观测observation)
  - [2.4 状态估计（State Estimation）](./01-System/02-自主系统的完整闭环.md#24-状态估计state-estimation)
  - [2.5 系统模型（System Model）](./01-System/02-自主系统的完整闭环.md#25-系统模型system-model)
  - [2.6 目标（Goal）](./01-System/02-自主系统的完整闭环.md#26-目标goal)
  - [2.7 规划（Planning）](./01-System/02-自主系统的完整闭环.md#27-规划planning)
  - [2.8 参考量与目标轨迹（Reference and Desired Trajectory）](./01-System/02-自主系统的完整闭环.md#28-参考量与目标轨迹reference-and-desired-trajectory)
  - [2.9 控制（Control）](./01-System/02-自主系统的完整闭环.md#29-控制control)
  - [2.10 执行器（Actuator）](./01-System/02-自主系统的完整闭环.md#210-执行器actuator)
  - [2.11 物理响应（Physical Response）](./01-System/02-自主系统的完整闭环.md#211-物理响应physical-response)
  - [2.12 反馈（Feedback）](./01-System/02-自主系统的完整闭环.md#212-反馈feedback)
  - [2.13 学习（Learning）](./01-System/02-自主系统的完整闭环.md#213-学习learning)
  - [2.14 安全（Safety）](./01-System/02-自主系统的完整闭环.md#214-安全safety)
  - [2.15 系统中的不同时间尺度（Multiple Time Scales）](./01-System/02-自主系统的完整闭环.md#215-系统中的不同时间尺度multiple-time-scales)
  - [2.16 分层控制架构（Hierarchical Control Architecture）](./01-System/02-自主系统的完整闭环.md#216-分层控制架构hierarchical-control-architecture)
  - [2.17 从感知—思考—行动到闭环自主系统](./01-System/02-自主系统的完整闭环.md#217-从感知思考行动到闭环自主系统)

- [第3章 贯穿全书的数学语言（Mathematical Language）](./01-System/03-贯穿全书的数学语言.md)

## 第二篇 建模（Modeling）
- [第4章 建模的本质（The Nature of Modeling）](./02-Modeling/04-建模的本质.md)
- [第5章 从物理规律到微分方程（From Physical Laws to Differential Equations）](./02-Modeling/05-从物理规律到微分方程.md)
- [第6章 几何与运动的数学描述（Mathematical Description of Geometry and Motion）](./02-Modeling/06-几何与运动的数学描述.md)
- [第7章 运动学建模（Kinematic Modeling）](./02-Modeling/07-运动学建模.md)
- [第8章 动力学建模（Dynamic Modeling）](./02-Modeling/08-动力学建模.md)
- [第9章 执行器与非理想系统建模（Actuator and Non-Ideal System Modeling）](./02-Modeling/09-执行器与非理想系统建模.md)
- [第10章 系统的统一数学表示（Unified Mathematical Representations）](./02-Modeling/10-系统的统一数学表示.md)

## 第三篇 估计（Estimation）
- [第11章 观测与传感器（Observation and Sensors）](./03-Estimation/11-观测与传感器.md)
- [第12章 信号处理基础（Signal Processing Fundamentals）](./03-Estimation/12-信号处理基础.md)
- [第13章 状态估计（State Estimation）](./03-Estimation/13-状态估计.md)
- [第14章 贝叶斯估计（Bayesian Estimation）](./03-Estimation/14-贝叶斯估计.md)
- [第15章 卡尔曼滤波系列（Kalman Filtering）](./03-Estimation/15-卡尔曼滤波系列.md)

## 第四篇 规划（Planning）
- [第16章 从目标到运动（From Goal to Motion）](./04-Planning/16-从目标到运动.md)
- [第17章 轨迹生成（Trajectory Generation）](./04-Planning/17-轨迹生成.md)
- [第18章 构型空间规划（Configuration-Space Planning）](./04-Planning/18-构型空间规划.md)
- [第19章 基于搜索的规划（Search-Based Planning）](./04-Planning/19-基于搜索的规划.md)
- [第20章 基于采样的规划（Sampling-Based Planning）](./04-Planning/20-基于采样的规划.md)
- [第21章 基于优化的规划（Optimization-Based Planning）](./04-Planning/21-基于优化的规划.md)
- [第22章 动态规划与序贯决策（Dynamic Programming and Sequential Decision Making）](./04-Planning/22-动态规划与序贯决策.md)

## 第五篇 控制（Control）
- [第23章 反馈的本质（The Nature of Feedback）](./05-Control/23-反馈的本质.md)
- [第24章 动态系统响应（Dynamic System Response）](./05-Control/24-动态系统响应.md)
- [第25章 经典控制（Classical Control）](./05-Control/25-经典控制.md)
- [第26章 PID 控制（PID Control）](./05-Control/26-PID控制.md)
- [第27章 状态空间控制（State-Space Control）](./05-Control/27-状态空间控制.md)
- [第28章 基于模型的控制（Model-Based Control）](./05-Control/28-基于模型的控制.md)
- [第29章 最优控制（Optimal Control）](./05-Control/29-最优控制.md)
- [第30章 线性二次调节器（Linear Quadratic Regulator, LQR）](./05-Control/30-线性二次调节器.md)
- [第31章 迭代 LQR 与微分动态规划（iLQR and DDP）](./05-Control/31-iLQR与DDP.md)
- [第32章 模型预测控制（Model Predictive Control, MPC）](./05-Control/32-模型预测控制.md)
- [第33章 非线性控制（Nonlinear Control）](./05-Control/33-非线性控制.md)
- [第34章 鲁棒控制与自适应控制（Robust and Adaptive Control）](./05-Control/34-鲁棒控制与自适应控制.md)

## 第六篇 执行（Execution）
- [第35章 连续理论与数字计算机之间的鸿沟（Continuous Theory to Digital Implementation）](./06-Execution/35-连续理论与数字实现.md)
- [第36章 实时控制（Real-Time Control）](./06-Execution/36-实时控制.md)
- [第37章 从控制量到物理作用（From Control Command to Physical Action）](./06-Execution/37-从控制量到物理作用.md)
- [第38章 通信、延迟与系统架构（Communication, Delay and System Architecture）](./06-Execution/38-通信延迟与系统架构.md)
- [第39章 现实系统中的非理想问题（Non-Idealities in Real Systems）](./06-Execution/39-现实系统中的非理想问题.md)
- [第40章 从仿真到真实系统（Simulation to Real System）](./06-Execution/40-从仿真到真实系统.md)

## 第七篇 学习（Learning）
- [第41章 学习到底在系统中学习什么（What Can Be Learned）](./07-Learning/41-学习到底在系统中学习什么.md)
- [第42章 系统辨识（System Identification）](./07-Learning/42-系统辨识.md)
- [第43章 学习动力学模型（Learned Dynamics）](./07-Learning/43-学习动力学模型.md)
- [第44章 数据驱动控制（Data-Driven Control）](./07-Learning/44-数据驱动控制.md)
- [第45章 强化学习（Reinforcement Learning, RL）](./07-Learning/45-强化学习.md)
- [第46章 基于模型的强化学习（Model-Based Reinforcement Learning）](./07-Learning/46-基于模型的强化学习.md)
- [第47章 基于学习的控制（Learning-Based Control）](./07-Learning/47-基于学习的控制.md)

## 第八篇 系统集成（Integration）
- [第48章 模块之间如何连接（How Modules Connect）](./08-Integration/48-模块之间如何连接.md)
- [第49章 不同模块的时间尺度（Time Scales of Different Modules）](./08-Integration/49-不同模块的时间尺度.md)
- [第50章 规划与控制为什么越来越难以区分（Why Planning and Control Converge）](./08-Integration/50-规划与控制为什么越来越难以区分.md)
- [第51章 模型与学习为什么正在融合（Why Modeling and Learning Converge）](./08-Integration/51-模型与学习为什么正在融合.md)
- [第52章 一个系统应该怎样从零开始设计（Designing a System from Scratch）](./08-Integration/52-从零开始设计系统.md)

## 第九篇 统一视角（Unified View）
- [第53章 每个算法到底位于哪里（Where Algorithms Belong）](./09-Unified-View/53-每个算法到底位于哪里.md)
- [第54章 动力学：世界如何变化（Dynamics: How the World Evolves）](./09-Unified-View/54-动力学世界如何变化.md)
- [第55章 概率：我们知道多少（Probability: What We Know）](./09-Unified-View/55-概率我们知道多少.md)
- [第56章 优化：我们希望未来怎样变化（Optimization: How We Want the Future to Evolve）](./09-Unified-View/56-优化我们希望未来怎样变化.md)
- [第57章 反馈：整本书真正的中心（Feedback as the Core）](./09-Unified-View/57-反馈整本书真正的中心.md)
- [第58章 最终统一（Final Unification）](./09-Unified-View/58-最终统一.md)

## 附录
- [附录 A 数学基础速查（Mathematics Reference）](./Appendix/A-数学基础速查.md)
- [附录 B 空间与刚体数学速查（Rigid-Body Mathematics Reference）](./Appendix/B-空间与刚体数学速查.md)
- [附录 C 常见控制算法速查（Control Algorithms Reference）](./Appendix/C-常见控制算法速查.md)
- [附录 D 常见规划算法速查（Planning Algorithms Reference）](./Appendix/D-常见规划算法速查.md)
- [附录 E 软件工具链（Software Toolchain）](./Appendix/E-软件工具链.md)
- [附录 F 配套实验系统（Companion Experimental Systems）](./Appendix/F-配套实验系统.md)
