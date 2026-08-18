#!/usr/bin/env python3
"""Rebuild the book to the compressed 46-chapter architecture."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PARTS = {
    1: ("01-System", "第一篇 世界与系统（World and System）",
        "从真实对象抽出系统，定义状态、输入、输出，画出闭环，准备好数学语言。"),
    2: ("02-Modeling", "第二篇 建模（Modeling）",
        "物理规律 → 微分方程 → 状态空间 → 简化/线性化 → 开环分析。"),
    3: ("03-Estimation", "第三篇 估计（Estimation）",
        "测量的是 $y$，控制器需要的是 $x$（或 $\\hat x$）。"),
    4: ("04-Planning", "第四篇 规划（Planning）",
        "把目标变成一条可行的未来。约束会改变问题类型。"),
    5: ("05-Control", "第五篇 控制（Control）",
        "先架构（层级、前馈+反馈），再方法（PID / 状态反馈 / 最优 / 约束）。"),
    6: ("06-Execution", "第六篇 执行（Execution）",
        "把连续状态空间变成数字计算机上的实时闭环。"),
    7: ("07-Learning", "第七篇 学习（Learning）",
        "学习横切修正主链上的某类误差，不替代主链。"),
    8: ("08-Integration", "第八篇 系统集成（Integration）",
        "把已经讲过的模块接成一条可运行的系统。不新讲概念。"),
    9: ("09-Unified-View", "第九篇 统一视角（Unified View）",
        "动力学、概率、优化、反馈是四套语言；算法只是落点。"),
}

# n, part, filename, title, sections
CHAPTERS: list[tuple[int, int, str, str, list[str]]] = [
    (1, 1, "01-什么是系统.md", "什么是系统（What Is a System）", []),  # patched
    (2, 1, "02-自主系统的完整闭环.md", "自主系统的完整闭环（Complete Closed Loop of Autonomous Systems）", []),
    (3, 1, "03-贯穿全书的数学语言.md", "贯穿全书的数学语言（Mathematical Language）", []),
    (4, 2, "04-建模的本质.md", "建模的本质（The Nature of Modeling）", []),
    (5, 2, "05-从物理规律到微分方程.md", "从物理规律到微分方程（From Physical Laws to Differential Equations）", []),
    (6, 2, "06-几何与运动的数学描述.md", "几何与运动的数学描述（Mathematical Description of Geometry and Motion）", [
        "构型、构型空间、自由度、任务空间",
        "旋转：矩阵、欧拉角、轴角、四元数",
        "SO(3)、SE(3)、so(3)、se(3)",
        "螺旋、运动旋量、力旋量、指数映射、伴随",
        "后文出口：POE、运动学 Jacobian、几何控制",
    ]),
    (7, 2, "07-运动学建模.md", "运动学建模（Kinematic Modeling）", [
        "正运动学；DH / MDH；指数积公式（Product of Exponentials, POE）",
        "微分运动学；雅可比矩阵作为速度映射（Jacobian as Velocity Map）",
        "奇异位形（Singularity）与可操作度（Manipulability）",
        "逆运动学、伪逆、冗余与零空间",
        "运动学 Jacobian ≠ 后文动力学线性化用的 $\\partial f/\\partial x$",
    ]),
    (8, 2, "08-动力学建模.md", "动力学建模（Dynamic Modeling）", [
        "正动力学与逆动力学（Forward and Inverse Dynamics）",
        r"$M(q)\ddot q + C(q,\dot q)\dot q + g(q)=\tau$",
        r"改写成 $\dot x=f(x,u)$；六轴臂：12 状态、6 输入",
        "正动力学用于仿真，逆动力学用于前馈（实现见第29章）",
        "约束、接触、浮动基、欠驱动：约束会改写 $f$",
        "模型验证；出口：前馈 / MPC / 轨迹优化",
    ]),
    (9, 2, "09-执行器与非理想系统建模.md", "执行器与非理想因素（Actuators and Non-Idealities）", [
        "为什么刚体动力学还不够",
        "电机电气动态；为什么它通常比机械动态快",
        "摩擦、齿隙、柔顺、饱和、延迟",
        "这些非理想因素如何进入后文的约束与误差",
    ]),
    (10, 2, "10-状态空间：系统的统一接口.md", "状态空间：系统的统一接口（State Space as Unified Interface）", [
        "为什么需要状态空间；高阶方程为什么改写成一阶",
        r"非线性：$\dot x=f(x,u,t),\quad y=h(x,u,t)$",
        r"线性：$\dot x=Ax+Bu,\quad y=Cx+Du$；$A/B/C/D$ 的工程含义",
        "与传递函数的关系：各自擅长什么",
        "为什么特别适合 MIMO；SISO/MIMO 与线性/非线性不要混为一谈",
        "非线性 MIMO 同样使用状态空间；机械臂 / 无人机 / 移动机器人共用接口",
        r"离散：$x_{k+1}=f(x_k,u_k)$；通向数字控制、Kalman、MPC",
        "随机与混杂：只给接口，不在这里展开滤波或混合规划",
        "下一步是简化与分析，不是立刻设计控制器",
    ]),
    (11, 2, "11-工作点、线性化与模型简化.md", "工作点、线性化与模型简化（Linearization and Model Simplification）", [
        "平衡点（Equilibrium Point）与工作点（Operating Point）；小扰动",
        r"多变量 Taylor；$A=\partial f/\partial x,\ B=\partial f/\partial u$",
        "MIMO 同样可线性化；限制来自局部性，不是 SISO/MIMO",
        r"机械臂：从 $M\ddot q+\cdots=\tau$ 到 $\delta\dot x=A\delta x+B\delta u$",
        "轨迹线性化与时变线性系统（为 TVLQR / iLQR / EKF 埋伏笔）",
        "时间尺度分离（Time-Scale Separation）：为什么机械模型可以忽略电流环",
        "快变量消除、主导动态、降阶模型（Reduced-Order Model）",
        "控制模型为何故意更简单；降阶误差交给反馈 / 鲁棒控制",
    ]),
    (12, 2, "12-开环系统分析.md", "开环系统分析（Open-Loop System Analysis）", [
        "顺序：建模 → 状态空间 → 分析 → 再设计",
        "稳定性（Stability）、模态（Modes）、特征值与极点（工程直觉）",
        "可控性（Controllability）、可观性（Observability）；输入–状态与输出–内部状态",
        "执行器配置与传感器配置",
        "系统中的误差地图（只此一次）",
        "开环分析能回答什么，还不能回答什么",
    ]),
    (13, 3, "13-观测与传感器.md", "观测与传感器（Observation and Sensors）", [
        r"状态 vs 测量；$y=h(x,u,t)$",
        "噪声、偏置、量化、带宽、延迟、标定",
        "传感器误差对应误差地图中的哪一项",
    ]),
    (14, 3, "14-信号处理基础.md", "信号处理基础（Signal Processing Fundamentals）", [
        "时域 / 频域，拉普拉斯变换 / Z 变换",
        "滤波、延迟，以及滤波与反馈的矛盾",
        "滤波 ≠ 状态估计",
    ]),
    (15, 3, "15-状态估计.md", "状态估计（State Estimation）", [
        "回顾可观性（回指第12章，不重讲）",
        "龙伯格观测器（Luenberger Observer）与误差动力学",
        "扰动 / 扩张状态 / 动量观测器",
        "估计误差如何进入控制",
    ]),
    (16, 3, "16-贝叶斯估计.md", "贝叶斯估计（Bayesian Estimation）", [
        "先验、似然、后验",
        "预测用 $f$，校正用 $h$",
        "高斯与协方差：Kalman 的语言",
    ]),
    (17, 3, "17-卡尔曼滤波系列.md", "卡尔曼滤波系列（Kalman Filtering）", [
        "离散线性高斯上的卡尔曼滤波（Kalman Filter）",
        "扩展卡尔曼滤波（Extended Kalman Filter, EKF）= 第11章的 Taylor / Jacobian",
        "UKF、粒子滤波、互补滤波、融合",
        r"分离原则（Separation Principle）；控制器吃进去的是 $\hat x$",
    ]),
    (18, 4, "18-从目标到运动.md", "从目标到运动（From Goal to Motion）", [
        "目标、参考、路径、轨迹、策略",
        "规划在控制层级中的位置",
        "约束如何改变问题：无约束插值 → 几何路径规划 → Kinodynamic → 接触规划",
        "可行性（Feasibility）与最优性（Optimality）",
    ]),
    (19, 4, "19-轨迹生成.md", "轨迹生成（Trajectory Generation）", [
        "多项式、梯形 / S 形、样条",
        "速度 / 加速度 / jerk 约束",
        "几何光滑 ≠ 动力学可行",
    ]),
    (20, 4, "20-构型空间与搜索.md", "构型空间与搜索（Configuration Space and Search）", [
        "构型空间（Configuration Space）、障碍、碰撞、维数灾难",
        "图搜索：BFS、Dijkstra、A*",
    ]),
    (21, 4, "21-基于采样的规划.md", "基于采样的规划（Sampling-Based Planning）", [
        "概率路图法（PRM）、快速扩展随机树（RRT）、RRT*",
        "概率完备与渐近最优",
    ]),
    (22, 4, "22-基于优化的规划.md", "基于优化的规划（Optimization-Based Planning）", [
        "决策变量、代价、状态/输入/动力学/碰撞约束",
        "打靶、配点、序列凸、CHOMP / STOMP",
        "二次型、Hessian、KKT 如何进入规划器（回指第3章）",
    ]),
    (23, 4, "23-动态规划与序贯决策.md", "动态规划与序贯决策（Dynamic Programming and Sequential Decision Making）", [
        "贝尔曼方程（Bellman Equation）、价值函数、时域",
        "规划与最优控制的第一次汇合",
    ]),
    (24, 5, "24-反馈的本质.md", "反馈的本质（The Nature of Feedback）", [
        "开环 / 闭环，调节 / 跟踪，扰动抑制",
        "稳定性与性能；模型误差为什么需要反馈",
    ]),
    (25, 5, "25-控制架构：层级、前馈与反馈.md", "控制架构：层级、前馈与反馈（Control Architecture）", [
        "电流 → 力矩 → 速度 → 位置 → 任务空间 → 运动规划 → 任务规划",
        "PID / MPC / RL 都可以出现在不同层级；层级 ≠ 算法",
        r"$\tau=\tau_{\mathrm{model}}+\tau_{\mathrm{feedback}}$；重力补偿与逆动力学前馈",
        "为什么模型不必完美；高性能往往是前馈预测 + 反馈修正",
        "与第11章时间尺度、第12章误差地图的关系",
    ]),
    (26, 5, "26-动态响应与经典控制.md", "动态响应与经典控制（Response and Classical Control）", [
        "一、二阶响应指标；与第12章模态/特征值对应",
        "传递函数、根轨迹、波特图、裕度、校正",
        "经典控制与状态空间如何对接",
    ]),
    (27, 5, "27-PID控制.md", "PID 控制（PID Control）", [
        "比例 / 积分 / 微分、离散实现、抗饱和、串级、增益调度",
        "PID 是一种反馈律，不是一个控制层级",
    ]),
    (28, 5, "28-状态空间控制.md", "状态空间控制（State-Space Control）", [
        "从第12章分析到状态反馈设计",
        "极点配置、参考跟踪、积分扩维、观测器反馈",
        "无约束状态反馈的边界；有输入约束 → QP / MPC",
    ]),
    (29, 5, "29-基于模型的控制.md", "基于模型的控制（Model-Based Control）", [
        "计算力矩（Computed Torque）：把第25章结构落在机械臂上",
        "反馈线性化；关节空间 / 任务空间 / 力与阻抗",
        "SE(3) 与几何控制（回指第6章）",
    ]),
    (30, 5, "30-最优控制与LQR.md", "最优控制与 LQR（Optimal Control and LQR）", [
        "代价、约束、庞特里亚金最小值原理（PMP）、HJB 方程",
        "二次型 → 线性二次调节器（Linear Quadratic Regulator, LQR）；TVLQR 接第11章；LQG 接 Kalman",
        "LQR 仍是无约束状态反馈",
    ]),
    (31, 5, "31-iLQR、DDP与MPC.md", "iLQR、DDP 与 MPC（Trajectory Optimization and MPC）", [
        "迭代 LQR（iLQR）/ 微分动态规划（DDP）：Taylor + Hessian 沿轨迹迭代",
        "模型预测控制（Model Predictive Control, MPC）：离散状态空间 + 二次型 + 约束",
        "有约束之后问题类型变了；MPC 也可用于不同层级",
        "规划与控制在滚动时域中汇合",
    ]),
    (32, 5, "32-非线性、鲁棒与自适应.md", "非线性、鲁棒与自适应（Nonlinear, Robust, Adaptive）", [
        "第11章局部线性化的边界；李雅普诺夫稳定性、滑模、反步、能量整形",
        "模型误差 → 鲁棒控制；参数误差 → 自适应控制（回指第12章误差地图）",
        "与学习方法的边界",
    ]),
    (33, 6, "33-离散化与数字实现.md", "离散化与数字实现（Discretization）", [
        "采样、零阶保持（ZOH）、欧拉 / 双线性变换 / 精确离散化",
        r"为什么 Kalman 与 MPC 通常在 $x_{k+1}$ 上实现",
        "离散化误差（回指第12章）",
    ]),
    (34, 6, "34-实时与多速率.md", "实时与多速率（Real-Time and Multi-Rate）", [
        "控制循环、截止时间、抖动",
        "多速率：落实第11章的时间尺度分离",
    ]),
    (35, 6, "35-从指令到物理作用.md", "从指令到物理作用（Command to Action）", [
        "位置 / 速度 / 力矩 / 电流指令",
        "电流环、速度环、位置环、带宽分离（Bandwidth Separation）",
        "实现的是第25章的层级，可在各层换算法",
    ]),
    (36, 6, "36-通信、非理想与仿真到实机.md", "通信、非理想与仿真到实机（Deployment）", [
        "总线、延迟、同步",
        "饱和如何迫使你离开纯 LQR",
        "仿真—现实差距；数值误差 ≠ 模型误差",
    ]),
    (37, 7, "37-学习什么、不替代什么.md", "学习什么、不替代什么（What Can Be Learned）", [
        "可学生：感知、估计、动力学、参数、代价、策略、残差",
        "先看第12章误差地图，再决定学习加在哪",
        "学习 vs 反馈",
    ]),
    (38, 7, "38-系统辨识.md", "系统辨识（System Identification）", [
        "参数 / 状态空间辨识，持续激励（Persistent Excitation）",
        "运动学标定、惯性与摩擦参数",
        "参数误差优先走辨识，而不是直接上强化学习",
    ]),
    (39, 7, "39-学习动力学与数据驱动控制.md", "学习动力学与数据驱动控制（Learned Dynamics and Data-Driven Control）", [
        r"$f_{\mathrm{physics}}$ 与 $f_\theta$；残差与混合模型",
        r"学到的仍应能写成 $\dot x=f(x,u)$ 或 $x_{k+1}=f(x_k,u_k)$",
        "数据驱动预测控制（DeePC）、Koopman：仍是预测接口，不是另一套系统观",
    ]),
    (40, 7, "40-强化学习及其与控制的接口.md", "强化学习及其与控制的接口（RL and Control）", [
        "马尔可夫决策过程（MDP）的 state 就是状态；action 可以位于不同控制层级",
        "无模型 / 基于模型；学习模型上的规划与 MPC",
        "残差强化学习、安全层、仿真到现实：默认补的是模型残差",
    ]),
    (41, 8, "41-模块如何连接.md", "模块如何连接（How Modules Connect）", [
        "传感 → 估计 → 规划 → 控制 → 执行 → 世界",
        "模型分别进入估计、规划、控制",
        "状态空间是模块间的共同语言",
    ]),
    (42, 8, "42-规划与控制、模型与学习为何汇合.md", "规划与控制、模型与学习为何汇合（Two Convergences）", [
        "路径规划 → 轨迹优化 → MPC / iLQR → 基于模型的强化学习",
        "第一性原理 → 辨识 → 学习残差 → 对任务有用即可",
    ]),
    (43, 8, "43-从零设计一条系统.md", "从零设计一条系统（Designing from Scratch）", [
        "定义任务、边界、状态、输入、观测",
        "建模 → 写成状态空间 → 开环分析",
        "估计器；目标与约束；规划器与控制器（层级决策与算法决策分开）",
        "执行、安全、仿真、实机；按误差类型决定学习加在哪；闭环迭代",
    ]),
    (44, 9, "44-算法落在主线上的哪里.md", "算法落在主线上的哪里（Where Algorithms Belong）", [
        "PID、观测器、Kalman、A* / RRT、LQR / iLQR / DDP、MPC、辨识、强化学习",
        "不要把算法作为知识体系的一级节点",
    ]),
    (45, 9, "45-四套语言.md", "四套语言（Four Languages）", [
        "动力学：世界如何变化（连续 / 离散 / 随机 / 混杂 / 学习）",
        "概率：我们知道多少",
        "优化：我们希望未来怎样变化",
        "反馈：整本书的中心",
    ]),
    (46, 9, "46-概念如何长出方法，再回到世界.md", "概念如何长出方法，再回到世界（From Concepts Back to the World）", [
        "状态空间、Jacobian / Taylor、二次型 / Hessian / KKT、SE(3)、时间尺度、约束、误差",
        "观测 → 估计 → 建模 → 预测 → 规划 → 控制 → 执行 → 再观测 → 学习 → 循环",
    ]),
]


def ch_by_n(n: int):
    return next(c for c in CHAPTERS if c[0] == n)


def rel_link(from_part: int, to_n: int) -> str:
    if to_n == 0:
        to_dir = "00-Preface"
        fn = "00-前言.md"
        to_part = 0
    else:
        tn, to_part, fn, _, _ = ch_by_n(to_n)
        to_dir = PARTS[to_part][0]
    from_dir = PARTS[from_part][0] if from_part else "00-Preface"
    if from_dir == to_dir:
        return fn
    return f"../{to_dir}/{fn}"


def nav_bar(n: int, part: int) -> str:
    prev = n - 1
    nxt = n + 1 if n < 46 else None
    left = f"[← 第{prev}章]({rel_link(part, prev)})" if prev >= 1 else f"[← 前言]({rel_link(part, 0)})"
    right = f"[第{nxt}章 →]({rel_link(part, nxt)})" if nxt else ""
    mid = "[目录](../SUMMARY.md)"
    if right:
        return f"{left} · {mid} · {right}"
    return f"{left} · {mid}"


def stub_markdown(n: int, part: int, filename: str, title: str, sections: list[str]) -> str:
    part_dir, part_name, spine = PARTS[part]
    nav_items = "\n".join(
        f"- [{n}.{i} {sec}](#ch{n}-sec{i})" for i, sec in enumerate(sections, 1)
    )
    bodies = []
    for i, sec in enumerate(sections, 1):
        bodies.append(f'<a id="ch{n}-sec{i}"></a>\n## {n}.{i} {sec}\n\n> TODO\n')
    first_of_part = min(c[0] for c in CHAPTERS if c[1] == part)
    extra = f"\n\n> **本篇主线：** {spine}" if n == first_of_part else ""
    bar = nav_bar(n, part)
    return (
        f"# 第{n}章 {title}\n\n"
        f"{bar}\n\n"
        f"**小节导航**\n\n"
        f"{nav_items}\n\n"
        f"> 本章属于 **{part_name}**。机械臂作为贯穿实例，用于连接理论、代码、仿真与真实硬件。"
        f"{extra}\n\n"
        + "\n".join(bodies)
        + f"\n---\n\n{bar}\n"
    )


# ---------- written-chapter patches ----------

TODO_BLOCK = "> TODO\n"


def rebuild_nav_from_headings(text: str, ch: int) -> str:
    heads = re.findall(rf"^## ({ch}\.\d+) (.+)$", text, re.M)
    items = "\n".join(f"- [{num} {title}](#ch{ch}-sec{num.split('.')[1]})" for num, title in heads)
    text = re.sub(
        r"\*\*小节导航\*\*\n\n(?:- .+\n)+",
        f"**小节导航**\n\n{items}\n\n",
        text,
        count=1,
    )
    return text


def replace_nav_bar(text: str, ch: int, part: int) -> str:
    bar = nav_bar(ch, part)
    text = re.sub(r"^\[.*目录.*$", bar, text, count=1, flags=re.M)
    # footer: last similar line
    lines = text.rstrip().splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if "SUMMARY.md" in lines[i] and ("第" in lines[i] or "前言" in lines[i] or "目录" in lines[i]):
            lines[i] = bar
            break
    return "\n".join(lines) + "\n"


def renumber_from_high(text: str, ch: int, mapping: dict[int, int]) -> str:
    """mapping old_sec -> new_sec, apply high-to-low to avoid collisions."""
    for old in sorted(mapping, reverse=True):
        new = mapping[old]
        if old == new:
            continue
        text = text.replace(f"ch{ch}-sec{old}", f"ch{ch}-secTMP{old}")
        text = re.sub(rf"(## {ch}\.){old}( )", rf"\g<1>TMP{old}\2", text)
        text = re.sub(rf"(\[){ch}\.{old}( )", rf"\g<1>{ch}.TMP{old}\2", text)
    for old, new in mapping.items():
        if old == new:
            continue
        text = text.replace(f"ch{ch}-secTMP{old}", f"ch{ch}-sec{new}")
        text = re.sub(rf"(## {ch}\.)TMP{old}( )", rf"\g<1>{new}\2", text)
        text = re.sub(rf"(\[){ch}\.TMP{old}( )", rf"\g<1>{ch}.{new}\2", text)
    return text


def insert_before_anchor(text: str, anchor: str, block: str) -> str:
    needle = f'<a id="{anchor}"></a>'
    if needle not in text:
        raise SystemExit(f"missing anchor {anchor}")
    return text.replace(needle, block + needle, 1)


def insert_before_heading_line(text: str, heading: str, block: str) -> str:
    if heading not in text:
        raise SystemExit(f"missing heading {heading}")
    return text.replace(heading, block + heading, 1)


def section_block(ch: int, sec: int, title: str, body: str) -> str:
    return (
        f'<a id="ch{ch}-sec{sec}"></a>\n'
        f"## {ch}.{sec} {title}\n\n"
        f"{body.rstrip()}\n\n"
    )


def patch_ch1(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mapping = {16: 19, 15: 18, 14: 17, 13: 16, 12: 15}
    text = renumber_from_high(text, 1, mapping)
    b12 = section_block(1, 12, "单输入单输出与多输入多输出（SISO and MIMO）", """
