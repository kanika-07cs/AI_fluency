## Overview

This project demonstrates and compares three different approaches for solving problems using Large Language Models (LLMs):

1. Direct Prompting
2. Chain-of-Thought Style Prompting
3. ReAct (Reasoning + Action) Agent

The scenario used in this project is a **Student Train Travel Assistant**.

The assistant handles questions related to train fares, discounts, expenses, and student travel budgets.

---

## Scenario

A student is travelling from Coimbatore to Chennai.

The available train information used by the tool is:

| Train | Fare |
|---|---:|
| Cheran Express | ₹650 |
| Brindavan Express | ₹550 |

The project contains questions that require:

- Simple direct answers
- Numerical reasoning
- External information through a tool
- Combining tool results with reasoning

---

## Approaches Demonstrated

### 1. Direct Prompting

In direct prompting, the question is given directly to the LLM.

Example:

```text
A student has ₹1000.
The train ticket costs ₹650 and food costs ₹200.
How much money remains?