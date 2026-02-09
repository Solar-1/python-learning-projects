# Python Learning Projects

A small collection of Python projects I built while learning core programming and simulation concepts.

## What This Repo Contains

- `src/learning_projects/pendulum_sim.py`: A chained pendulum visualization and interaction demo built with Pygame.
- `src/learning_projects/physics_simulation.py`: A collision/reflection sandbox inside a circular boundary.
- `src/vector_operations/__init__.py`: My custom vector-operations library used by both projects.

## About The Vector Operations Library

`vector_operations` is a custom utility module I wrote for this codebase. It provides:

- 2D/3D vector construction and conversion helpers
- vector arithmetic (`add`, `subtract`, `scale`, `normalize`)
- geometry operations (`dot`, `cross`, projection, reflection)
- angle/euler conversion helpers for simulation-style workflows

This library was designed for readability and fast iteration while learning physics-based scripting.

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run a project from the repo root:
   - `python -m src.learning_projects.pendulum_sim`
   - `python -m src.learning_projects.physics_simulation`

## Repository Structure

```text
Python-Projects/
  src/
    learning_projects/
      __init__.py
      pendulum_sim.py
      physics_simulation.py
    vector_operations/
      __init__.py
  requirements.txt
  .gitignore
  README.md
```

## Purpose

This repository is intentionally simple and focused on learning progress. It is structured to be clean, readable, and ready to publish as a portfolio repo.