输入和输出的个数，是系统的另一条分类轴。

单输入单输出（Single-Input Single-Output, SISO）系统只有一个控制量和一个被关注的输出。多输入多输出（Multi-Input Multi-Output, MIMO）系统则同时有多个输入和多个输出。

六轴机械臂是一个典型的 MIMO 例子：六个关节力矩是输入，六个关节角度（以及它们的速度）进入状态。它并不是“另一种理论”，只是输入、输出和状态的维数都大于 1。

这条分类轴与线性/非线性无关。非线性系统可以是 SISO，线性系统也可以是 MIMO。统一接口仍然是状态空间，细节见第10章。
""")
    b13 = section_block(1, 13, "线性/非线性 与 SISO/MIMO 是两个独立维度", """
读者很容易把这两件事叠在一起，以为“非线性就不能用状态空间”，或“MIMO 必须先线性化”。

它们是两个独立问题：

- 线性 / 非线性：状态方程 $\\dot x=f(x,u)$ 对 $(x,u)$ 是否线性；
- SISO / MIMO：输入维数 $m$ 和输出维数 $p$ 是否等于 1。

非线性 MIMO 系统完全可以写成

$$
\\dot x=f(x,u),\\qquad y=h(x,u)
$$

局部线性化（第11章）可以作用在 MIMO 上；限制来自工作点附近的局部性，不是来自输入输出个数。
""")
    b14 = section_block(1, 14, "状态维数与输入输出维数的区别", """
