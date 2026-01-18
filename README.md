## UE5 Tools Library

A focused collection of **Python tools for Unreal Engine 5** for editor automation and pipeline workflows (MRQ helpers, camera/sequencer utilities, and other productivity scripts). The goal is simple: **reliable tools you can drop into a project and run**.

This repo will keep evolving as new utilities are added and existing ones get improved.

### Tools included
- **Movie Render Queue helpers**: automate MRQ job setup and rendering.
- **Camera + Sequencer utilities**: generate cameras, create Level Sequences, batch workflows.
- **Editor automation**: remove repetitive clicks and keep pipelines consistent.

### Requirements
- Unreal Engine 5
- Python enabled (Editor Scripting Utilities recommended)
- Movie Render Queue plugin (for MRQ scripts)

### Usage

Run scripts inside the UE5 Editor (Python console / Editor Utility).

**Option A: Python Console**
1. UE5 → `Window > Developer Tools > Output Log`
2. Switch to **Python** mode
3. Run:
```python
import unreal
unreal.log("Python ready")
