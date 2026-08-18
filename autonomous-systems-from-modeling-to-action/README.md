# From Models to Action
## A Systems-First Guide to Autonomous Systems and Robotics

**From Models to Action** is an open, systems-first book project on how autonomous systems are built from first principles to real hardware.

Rather than organizing knowledge around isolated algorithms, the book follows the functional structure of a complete autonomous system:

**World → Model → State Space → Analysis → Estimation → Planning → Control → Execution**

**Learning** can improve each layer, while **Feedback** closes the loop between computation and the physical world.

The book covers mathematical modeling, rigid-body kinematics and dynamics, state estimation, motion planning, classical and modern control, optimal control, real-time execution, system identification, data-driven control, reinforcement learning, and system integration.

A real robot manipulator is used as a recurring experimental platform throughout the book, connecting theory with code, simulation, and physical experiments. Other systems such as motors, quadrotors, mobile robots, and quadrupeds are used as comparative examples.

## Book Structure

1. World and System
2. Modeling
3. Estimation
4. Planning
5. Control
6. Execution
7. Learning
8. Integration
9. Unified View

## Start Reading

- [Full Table of Contents](./SUMMARY.md)
- [Preface](./00-Preface/00-前言.md)
- [Chapter 1: 什么是系统（What Is a System）](./01-System/01-什么是系统.md)

## Repository Layout

```text
.
├── README.md
├── SUMMARY.md
├── 00-Preface/
├── 01-System/
├── 02-Modeling/
├── 03-Estimation/
├── 04-Planning/
├── 05-Control/
├── 06-Execution/
├── 07-Learning/
├── 08-Integration/
├── 09-Unified-View/
├── Appendix/
├── assets/
├── code/
└── experiments/
```

## Writing Convention

Technical terms use the format **中文（English）** when first introduced. Standard abbreviations such as PID, LQR, EKF, RRT, MPC, and RL are retained where appropriate.

All chapter files contain stable explicit anchors so links in `SUMMARY.md` remain reliable on GitHub even when titles contain Chinese characters, punctuation, or mathematical notation.

## Status

This repository currently provides the complete book architecture and chapter templates. Content, code, figures, simulations, and hardware experiments will be added progressively.