状态维数 $n$、输入维数 $m$、输出维数 $p$ 是三个不同的整数。

六轴机械臂若取 $x=(q,\\dot q)$，则 $n=12$、$m=6$。输出可以是全部关节角（$p=6$），也可以只是末端位姿。

不要把“有六个电机”理解成“只有六维状态”。状态回答的是：要预测未来，现在必须记住什么。
""")
    text = insert_before_anchor(text, "ch1-sec15", b12 + b13 + b14)
    text = rebuild_nav_from_headings(text, 1)
    text = replace_nav_bar(text, 1, 1)
    path.write_text(text, encoding="utf-8")


def patch_ch2(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mapping = {17: 19, 16: 17, 15: 16, 14: 15, 13: 14}
    text = renumber_from_high(text, 2, mapping)
    b13 = section_block(2, 13, "前馈（Feedforward）：模型如何参与行动", """
闭环图里不能只有反馈。模型除了用来估计和规划，还可以直接给出控制量：重力补偿、逆动力学、轨迹前馈都是这一类。

一个贯穿全书的结构是

$$
\\tau=\\tau_{\\mathrm{model}}+\\tau_{\\mathrm{feedback}}
$$

模型负责预测，反馈负责修正模型误差。完整讨论放在第25章；这里只需记住：开环模型也会进入行动，而不是等控制篇才突然出现。
""")
    b18 = section_block(2, 18, "控制层级不等于控制算法", """
