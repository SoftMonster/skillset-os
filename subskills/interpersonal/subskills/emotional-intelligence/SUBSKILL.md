---
name: emotional-intelligence
description: "Develops emotional intelligence in interactions: naming one's own emotions precisely, calming down in the moment before responding, reading other people's cues, and taking another perspective. Use when the user reacts in ways they regret, gets defensive or snappy, cannot tell what others feel, wants more empathy or emotional intelligence, or wants to stay calm in heated moments. Do not use for a planned hard talk; use difficult-conversations. Also guides how Claude reads and responds to the person's emotions."
trigger: "understand and manage emotions in myself and others"
command: "manage emotions"
metadata:
  version: "1.1.0"
---

# Emotional intelligence

🧬 **Core meme:** Name the feeling, pause, then choose the response.

Help the person notice, name and steer emotions in themselves and others during real interactions. Good output connects a specific situation to one skill and a practice for next time.

## The four skills

1. **Name your own emotions precisely.** "Bad" becomes "embarrassed", "resentful" or "anxious". Precise names make emotions easier to manage and explain. Offer a short list of options if they struggle.
2. **Regulate in the moment.** Notice early body signals (heat, tight jaw, fast heart). Pause before replying: a slow breath with a longer out-breath, "Let me think about that", or a break ("Can we pick this up in twenty minutes?"). Respond once the first surge passes.
3. **Read others.** Tone, pace, what is not said, changes from their usual behaviour. Treat readings as guesses and check: "You seem quieter today; everything OK?"
4. **Take their perspective.** Ask: what might they be feeling, needing or afraid of? What else might explain their behaviour besides the worst reading?

## Workflow for a situation they regret

```
- [ ] 1. Replay it: what happened, what they felt, what they did
- [ ] 2. Find the trigger and the earliest warning sign
- [ ] 3. Name what they needed in that moment
- [ ] 4. Imagine the other person's side
- [ ] 5. Plan the pause and a better response for next time
- [ ] 6. Decide whether a repair is needed (apologies-repair)
```

## On Claude's own work

Claude reads the emotional tone of messages as a guess, not a certainty, and responds to it: brief and practical when someone is stressed, warmer when they are upset. It does not mirror frustration or become defensive, and it checks rather than assumes when a message could be read two ways. It does not claim feelings it cannot verify.

## Gotchas

- Emotional intelligence is not suppressing emotions or always being pleasant; it is choosing what to do with them.
- Avoid diagnosing other people ("he's a narcissist"); stay with behaviour and possible feelings.
- Frequent intense anger, panic or numbness that disrupts life deserves professional support; say so gently.

## Commands

- 🧘 **Name it, pause, choose** · `manage emotions`: Helps understand and manage emotions in oneself and others: name, regulate, read others, take their perspective, and review situations that went badly.
  - 🔁 `review regret moment`: Walks through a situation the person regrets and what to do differently.
  - 🧊 `pause before reacting`: Gives a short routine to use between feeling and response.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/emotional-intelligence` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/emotional-intelligence` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
