---
name: simulation
description: "Runs scenarios forward: mental simulation and rehearsal, scenario planning across several futures, role-play of people and conversations, and quantitative simulation in code such as Monte Carlo, with explicit assumptions and ranges. For people, covers rehearsing events, planning for different futures and testing what-ifs; for Claude, covers tracing code or plans step by step before running them, running actual simulations with code, and role-playing others honestly as simulations rather than facts. Use when the user wants to explore what-ifs, plan for different futures, rehearse an event, model risk or outcomes, or run a simulation."
trigger: "imagine or model how a scenario might play out"
metadata:
  version: "1.0.0"
---

# 🎲 Simulation

🧬 **Core meme:** Run it forward with stated assumptions and ranges, not one guess.

Run a situation forward before it happens, in the mind or in code, to prepare, test and choose. The brain is a prediction machine: it simulates outcomes constantly. Doing it deliberately, with explicit assumptions and several scenarios, turns vague worry or hope into usable plans.

## Types

- **Mental rehearsal:** step through an event in detail (a talk, an interview, a hard conversation), including what could go wrong and the response.
- **Scenario planning:** three or four plausible futures (best, worst, likely, wild card), with signs to watch and actions for each.
- **Role-play:** simulate a person to practise with; always a model, not the real person.
- **Quantitative simulation:** a model in a spreadsheet or code; Monte Carlo runs many random trials to show a range of outcomes rather than one number.

## For people

```
- [ ] 1. Define the question
- [ ] 2. List the key uncertainties
- [ ] 3. Build scenarios or a model
- [ ] 4. Run it
- [ ] 5. Find robust actions and signposts
```

Example: *Will savings last through a career break? Uncertainties: months out of work (3–9), monthly costs (£1.8k–2.3k). Run the combinations: in the worst case the money runs out in month 7. Robust action: cut costs to £2k now; signpost: no offer by month 4 → take contract work.*

For rehearsing conversations, Claude can play the other person (see `difficult-conversations` in interpersonal).

## For Claude

- **Trace before running:** walk through code or a plan step by step with a concrete example to catch errors early.
- **Then actually run it** when tools allow; a real run beats a mental trace. Use code for any quantitative simulation, and show the assumptions and ranges.
- **Role-play honestly:** simulated people are models, not predictions of what a real person will say; say so when it matters.
- **Scenarios over single forecasts** for uncertain futures.

## Gotchas

- A simulation is only as good as its assumptions; state them and vary them.
- Mental rehearsal helps performance; endless replay of worst cases is worry, not planning (see `mindset-resilience` in self-improvement).
- Precise-looking outputs from rough inputs create false confidence; report ranges.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents cognition/reasoning/simulation` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review cognition/reasoning/simulation` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