电流环、力矩环、速度环、位置环、任务空间控制、运动规划、任务规划，是**架构轴**。

PID、LQR、MPC、强化学习，是**方法轴**。

同一层级可以换算法：电流环常用 PID，位置层也可以用 PID 或 MPC；强化学习输出的动作也可以是力矩、速度或任务空间增量。不要把“用了 MPC”理解成“系统不再有层级”。细节见第25章。
""")
    text = insert_before_anchor(text, "ch2-sec14", b13)
    text = insert_before_anchor(text, "ch2-sec19", b18)
    # note in 2.16 time scales
    text = text.replace(
        "## 2.16 系统中的不同时间尺度（Multiple Time Scales）",
        "## 2.16 系统中的不同时间尺度（Multiple Time Scales）",
    )
    note = "\n\n> 这里只建立“快环 / 慢环”的直觉。把它提升为建模原则（为何机械模型可以忽略电流环、为何不同层用不同模型）见第11章。\n"
    # insert note after 2.16 heading
    text = text.replace(
        "## 2.16 系统中的不同时间尺度（Multiple Time Scales）\n",
        "## 2.16 系统中的不同时间尺度（Multiple Time Scales）\n" + note,
        1,
    )
    text = rebuild_nav_from_headings(text, 2)
    text = replace_nav_bar(text, 2, 1)
    path.write_text(text, encoding="utf-8")


def patch_ch3(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mapping = {k: k + 1 for k in range(14, 25)}
    text = renumber_from_high(text, 3, mapping)
    b14 = section_block(3, 14, "高阶微分方程与一阶方程组（Higher-Order ODE to First-Order Form）", """
