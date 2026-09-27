---
name: security-review
description: "Audits the user's own code and configuration defensively against the OWASP Top 10 and common weaknesses (injection, broken access control, secrets in code, unsafe deserialisation, SSRF, weak crypto, vulnerable dependencies) and returns prioritised findings with fixes. Use when the user asks for a security review or audit, asks whether code is secure, wants to harden auth, input handling or configuration, or needs to fix a reported vulnerability or dependency advisory. Do not use for writing exploits or attacking systems."
trigger: "audit code for security vulnerabilities or harden an application"
metadata:
  version: "1.0.0"
---

# Security review

🧬 **Core meme:** Assume input is hostile, rank the findings, and fix the worst first.

Find and fix security weaknesses in the person's own code, configuration and dependencies before an attacker does. Output is a prioritised list of findings, each with evidence, impact and a fix, plus quick wins for hardening. This is defensive work: explain how an issue could be abused only as much as needed to justify its priority, and never write working exploits or attack tooling.

## Workflow

```
- [ ] 1. Scope and threat model
- [ ] 2. Run automated scanners
- [ ] 3. Review manually by risk area
- [ ] 4. Rate and write findings
- [ ] 5. Fix and verify
```

1. **Scope.** Establish what the system does, what data it holds, who its users and trust boundaries are (internet, internal, admin), and which parts are in scope. Five lines of threat model direct attention better than a full checklist.
2. **Scanners** (install from PyPI or npm in the sandbox; run what fits the stack):
   ```bash
   pip install semgrep bandit pip-audit --break-system-packages -q
   semgrep scan --config auto --metrics=off <repo>    # multi-language rules
   bandit -r <repo> -q                                  # Python
   pip-audit -r requirements.txt                        # Python deps
   npm audit --omit=dev                                 # Node deps
   git log -p | grep -nEi '(api[_-]?key|secret|password|token)\s*[:=]'   # rough secret sweep
   ```
   Treat scanner output as leads. Confirm each by reading the code, and discard false positives with a one-line reason.
3. **Manual review.** Work through [security-checklist.md](security-checklist.md), starting with the areas the threat model says matter most. Follow untrusted input from where it enters to every place it is used.
4. **Findings.** Rate each finding as Critical, High, Medium or Low from exploitability and impact (for example, unauthenticated remote data access is Critical; a missing security header is Low). Use the format below and order by severity.
5. **Fix.** When asked, implement fixes with regression tests (for example, a test that an injected payload is treated as data, or that user A gets 403 on user B's object). Re-run the scanners.

## Finding format

```
**[High] Missing object-level authorisation on invoice download** — `billing/views.py:88`
Evidence: `get_invoice(id)` loads by ID without checking the requester owns it.
Impact: any logged-in user can download other customers' invoices by changing the ID.
Fix: scope the lookup to the current account.
    invoice = Invoice.objects.get(id=invoice_id, account=request.user.account)
Reference: OWASP A01 Broken Access Control, CWE-639.
```

## Gotchas

- Broken access control is the most common serious issue and scanners rarely find it. Always check authorisation per object on every endpoint by hand.
- A secret that was ever committed is compromised even after deletion. The fix is to rotate it, then purge history (`git filter-repo`) if needed.
- Client-side validation is not a control. Check that the server enforces everything.
- Do not roll your own crypto, password hashing or session handling. Recommend the framework's built-in or a vetted library.
- If the request moves from reviewing the person's own code to attacking systems they do not own, decline that part.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/security-review` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/security-review` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
