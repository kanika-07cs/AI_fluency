## Overview

This project demonstrates three different approaches to solving the same private-data problem using a **Hostel Complaint Assistant**:

1. Plain Chatbot
2. Rule-Based Workflow
3. Tool-Using AI Agent

The project shows how each approach handles user requests, private data, tools, decision-making, and multi-step tasks.

---

## Scenario

The chosen scenario is a **Hostel Complaint Assistant**.

A student can ask questions such as:

> "What is the status of my hostel complaint?"

Example private data:

- Student ID: STU1024
- Student Name: Kanika
- Room Number: A-204
- Complaint ID: C102
- Complaint: Fan not working
- Complaint Status: In Progress

---

## Approaches

### 1. Plain Chatbot

The chatbot mainly uses an **LLM to generate a response** based on the information provided in the prompt.

```text
User Question
      ↓
     LLM
      ↓
Response