牛顿定律给出的往往是关于位置的二阶方程。状态空间要求一阶形式 $\\dot x=f(x,u)$。

标准做法是把位置和速度一起取成状态。例如 $\\ddot q=a(q,\\dot q,u)$ 取 $x=(q,\\dot q)$ 后变成

$$
\\dot x=\\begin{bmatrix}\\dot q\\\\ a(q,\\dot q,u)\\end{bmatrix}
$$

这就是第5章到第10章之间最关键的一步：不是新的物理，而是换一种适合估计和控制的写法。
""")
    b26 = section_block(3, 26, "这些对象将在何处再次出现（Concept Roadmap）", """
本章不是工具箱陈列，而是伏笔图：

| 概念 | 后面自然长出 |
|---|---|
| 秩、零空间 | 可控性、可观性 |
| 特征值 | 模态、稳定性、极点配置 |
| 二次型 | LQR、MPC 代价 |
| Jacobian | 机械臂速度映射；非线性线性化 |
| Hessian | Newton / SQP / iLQR / DDP |
| Taylor | 工作点线性化、EKF、iLQR |
| 协方差、贝叶斯 | Kalman |
| KKT、凸性 | QP、MPC |

方法出现时，应能指回这一行，而不是当成突然冒出来的算法。
""")
    text = insert_before_anchor(text, "ch3-sec15", b14)
    # append 3.26 before footer ---
    if "\n---\n" in text:
        idx = text.rfind("\n---\n")
        text = text[:idx] + "\n" + b26 + text[idx:]
    text = rebuild_nav_from_headings(text, 3)
    text = replace_nav_bar(text, 3, 1)
    path.write_text(text, encoding="utf-8")


def patch_ch4(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    mapping = {k: k + 1 for k in range(6, 16)}
    text = renumber_from_high(text, 4, mapping)
    b6 = section_block(4, 6, "高保真仿真模型与控制模型（Simulation Model vs. Control Model）", """
