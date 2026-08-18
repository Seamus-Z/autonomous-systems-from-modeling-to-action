<a id="ch7"></a>
# Chapter 7 线性代数、局部线性化与 Jacobian（Linear Algebra, Local Linearization and Jacobians）

[← 第6章](06-状态与状态空间.md) · [目录](../SUMMARY.md) · [第8章 →](08-概率-优化与几何.md)

**小节导航**

- [7.1 向量、矩阵与线性映射](#ch7-sec1)
- [7.2 秩、零空间与值域](#ch7-sec2)
- [7.3 特征值与特征向量](#ch7-sec3)
- [7.4 模态（Mode）](#ch7-sec4)
- [7.5 正定矩阵与二次型](#ch7-sec5)
- [7.6 非线性函数的局部近似](#ch7-sec6)
- [7.7 工作点（Operating Point）](#ch7-sec7)
- [7.8 平衡点（Equilibrium Point）](#ch7-sec8)
- [7.9 小扰动变量](#ch7-sec9)
- [7.10 多变量 Taylor 展开](#ch7-sec10)
- [7.11 Jacobian 矩阵](#ch7-sec11)
- [7.12 非线性系统的局部线性化](#ch7-sec12)
- [7.13 MIMO 系统的线性化](#ch7-sec13)
- [7.14 局部线性模型与时变线性模型](#ch7-sec14)
- [7.15 Jacobian 为什么会在机器人、EKF、iLQR 中反复出现](#ch7-sec15)

自主系统中的建模、估计、规划与控制虽然解决不同问题，却反复依赖同一种基本操作：先把多个变量组织成向量，再用矩阵描述变量之间的映射；面对非线性关系时，则在当前状态或参考轨迹附近建立局部线性模型。线性代数提供结构，Taylor 展开提供近似原理，Jacobian 矩阵则把二者连接起来。

本章以一台平面二连杆分拣机器人为贯穿例子。它通过两个关节驱动末端执行器运动，相机测量目标位置，控制器计算关节力矩。定义关节角与关节速度为

```math
q=\begin{bmatrix}q_1\\q_2\end{bmatrix}\in\mathbb R^2,
\qquad
\dot q=\begin{bmatrix}\dot q_1\\\dot q_2\end{bmatrix}\in\mathbb R^2,
```

状态与输入分别为

```math
x=\begin{bmatrix}q\\\dot q\end{bmatrix}\in\mathbb R^4,
\qquad
u=\tau=\begin{bmatrix}\tau_1\\\tau_2\end{bmatrix}\in\mathbb R^2.
```

机器人本体是非线性的，末端位置、动力学、相机观测也通常是非线性的。但在一个姿态或一条轨迹附近，这些关系都可以由 Jacobian 给出的一阶映射近似。理解这种“全局非线性、局部线性”的结构，是后续分析和算法设计的共同基础。

<a id="ch7-sec1"></a>
## 7.1 向量、矩阵与线性映射

向量（vector）是定义在向量空间中的对象，坐标列只是它在某组基下的数值表示。若

```math
x=\begin{bmatrix}x_1&\cdots&x_n\end{bmatrix}^T\in\mathbb R^n,
```

则 $`x`$ 可以表示状态、误差、速度或控制输入。欧氏二范数

```math
\|x\|_2=\sqrt{x^Tx}
```

衡量坐标空间中的长度，但它隐含各分量量纲一致且权重相同。若状态同时含有米、弧度和米每秒，直接计算 $`\|x\|_2`$ 往往没有清晰物理意义，应先归一化或使用加权范数。

矩阵更本质的含义是线性映射。对

```math
A\in\mathbb R^{m\times n},\qquad y=Ax,
```

矩阵 $`A`$ 把 $`\mathbb R^n`$ 中的输入映射到 $`\mathbb R^m`$ 中的输出，并满足

```math
A(\alpha x_1+\beta x_2)=\alpha Ax_1+\beta Ax_2.
```

矩阵乘法表示映射的复合：若 $`z=Bx`$ 、 $`y=Az`$ ，则 $`y=ABx`$ 。转置 $`A^T`$ 则与内积的转移有关，因为

```math
y^TAx=(A^Ty)^Tx.
```

这一性质解释了为什么机器人中的速度映射常使用 Jacobian，而力的反向映射使用 Jacobian 的转置。

在线性状态空间模型中，

```math
\dot x=Ax+Bu,\qquad y=Cx+Du,
```

若 $`x\in\mathbb R^n`$ 、 $`u\in\mathbb R^p`$ 、 $`y\in\mathbb R^m`$ ，则

```math
A\in\mathbb R^{n\times n},\quad
B\in\mathbb R^{n\times p},\quad
C\in\mathbb R^{m\times n},\quad
D\in\mathbb R^{m\times p}.
```

维度检查是最基本也最有效的工程检查之一。不过，维度相容并不保证物理正确；坐标系、单位、符号约定和采样时刻同样必须一致。

<a id="ch7-sec2"></a>
## 7.2 秩、零空间与值域

矩阵 $`A\in\mathbb R^{m\times n}`$ 的值域（range space）与零空间（null space）分别定义为

```math
\mathcal R(A)=\{Ax\mid x\in\mathbb R^n\},
```

```math
\mathcal N(A)=\{x\in\mathbb R^n\mid Ax=0\}.
```

秩（rank）是值域的维数：

```math
\operatorname{rank}(A)=\dim\mathcal R(A).
```

由秩—零度定理，

```math
\operatorname{rank}(A)+\dim\mathcal N(A)=n.
```

因此，秩说明映射能产生多少个独立输出方向，零空间则说明哪些输入方向不会出现在输出中。

对于二连杆机器人，末端位置 $`p\in\mathbb R^2`$ 的瞬时速度满足

```math
\dot p=J_p(q)\dot q,
```

其中 $`J_p(q)\in\mathbb R^{2\times2}`$ 是位置 Jacobian。若 $`\operatorname{rank}(J_p)=2`$ ，任意足够小的平面末端速度都可由某个关节速度产生；若秩下降为 $`1`$ ，机器人在该构型只能沿一个瞬时方向运动，这就是运动学奇异性。此时直接求逆 $`J_p^{-1}`$ 会不存在或数值极不稳定。

对于自由度多于任务维度的冗余机器人， $`J\in\mathbb R^{m\times n}`$ 且 $`n>m`$ ，通常存在非零零空间。关节速度可写为

```math
\dot q=J^\dagger \dot p+\left(I-J^\dagger J\right)z,
```

其中 $`J^\dagger`$ 为 Moore–Penrose 伪逆， $`z\in\mathbb R^n`$ 是任意向量。第一项完成主要末端任务，第二项位于 $`\mathcal N(J)`$ 中，可用于避开关节限位、降低能耗或远离奇异构型。

工程上不能把“满秩”和“条件良好”等同起来。矩阵即使理论上满秩，也可能有很小的奇异值，使逆映射放大噪声。奇异值分解

```math
A=U\Sigma V^T
```

可同时揭示秩、主要映射方向和数值条件；实际系统中往往应结合奇异值阈值、阻尼伪逆或正则化，而不是仅依据精确秩作判断。

<a id="ch7-sec3"></a>
## 7.3 特征值与特征向量

对方阵 $`A\in\mathbb R^{n\times n}`$ ，若存在非零向量 $`v\in\mathbb C^n`$ 和标量 $`\lambda\in\mathbb C`$ ，满足

```math
Av=\lambda v,
```

则 $`\lambda`$ 是特征值（eigenvalue）， $`v`$ 是对应的右特征向量（eigenvector）。特征值由特征方程

```math
\det(\lambda I-A)=0
```

确定。即使 $`A`$ 为实矩阵，特征值和特征向量也可能成共轭复数对出现。

连续时间线性系统

```math
\dot x=Ax
```

的解为

```math
x(t)=e^{At}x(0).
```

若 $`A`$ 可对角化为 $`A=V\Lambda V^{-1}`$ ，则

```math
e^{At}=Ve^{\Lambda t}V^{-1}.
```

沿特征向量 $`v_i`$ 的状态分量按 $`e^{\lambda_i t}`$ 演化。因而 $`\operatorname{Re}(\lambda_i)<0`$ 对应指数衰减， $`\operatorname{Re}(\lambda_i)>0`$ 对应指数增长，非零虚部对应振荡。离散系统 $`x_{k+1}=Ax_k`$ 中，相应分量按 $`\lambda_i^k`$ 演化，渐近衰减要求 $`|\lambda_i|<1`$ 。

特征值并不总能完整描述瞬态行为。若矩阵不可对角化，需要 Jordan 形式，解中会出现 $`t^re^{\lambda t}`$ 一类项；若 $`A`$ 是非正规矩阵，即 $`A^TA\neq AA^T`$ ，即使所有特征值都稳定，不同方向的非正交叠加也可能产生显著瞬态放大。因此工程分析中常把特征值与矩阵指数、奇异值、条件数和扰动敏感性结合使用。

<a id="ch7-sec4"></a>
## 7.4 模态（Mode）

模态（mode）是系统中具有特定时间演化规律的动态成分。对可对角化的连续线性系统，若初始状态可表示为

```math
x(0)=\sum_{i=1}^n c_i v_i,
```

则

```math
x(t)=\sum_{i=1}^n c_i e^{\lambda_i t}v_i.
```

每一项 $`c_i e^{\lambda_i t}v_i`$ 可视为一个模态： $`v_i`$ 描述状态各分量如何共同参与， $`\lambda_i`$ 描述该组合随时间如何衰减、增长或振荡。对于共轭特征值

```math
\lambda_{1,2}=-\sigma\pm j\omega,
```

对应的实响应表现为衰减包络 $`e^{-\sigma t}`$ 下频率约为 $`\omega`$ 的振荡。

在机器人关节附近的小扰动模型中，两个关节并不一定分别形成两个模态。惯性和弹性耦合会使某个模态表现为两关节同向运动，另一个表现为两关节反向运动。模态是系统动力学的自然运动模式，不是传感器通道、执行器通道或某个单独状态分量。一个状态通常是多个模态的叠加，一个模态也通常同时涉及多个状态。

还要区分模态是否存在、能否被输入激发、能否从输出观察到。某个内部模态可能由于输入方向不合适而难以控制，也可能由于传感器配置不合适而不出现在测量中。秩、值域和零空间由此会在后续系统分析中重新出现。仅凭响应曲线中“看不到振荡”，不能断言系统不存在相应模态。

<a id="ch7-sec5"></a>
## 7.5 正定矩阵与二次型

对实对称矩阵 $`P=P^T\in\mathbb R^{n\times n}`$ ，若对任意非零 $`x\in\mathbb R^n`$ 都有

```math
x^TPx>0,
```

则称 $`P`$ 为正定矩阵（positive definite matrix），记为 $`P\succ0`$ 。若仅有 $`x^TPx\ge 0`$ ，则称其半正定，记为 $`P\succeq0`$ 。对称矩阵正定等价于所有特征值均为正，也等价于存在可逆矩阵 $`L`$ 使

```math
P=L^TL.
```

工程计算中常使用 Cholesky 分解判断和利用正定性。

二次型（quadratic form）

```math
V(x)=x^TPx
```

定义了椭球形的等值面。若 $`P\succ0`$ ，则

```math
\|x\|_P=\sqrt{x^TPx}
```

是加权范数。较大的权重意味着相应方向上的误差代价更高，但非对角项也会耦合不同状态方向，因此不能只逐项解释矩阵元素。若 $`P`$ 不对称，则

```math
x^TPx=x^T\frac{P+P^T}{2}x,
```

其反对称部分对二次型没有贡献，所以讨论正定性时通常明确要求对称。

机器人的局部控制代价常写为

```math
J=\int_0^T
\left(
\delta x(t)^TQ\delta x(t)
+\delta u(t)^TR\delta u(t)
\right)dt,
```

其中 $`Q\in\mathbb R^{4\times4}`$ 通常满足 $`Q\succeq0`$ ， $`R\in\mathbb R^{2\times2}`$ 满足 $`R\succ0`$ 。 $`Q`$ 惩罚位置和速度偏差， $`R`$ 惩罚控制作用。权重必须结合单位和允许误差选择，例如可用典型尺度 $`s_i`$ 设置对角权重 $`Q_{ii}\propto 1/s_i^2`$ ，避免弧度、弧度每秒和牛顿米之间的数值尺度任意主导优化结果。

正定二次型常被解释为能量或距离，但这种解释需要依据。任意 $`P\succ0`$ 都可构造数学上的广义能量，却未必等于真实机械能；任意二次代价也不自动保证非线性系统的全局稳定。它们首先提供的是局部结构良好、易于计算的度量。

<a id="ch7-sec6"></a>
## 7.6 非线性函数的局部近似

设标量函数 $`f:\mathbb R\rightarrow\mathbb R`$ 在 $`x_0`$ 附近充分光滑，则

```math
f(x_0+\delta x)
=
f(x_0)+f'(x_0)\delta x
+\frac12f''(x_0)\delta x^2
+O(\delta x^3).
```

忽略二阶及更高阶项，得到一阶局部近似

```math
f(x_0+\delta x)\approx f(x_0)+f'(x_0)\delta x.
```

这不是说原函数已经变成线性函数，而是说当 $`\delta x`$ 足够小时，函数增量近似由一个线性映射决定。

例如机器人动力学中的重力项可能包含

```math
g_1(q_1)=a\sin q_1,
```

其中常数 $`a`$ 的单位为牛顿米。在 $`q_{1,0}`$ 附近，

```math
g_1(q_{1,0}+\delta q_1)
\approx
a\sin q_{1,0}
+a\cos q_{1,0}\delta q_1.
```

当 $`q_{1,0}=0`$ 时，局部斜率为 $`a`$ ；当 $`q_{1,0}=\pi/2`$ 时，一阶斜率为零，此时二阶项可能成为主要误差来源。同一个非线性函数在不同位置附近会产生不同的线性模型。

局部近似的有效范围取决于高阶导数、扰动方向和允许误差，不存在对所有问题统一适用的“足够小”。工程上应通过余项界、仿真比较或在线残差检查验证线性化范围。尤其要避免把局部正确误读为全局正确：线性化模型通常不能跨越大角度运动、碰撞切换、饱和边界或接触模式变化。

<a id="ch7-sec7"></a>
## 7.7 工作点（Operating Point）

工作点（operating point）是选定用于描述、分析或控制系统的名义状态与名义输入，记为

```math
(\bar x,\bar u).
```

对于非线性系统

```math
\dot x=f(x,u),\qquad y=h(x,u),
```

工作点处的名义变化率与输出分别为

```math
\dot{\bar x}=f(\bar x,\bar u),\qquad
\bar y=h(\bar x,\bar u).
```

工作点可以是静止构型，也可以是正在运动的某个瞬时状态，因此工作点不必满足 $`f(\bar x,\bar u)=0`$ 。

在分拣任务中，机械臂可能频繁经过某个拾取姿态。若该姿态附近承担精确视觉伺服，可以把对应的关节角、关节速度和力矩选为工作点。选择工作点的工程意义在于：模型精度和控制性能应优先保证在系统实际运行最频繁、风险最高或精度要求最高的区域，而不是抽象地追求全状态空间内同等准确。

工作点应包含足以使名义运动满足模型的信息。仅指定 $`\bar x`$ 而忽略 $`\bar u`$ ，一般无法确定线性化模型；若系统显式依赖时间，还应记录 $`\bar t`$ 。对于周期运动、轨迹跟踪或速度保持任务，单一固定工作点往往不够，需要沿名义轨迹不断更新工作点。

<a id="ch7-sec8"></a>
## 7.8 平衡点（Equilibrium Point）

对自治或恒定输入下的连续系统，若存在 $`(x_e,u_e)`$ 满足

```math
f(x_e,u_e)=0,
```

则 $`x_e`$ 是输入 $`u_e`$ 下的平衡点（equilibrium point）。当系统从 $`x_e`$ 出发并保持 $`u=u_e`$ 时，状态不随时间改变。平衡点一定可以作为工作点，但一般工作点不一定是平衡点。

对二连杆机器人，

```math
M(q)\ddot q+C(q,\dot q)\dot q+g(q)=\tau.
```

若希望机器人静止在 $`q=q_e`$ ，则 $`\dot q_e=0`$ 、 $`\ddot q_e=0`$ ，平衡输入必须满足

```math
\tau_e=g(q_e).
```

因此“关节静止且输入为零”通常不是平衡点，除非该构型的重力矩恰好为零。忘记名义重力补偿，会使线性模型出现持续偏置，并把本应由前馈承担的作用错误地交给反馈控制器。

平衡点还必须与稳定性区分。满足 $`f(x_e,u_e)=0`$ 只说明系统可以停在那里，不说明受到扰动后会返回。倒立摆直立状态是典型的不稳定平衡点。稳定性需要考察平衡点附近扰动的演化；线性化特征值能够在一定条件下提供局部结论，但对特征值实部为零的临界情形，一阶线性化可能无法判定。

<a id="ch7-sec9"></a>
## 7.9 小扰动变量

围绕工作点定义小扰动变量

```math
\delta x=x-\bar x,\qquad
\delta u=u-\bar u,\qquad
\delta y=y-\bar y.
```

它们描述实际量相对名义量的偏差。若 $`\bar x`$ 为常数，则 $`\delta\dot x=\dot x`$ ；若 $`\bar x(t)`$ 是随时间变化的轨迹，则

```math
\delta\dot x=\dot x-\dot{\bar x}.
```

后一项不能遗漏，否则轨迹线性化中会出现错误的常量偏置。

小扰动模型通常写为

```math
\delta\dot x=A\delta x+B\delta u,
\qquad
\delta y=C\delta x+D\delta u.
```

其中各矩阵描述的是增量之间的关系，而不是绝对状态之间的关系。控制器求得 $`\delta u`$ 后，施加到物理系统的输入应恢复为

```math
u=\bar u+\delta u.
```

在机械臂静止保持任务中， $`\bar u=g(q_e)`$ 是重力补偿， $`\delta u`$ 才是抑制位置与速度偏差的反馈力矩。

“小扰动”不是一个固定数值阈值，而是相对于局部曲率、约束裕度和性能要求而言。若关节角误差虽小，却使机械臂靠近奇异构型或碰撞边界，一阶模型仍可能迅速失效。工程实现中应明确扰动允许域，并在超出该域时重新线性化、切换模型或采用非线性方法。

<a id="ch7-sec10"></a>
## 7.10 多变量 Taylor 展开

设标量函数 $`\phi:\mathbb R^n\rightarrow\mathbb R`$ 二阶连续可微，在 $`\bar x`$ 附近有

```math
\phi(\bar x+\delta x)
=
\phi(\bar x)
+\nabla\phi(\bar x)^T\delta x
+\frac12\delta x^TH_\phi(\bar x)\delta x
+O(\|\delta x\|^3),
```

其中梯度 $`\nabla\phi\in\mathbb R^n`$ ，Hessian 矩阵

```math
H_\phi=\nabla^2\phi\in\mathbb R^{n\times n}.
```

梯度描述一阶变化，Hessian 描述局部曲率。在线性化中保留一阶项；在局部二次优化中，还会保留标量代价的二阶项。

对向量函数 $`f:\mathbb R^n\rightarrow\mathbb R^m`$ ，一阶展开为

```math
f(\bar x+\delta x)
=
f(\bar x)+J_f(\bar x)\delta x
+O(\|\delta x\|^2),
```

其中 $`J_f\in\mathbb R^{m\times n}`$ 。若函数同时依赖状态和输入，

```math
f(\bar x+\delta x,\bar u+\delta u)
\approx
f(\bar x,\bar u)
+A\delta x+B\delta u,
```

并定义

```math
A=\left.\frac{\partial f}{\partial x}\right|_{(\bar x,\bar u)},
\qquad
B=\left.\frac{\partial f}{\partial u}\right|_{(\bar x,\bar u)}.
```

这里忽略了 $`\delta x`$ 与 $`\delta u`$ 的二阶项、交叉项以及更高阶项。

Taylor 展开要求函数在展开点附近具有相应光滑性。摩擦死区、饱和、绝对值、碰撞和接触切换处可能不可微，或者左右导数不一致。此时强行计算一个 Jacobian 会掩盖模式变化，应使用分段模型、混杂系统模型、广义导数或平滑近似，并明确近似引入的偏差。

<a id="ch7-sec11"></a>
## 7.11 Jacobian 矩阵

对可微映射 $`f:\mathbb R^n\rightarrow\mathbb R^m`$ ，

```math
f(x)=
\begin{bmatrix}
f_1(x)\\
\vdots\\
f_m(x)
\end{bmatrix},
```

其 Jacobian 矩阵（Jacobian matrix）定义为

```math
J_f(x)=\frac{\partial f}{\partial x}
=
\begin{bmatrix}
\frac{\partial f_1}{\partial x_1}&\cdots&\frac{\partial f_1}{\partial x_n}\\
\vdots&\ddots&\vdots\\
\frac{\partial f_m}{\partial x_1}&\cdots&\frac{\partial f_m}{\partial x_n}
\end{bmatrix}
\in\mathbb R^{m\times n}.
```

本书采用列向量约定，因此局部增量满足

```math
\delta f\approx J_f(x)\delta x.
```

不同资料可能采用分子布局或分母布局，使用公式前必须核对维度和约定。

二连杆末端位置为

```math
p(q)=
\begin{bmatrix}
l_1\cos q_1+l_2\cos(q_1+q_2)\\
l_1\sin q_1+l_2\sin(q_1+q_2)
\end{bmatrix},
```

其中 $`l_1,l_2`$ 为连杆长度。位置 Jacobian 为

```math
J_p(q)=
\begin{bmatrix}
-l_1\sin q_1-l_2\sin(q_1+q_2)&-l_2\sin(q_1+q_2)\\
l_1\cos q_1+l_2\cos(q_1+q_2)&l_2\cos(q_1+q_2)
\end{bmatrix}.
```

它既给出小位移关系 $`\delta p\approx J_p\delta q`$ ，也通过对时间求导给出精确瞬时速度关系 $`\dot p=J_p\dot q`$ 。前者是有限增量的一阶近似，后者是在可微轨迹上的瞬时链式法则，二者不应混淆。

Jacobian 还服从链式法则。若 $`y=g(z)`$ 、 $`z=f(x)`$ ，则

```math
J_{g\circ f}(x)=J_g(f(x))J_f(x).
```

这使复杂感知与动力学模型能够由局部模块组合。工程上 Jacobian 可以通过符号推导、自动微分、解析代码或有限差分获得。有限差分简单，但步长过大会产生截断误差，过小则会放大浮点误差；自动微分精确到机器计算图，却不能修复不可微模型、坐标约定错误或错误的物理方程。

<a id="ch7-sec12"></a>
## 7.12 非线性系统的局部线性化

考虑连续时间非线性系统

```math
\dot x=f(x,u),\qquad y=h(x,u),
```

其中 $`x\in\mathbb R^n`$ 、 $`u\in\mathbb R^p`$ 、 $`y\in\mathbb R^m`$ 。在工作点 $`(\bar x,\bar u)`$ 附近进行一阶展开：

```math
\dot x
\approx
f(\bar x,\bar u)+A\delta x+B\delta u,
```

```math
y
\approx
h(\bar x,\bar u)+C\delta x+D\delta u,
```

其中

```math
A=\left.\frac{\partial f}{\partial x}\right|_{(\bar x,\bar u)},
\quad
B=\left.\frac{\partial f}{\partial u}\right|_{(\bar x,\bar u)},
```

```math
C=\left.\frac{\partial h}{\partial x}\right|_{(\bar x,\bar u)},
\quad
D=\left.\frac{\partial h}{\partial u}\right|_{(\bar x,\bar u)}.
```

若工作点是满足 $`f(\bar x,\bar u)=0`$ 的平衡点，则得到

```math
\delta\dot x=A\delta x+B\delta u,
\qquad
\delta y=C\delta x+D\delta u.
```

对于机械臂，令 $`v=\dot q`$ ，则一阶状态方程为

```math
\dot x=
\begin{bmatrix}
\dot q\\
M(q)^{-1}\left[\tau-C(q,v)v-g(q)\right]
\end{bmatrix}
=f(x,\tau).
```

在静止平衡点 $`x_e=[q_e^T,0^T]^T`$ 、 $`\tau_e=g(q_e)`$ 附近，理想无摩擦情况下有结构

```math
A=
\begin{bmatrix}
0&I\\
-M_e^{-1}K_g&0
\end{bmatrix},
\qquad
B=
\begin{bmatrix}
0\\
M_e^{-1}
\end{bmatrix},
```

其中 $`M_e=M(q_e)`$ ， $`K_g=\left.\frac{\partial g}{\partial q}\right|_{q_e}`$ 。若存在黏性阻尼矩阵 $`F_v`$ ，则 $`A`$ 的右下块还包含 $`-M_e^{-1}F_v`$ 。该结构表明，质量矩阵决定力矩到加速度的局部映射，重力梯度决定姿态偏差产生的恢复或发散趋势。

线性化前后还必须保持连续与离散模型的一致性。若离散系统直接写为

```math
x_{k+1}=F(x_k,u_k),
```

则

```math
A_k=\frac{\partial F}{\partial x},\qquad
B_k=\frac{\partial F}{\partial u}.
```

若先得到连续矩阵 $`A_c,B_c`$ ，在零阶保持假设下应使用

```math
A_d=e^{A_c\Delta t},\qquad
B_d=\int_0^{\Delta t}e^{A_c\tau}B_c\,d\tau,
```

而 $`A_d\approx I+A_c\Delta t`$ 、 $`B_d\approx B_c\Delta t`$ 只是小采样周期下的近似。

<a id="ch7-sec13"></a>
## 7.13 MIMO 系统的线性化

多输入多输出系统（multiple-input multiple-output, MIMO）与单输入单输出系统使用完全相同的线性化原理。若 $`x\in\mathbb R^n`$ 、 $`u\in\mathbb R^p`$ 、 $`y\in\mathbb R^m`$ ，则局部模型仍为

```math
\delta\dot x=A\delta x+B\delta u,
\qquad
\delta y=C\delta x+D\delta u,
```

只是 $`B`$ 有 $`p`$ 列、 $`C`$ 有 $`m`$ 行，矩阵中的非对角元素显式描述通道耦合。线性化的限制来自局部近似和光滑性，而不是输入输出数量。

对二关节机器人，两个力矩同时影响两个关节加速度，因为通常

```math
M(q)^{-1}=
\begin{bmatrix}
m_{11}(q)&m_{12}(q)\\
m_{21}(q)&m_{22}(q)
\end{bmatrix}
```

不是对角矩阵。于是 $`\tau_1`$ 不只作用于 $`\ddot q_1`$ ， $`\tau_2`$ 也不只作用于 $`\ddot q_2`$ 。若相机同时输出末端横纵坐标，则观测矩阵中的关节位置部分为 $`J_p(q)`$ ，每个像平面或笛卡尔输出也通常依赖多个关节变量。

MIMO 线性化之后仍需检查结构，而不能因为得到矩阵就默认系统“可控制、可观测”。例如某一执行器失效会使 $`B`$ 的有效方向减少，某一构型下运动学 Jacobian 降秩会使输出对部分状态方向失去一阶敏感性。多通道系统尤其需要结合秩、奇异值和尺度归一化分析，避免把强耦合错误地当作多个独立的标量回路。

<a id="ch7-sec14"></a>
## 7.14 局部线性模型与时变线性模型

固定工作点附近得到的矩阵 $`A,B,C,D`$ 为常数，对应局部线性时不变模型（linear time-invariant, LTI）。它适合平衡点稳定、姿态保持和窄范围调节。然而分拣机器人从传送带取物并移动到料箱时，名义状态持续变化，质量矩阵、重力梯度和运动学 Jacobian 也随构型变化，单一固定模型无法覆盖整条轨迹。

设名义轨迹满足

```math
\dot{\bar x}(t)=f(\bar x(t),\bar u(t)).
```

沿轨迹逐点线性化得到

```math
\delta\dot x(t)=A(t)\delta x(t)+B(t)\delta u(t),
```

其中

```math
A(t)=
\left.\frac{\partial f}{\partial x}\right|_{(\bar x(t),\bar u(t))},
\qquad
B(t)=
\left.\frac{\partial f}{\partial u}\right|_{(\bar x(t),\bar u(t))}.
```

这称为线性时变模型（linear time-varying, LTV）。它对扰动是线性的，但矩阵随时间变化；“线性”与“时不变”是两个不同性质。

数字系统中常使用离散形式

```math
\delta x_{k+1}=A_k\delta x_k+B_k\delta u_k,
\qquad
\delta y_k=C_k\delta x_k+D_k\delta u_k.
```

矩阵可以离线沿参考轨迹预计算，也可以根据在线状态估计实时更新。前者计算稳定但难以应对大幅偏离，后者适应性更强却依赖可靠的状态估计和实时求导。

局部模型族并不自动成为全局模型。在线调度时应避免在不相容坐标、不同接触模式或跨越奇异区域的模型之间直接插值。若实际状态偏离名义轨迹过大，应重新规划或重新线性化，而不是无限延长某个局部模型的适用范围。

<a id="ch7-sec15"></a>
## 7.15 Jacobian 为什么会在机器人、EKF、iLQR 中反复出现

Jacobian 反复出现，并不是因为这些算法偶然选择了同一种记号，而是因为它们都需要回答同一个问题：

> 当输入、状态或参数发生一个很小的变化时，输出、动力学或代价会如何变化？

机器人运动学使用

```math
\delta p\approx J_p(q)\delta q,
\qquad
\dot p=J_p(q)\dot q
```

把关节变化映射为末端变化。由虚功关系

```math
F^T\delta p=\tau^T\delta q
```

以及 $`\delta p=J_p\delta q`$ ，得到

```math
\tau=J_p(q)^TF.
```

因此速度使用正向 Jacobian，力使用转置映射；这来自功率或虚功对偶关系，而不是把速度公式形式上“倒过来”。

扩展卡尔曼滤波（extended Kalman filter, EKF）面对非线性过程模型和观测模型

```math
x_{k+1}=F(x_k,u_k)+w_k,
\qquad
y_k=h(x_k)+v_k
```

时，使用 Jacobian

```math
A_k=\left.\frac{\partial F}{\partial x}\right|_{\hat x_k,u_k},
\qquad
H_k=\left.\frac{\partial h}{\partial x}\right|_{\hat x_k^-}
```

传播局部状态误差与协方差。例如预测协方差近似为

```math
P_{k+1}^-=A_kP_kA_k^T+Q_k.
```

这里 $`A_k`$ 传播过程扰动方向， $`H_k`$ 描述观测对状态误差的局部敏感性。若观测 Jacobian 在某方向接近零，传感器在该工作点附近便难以提供该方向的一阶信息。

迭代线性二次调节器（iterative linear quadratic regulator, iLQR）沿当前名义轨迹线性化动力学，

```math
\delta x_{k+1}\approx A_k\delta x_k+B_k\delta u_k,
```

并把代价在局部近似为二次函数，再通过反向递推求出局部反馈律

```math
\delta u_k=k_k+K_k\delta x_k.
```

随后前向滚动非线性动力学，更新名义轨迹并重复迭代。因此 iLQR 的基本循环不是“一次线性化解决整个非线性问题”，而是“线性化、求局部改进、回到非线性模型验证、再次线性化”。

三类应用的 Jacobian 分别作用于运动学映射、概率误差传播和动态优化，但共同本质都是切空间中的一阶敏感度。它们也共享同样的边界：线性化点错误、坐标定义不一致、函数不可微、扰动过大或 Jacobian 条件不良，都会使算法退化。可靠实现应进行维度检查、有限差分抽检、单位测试、奇异值监测，并比较局部预测与真实非线性增量：

```math
r(\delta x)
=
f(x+\delta x)-f(x)-J_f(x)\delta x.
```

当 $`\|\delta x\|\to0`$ 且函数可微时，应有 $`\|r(\delta x)\|/\|\delta x\|\to0`$ 。这一检查比仅确认“代码能运行”更能发现 Jacobian 的符号、索引和坐标错误。

## 本章小结

本章从线性映射出发，建立了理解自主系统局部结构的一条完整主线：

1. 向量组织状态、输入、输出和误差，矩阵表示这些空间之间的线性映射。
2. 秩刻画独立映射方向，值域刻画可到达的输出方向，零空间刻画不会影响当前任务的内部变化；奇异值进一步揭示数值敏感性。
3. 特征值和特征向量描述线性动态的自然方向，模态则把空间结构与时间演化结合起来。
4. 正定矩阵与二次型提供加权距离、局部能量和优化代价，但其物理意义必须由模型与单位支持。
5. Taylor 展开说明了为何光滑非线性函数在足够小的邻域内可以由线性映射近似，Jacobian 正是这一线性映射的矩阵表示。
6. 工作点是建模与设计所围绕的名义状态和输入，平衡点则额外满足状态变化率为零。通过小扰动变量，可以把绝对量问题转换为名义运动附近的偏差问题。
7. 非线性 SISO 与 MIMO 系统都可按同一规则线性化；固定工作点产生局部 LTI 模型，沿名义轨迹线性化则产生 LTV 模型。
8. 机器人运动学、EKF 和 iLQR 都依赖 Jacobian，因为它们分别需要传播几何增量、估计误差和轨迹扰动。

本章得到的核心接口可以压缩为

```math
\boxed{
\text{非线性模型}
\;\xrightarrow[\text{工作点或轨迹}]{\text{Taylor / Jacobian}}\;
\text{局部线性模型}
}
```

以及

```math
\boxed{
\delta\dot x=A\delta x+B\delta u,
\qquad
\delta y=C\delta x+D\delta u
}
```

下一章将以这些局部线性对象为接口，进一步讨论如何从模型结构中提取可分析、可计算和可用于决策的系统性质。需要始终保留的边界意识是：线性模型不是非线性世界的替代品，而是围绕明确名义状态、在明确误差范围内服务于分析、估计与控制的局部工具。

---

[← 第6章](06-状态与状态空间.md) · [目录](../SUMMARY.md) · [第8章 →](08-概率-优化与几何.md)
