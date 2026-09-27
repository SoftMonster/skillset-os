---
name: feedback
description: "Covers feedback in both directions: gives specific, behaviour-based feedback and praise that lands, and helps the user receive criticism without defensiveness, sort useful from not, and act on it. Use when the user needs to give feedback to a colleague, report, friend or family member, write a performance review, was criticised and is upset, or wants to ask for better feedback. Also guides how Claude gives and takes feedback."
trigger: "give or receive feedback well"
metadata:
  version: "1.1.0"
---

# Feedback

🧬 **Core meme:** Specific behaviour, real impact, then a question.

Help the person give feedback that changes things without damaging the relationship, and take feedback in without being flattened by it.

## Giving feedback

```
- [ ] 1. Check the purpose and timing
- [ ] 2. Write it as situation, behaviour, impact
- [ ] 3. Add the request or question
- [ ] 4. Plan the delivery
```

1. **Purpose and timing.** Feedback is for helping them improve or understand impact, not venting. Give it soon, in private, when there is time to talk.
2. **Situation, behaviour, impact (SBI):** "In Monday's client call (situation), you interrupted Priya twice (behaviour), and she stopped contributing (impact)."
3. **Request or question:** "What was going on for you?" then "Next time, could you let her finish?"
4. **Delivery:** calm, direct, about behaviour not character ("you interrupted", not "you're rude"). Skip the praise sandwich; it teaches people to distrust praise. Give praise separately and just as specifically.

For written feedback and performance reviews: concrete examples, the impact, what good looks like, and support offered.

## Receiving feedback

1. **Listen and let it land.** Breathe; the first reaction is often defensive. Say "Thanks, let me think about that."
2. **Ask for specifics:** "Can you give me an example?" "What would good look like?"
3. **Sort it later.** Is it about what I did, how I did it, or who is saying it? Take the useful part even if the delivery was poor.
4. **Act and close the loop:** tell them what you changed.

To get better feedback, ask a specific question: "What's one thing I could do differently in these meetings?"

## On Claude's own work

Claude gives the person feedback on their work the same way: specific, tied to impact, honest rather than flattering, with praise that is earned. When the person gives Claude feedback, it takes it in, asks for an example if unclear, fixes what is right, and says what it changed, without grovelling or getting defensive.

**Memetic check before it's sent:** feedback and review wording travel beyond this chat, so check them with `memetic-ethics` in cognition/communication-regulation: accurate, fair to the people involved, and clear even when quoted alone.

## Gotchas

- Feedback about identity or protected characteristics is not feedback; it may be discrimination.
- Harsh criticism that sticks for days may be hitting self-criticism; `mindset-resilience` in self-improvement helps.

## Commands

- 🎁 **Behaviour, impact, question** · `give feedback`: Gives or receives feedback well: situation, behaviour, impact and a request; or listening, asking for specifics, sorting and acting.
  - ✍️ `draft sbi feedback`: Drafts feedback in situation-behaviour-impact form with a question or request.
  - 📥 `receive feedback`: Helps the person take in feedback, ask for specifics and decide what to act on.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents interpersonal/feedback` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review interpersonal/feedback` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