“模型应该多复杂”真正要拆开的是两个用途。

高保真仿真模型尽量包含柔性、摩擦、接触、传感器延迟，用来检验想法。控制模型通常更简单：只保留当前层级需要的主导动态。

这不是偷懒。第11章会把这件事写成时间尺度分离和降阶：电流环动态可以不进入机械控制模型；未建模部分交给反馈和鲁棒控制。
""")
    b17 = section_block(4, 17, "本章如何通向降阶、前馈与反馈", """
如果模型永远等于现实，就不需要反馈，也不需要学习。正因为模型是抽象，后面才会出现：

- 用更简单的控制模型（第11章）；
- 用模型做前馈，用反馈修正误差（第25章）；
- 用误差地图决定问题该交给控制、估计还是辨识（第12章）。
""")
    text = insert_before_anchor(text, "ch4-sec7", b6)
    text = insert_before_heading_line(text, "## 本章小结", b17)
    text = rebuild_nav_from_headings(text, 4)
    text = replace_nav_bar(text, 4, 2)
    path.write_text(text, encoding="utf-8")


def patch_ch5(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    b16 = section_block(5, 16, "微分方程还不是状态空间：缺什么", """
写出牛顿定律、拉格朗日方程或电路方程，只完成了“物理 → 微分方程”。还缺三件事，第10章才会收口：

1. 选择状态：哪些变量足以预测未来；
2. 改写成一阶： $\\dot x=f(x,u)$；
3. 写出输出：$y=h(x,u)$。

机械臂的 $M(q)\\ddot q+C(q,\\dot q)\\dot q+g(q)=\\tau$ 在第8章完成第二类方程，在第10章才成为统一接口。在那之前，不要急着设计控制器。
""")
    text = insert_before_heading_line(text, "## 本章小结", b16)
    text = rebuild_nav_from_headings(text, 5)
    text = replace_nav_bar(text, 5, 2)
    path.write_text(text, encoding="utf-8")


def patch_preface(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "preface-sec9" in text:
        return
    nav_item = "- [0.9 全书主线与状态空间接口（The Spine and the Interface）](#preface-sec9)\n"
    text = text.replace(
        "- [0.8 如何使用本书：先建立地图，再深入细节](#preface-sec8)\n",
        "- [0.8 如何使用本书：先建立地图，再深入细节](#preface-sec8)\n" + nav_item,
    )
    sec = '''
<a id="preface-sec9"></a>
## 0.9 全书主线与状态空间接口（The Spine and the Interface）

本书按这条主线推进，而不是按算法名词推进：

$$
\\text{真实世界}\\to\\text{系统}\\to\\text{物理规律}\\to\\text{微分方程}\\to\\textbf{状态空间}\\to\\text{简化与分析}\\to\\text{估计}\\to\\text{规划}\\to\\text{控制}\\to\\text{执行}\\to\\text{学习}\\to\\text{再回到世界}
$$

**状态空间**是从具体物理系统走向通用估计与控制方法的统一接口。机械臂、电机、无人机在物理上不同，但都可以写成 $\\dot x=f(x,u),\\ y=h(x,u)$。

阅读时分三层：

1. **概念层**（第1–3章）：状态、闭环、数学语言；
2. **桥梁层**（第10–12章、第25章）：状态空间、线性化与降阶、开环分析、控制架构；
3. **方法层**：Kalman、A*、PID、LQR、MPC、强化学习等，都是前面接口上长出来的工具。

三个不要混用的轴：

- **对象轴：** 物理系统 → 数学模型；
- **架构轴：** 电流 / 力矩 / 速度 / 位置 / 任务 / 规划；
- **方法轴：** PID / LQR / MPC / RL。

'''
    idx = text.rfind("\n---\n")
    text = text[:idx] + "\n" + sec + text[idx:]
    path.write_text(text, encoding="utf-8")


def parse_sections(path: Path, ch: int) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    return re.findall(rf"^## ({ch}\.\d+) (.+)$", text, re.M)


def write_summary() -> None:
    lines = [
        "# SUMMARY",
        "",
        "# 《从模型到行动：自主系统的统一方法》",
        "",
        "> 真实世界 → 系统 → 物理规律 → 微分方程 → **状态空间** → 系统分析 → 估计 → 规划 → 控制 → 执行 → 学习 → 再回到真实世界",
        ">",
        "> 学习（Learning）横跨各层，反馈（Feedback）将整个系统连接成闭环。状态空间是统一接口。",
        "",
        "- [前言](./00-Preface/00-前言.md)",
        "  - [0.1 为什么需要一套统一的系统观（Unified System View）](./00-Preface/00-前言.md#preface-sec1)",
        "  - [0.2 从“学习算法”到“理解系统”（From Algorithms to Systems）](./00-Preface/00-前言.md#preface-sec2)",
        "  - [0.3 本书的核心架构（Core Architecture）](./00-Preface/00-前言.md#preface-sec3)",
        "  - [0.4 为什么不按照 PID、Kalman、MPC、RL 来组织知识](./00-Preface/00-前言.md#preface-sec4)",
        "  - [0.5 领域建模与通用数学方法](./00-Preface/00-前言.md#preface-sec5)",
        "  - [0.6 贯穿全书的真实系统实例](./00-Preface/00-前言.md#preface-sec6)",
        "  - [0.7 理论、仿真、代码与真实硬件之间的关系](./00-Preface/00-前言.md#preface-sec7)",
        "  - [0.8 如何使用本书：先建立地图，再深入细节](./00-Preface/00-前言.md#preface-sec8)",
        "  - [0.9 全书主线与状态空间接口（The Spine and the Interface）](./00-Preface/00-前言.md#preface-sec9)",
        "",
    ]
    current_part = None
    for n, part, fn, title, sections in CHAPTERS:
        if part != current_part:
            current_part = part
            part_dir, part_name, spine = PARTS[part]
            lines.append(f"## {part_name}")
            lines.append(f"> {spine}")
            lines.append("")
        part_dir = PARTS[part][0]
        path = ROOT / part_dir / fn
        if n <= 5:
            secs = parse_sections(path, n)
        else:
            secs = [(f"{n}.{i}", s) for i, s in enumerate(sections, 1)]
        lines.append(f"- [第{n}章 {title}](./{part_dir}/{fn})")
        for num, sec_title in secs:
            i = num.split(".")[1]
            lines.append(f"  - [{num} {sec_title}](./{part_dir}/{fn}#ch{n}-sec{i})")
        lines.append("")

    # appendix: keep original block from old SUMMARY if present, else reconstruct
    appendix = '''## 附录
- [附录 A 数学基础速查（Mathematics Reference）](./Appendix/A-数学基础速查.md)
  - [A.1 线性代数（Linear Algebra）](./Appendix/A-数学基础速查.md#appa-sec1)
  - [A.2 微积分（Calculus）](./Appendix/A-数学基础速查.md#appa-sec2)
  - [A.3 微分方程（Differential Equations）](./Appendix/A-数学基础速查.md#appa-sec3)
  - [A.4 概率论（Probability）](./Appendix/A-数学基础速查.md#appa-sec4)
  - [A.5 优化（Optimization）](./Appendix/A-数学基础速查.md#appa-sec5)
- [附录 B 空间与刚体数学速查（Rigid-Body Mathematics Reference）](./Appendix/B-空间与刚体数学速查.md)
  - [B.1 旋转矩阵（Rotation Matrix）](./Appendix/B-空间与刚体数学速查.md#appb-sec1)
  - [B.2 四元数（Quaternion）](./Appendix/B-空间与刚体数学速查.md#appb-sec2)
  - [B.3 SO(3)](./Appendix/B-空间与刚体数学速查.md#appb-sec3)
  - [B.4 SE(3)](./Appendix/B-空间与刚体数学速查.md#appb-sec4)
  - [B.5 运动旋量（Twist）](./Appendix/B-空间与刚体数学速查.md#appb-sec5)
  - [B.6 力旋量（Wrench）](./Appendix/B-空间与刚体数学速查.md#appb-sec6)
  - [B.7 伴随变换（Adjoint）](./Appendix/B-空间与刚体数学速查.md#appb-sec7)
  - [B.8 指数映射（Exponential Map）](./Appendix/B-空间与刚体数学速查.md#appb-sec8)
- [附录 C 常见控制算法速查（Control Algorithms Reference）](./Appendix/C-常见控制算法速查.md)
  - [C.1 PID](./Appendix/C-常见控制算法速查.md#appc-sec1)
  - [C.2 LQR](./Appendix/C-常见控制算法速查.md#appc-sec2)
  - [C.3 卡尔曼滤波（Kalman Filter）](./Appendix/C-常见控制算法速查.md#appc-sec3)
  - [C.4 MPC](./Appendix/C-常见控制算法速查.md#appc-sec4)
  - [C.5 iLQR](./Appendix/C-常见控制算法速查.md#appc-sec5)
  - [C.6 DDP](./Appendix/C-常见控制算法速查.md#appc-sec6)
- [附录 D 常见规划算法速查（Planning Algorithms Reference）](./Appendix/D-常见规划算法速查.md)
  - [D.1 A*](./Appendix/D-常见规划算法速查.md#appd-sec1)
  - [D.2 PRM](./Appendix/D-常见规划算法速查.md#appd-sec2)
  - [D.3 RRT](./Appendix/D-常见规划算法速查.md#appd-sec3)
  - [D.4 RRT*](./Appendix/D-常见规划算法速查.md#appd-sec4)
  - [D.5 轨迹优化（Trajectory Optimization）](./Appendix/D-常见规划算法速查.md#appd-sec5)
- [附录 E 软件工具链（Software Toolchain）](./Appendix/E-软件工具链.md)
  - [E.1 Python](./Appendix/E-软件工具链.md#appe-sec1)
  - [E.2 NumPy / SciPy](./Appendix/E-软件工具链.md#appe-sec2)
  - [E.3 MATLAB / Simulink](./Appendix/E-软件工具链.md#appe-sec3)
  - [E.4 CasADi](./Appendix/E-软件工具链.md#appe-sec4)
  - [E.5 Drake](./Appendix/E-软件工具链.md#appe-sec5)
  - [E.6 Pinocchio](./Appendix/E-软件工具链.md#appe-sec6)
  - [E.7 MuJoCo](./Appendix/E-软件工具链.md#appe-sec7)
  - [E.8 ROS 2](./Appendix/E-软件工具链.md#appe-sec8)
  - [E.9 Isaac Sim](./Appendix/E-软件工具链.md#appe-sec9)
- [附录 F 配套实验系统（Companion Experimental Systems）](./Appendix/F-配套实验系统.md)
  - [F.1 质量—弹簧—阻尼系统（Mass–Spring–Damper）](./Appendix/F-配套实验系统.md#appf-sec1)
  - [F.2 直流电机（DC Motor）](./Appendix/F-配套实验系统.md#appf-sec2)
  - [F.3 倒立摆（Inverted Pendulum）](./Appendix/F-配套实验系统.md#appf-sec3)
  - [F.4 真实机械臂（Real Robot Manipulator）](./Appendix/F-配套实验系统.md#appf-sec4)
  - [F.5 四旋翼无人机（Quadrotor）](./Appendix/F-配套实验系统.md#appf-sec5)
  - [F.6 移动机器人（Mobile Robot）](./Appendix/F-配套实验系统.md#appf-sec6)
  - [F.7 四足机器人（Quadruped Robot）](./Appendix/F-配套实验系统.md#appf-sec7)
'''
    lines.append(appendix)
    (ROOT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def delete_obsolete() -> None:
    keep = set()
    for n, part, fn, _, _ in CHAPTERS:
        keep.add(ROOT / PARTS[part][0] / fn)
    keep.add(ROOT / "00-Preface" / "00-前言.md")
    dirs = [
        "01-System", "02-Modeling", "03-Estimation", "04-Planning",
        "05-Control", "06-Execution", "07-Learning", "08-Integration",
        "09-Unified-View",
    ]
    for d in dirs:
        for p in (ROOT / d).glob("*.md"):
            if p not in keep:
                p.unlink()
                print("deleted", p.relative_to(ROOT))


def patch_readme() -> None:
    p = ROOT / "README.md"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "**Modeling → Estimation → Planning → Control → Execution**",
        "**World → Model → State Space → Analysis → Estimation → Planning → Control → Execution**",
    )
    p.write_text(text, encoding="utf-8")


def main() -> None:
    # stubs for ch 6-46
    for n, part, fn, title, sections in CHAPTERS:
        if n <= 5:
            continue
        path = ROOT / PARTS[part][0] / fn
        path.write_text(stub_markdown(n, part, fn, title, sections), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))

    patch_ch1(ROOT / "01-System/01-什么是系统.md")
    patch_ch2(ROOT / "01-System/02-自主系统的完整闭环.md")
    patch_ch3(ROOT / "01-System/03-贯穿全书的数学语言.md")
    patch_ch4(ROOT / "02-Modeling/04-建模的本质.md")
    patch_ch5(ROOT / "02-Modeling/05-从物理规律到微分方程.md")
    patch_preface(ROOT / "00-Preface/00-前言.md")
    delete_obsolete()
    write_summary()
    patch_readme()
    print("SUMMARY.md updated")


if __name__ == "__main__":
    main()
