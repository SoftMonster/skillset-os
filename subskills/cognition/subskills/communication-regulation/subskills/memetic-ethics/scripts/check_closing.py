"""Check a reply's ending against the memetic-ethics closing rule.
PASS: ends with a numbered list of 2-4 distinct, non-empty options (one per line, or inline "1. X  2. Y").
EXEMPT: ends by asking a direct question. FAIL: anything else, with the reason.
usage: python3 check_closing.py < reply.txt"""
import re,sys
def check(text):
    t=text.rstrip(); last=t.splitlines()[-1].strip() if t else ""
    if last.endswith("?") and not re.match(r"^\d+\.",last): return "EXEMPT","ends with a direct question"
    tail=[]
    for line in reversed(t.splitlines()):
        if re.match(r"^\s*\d+\.\s+\S",line): tail.insert(0,line.strip())
        elif line.strip()=="" and not tail: continue
        else: break
    if not tail:                                   # inline form on the last line: "... 1. X  2. Y"
        m=re.search(r"(?:^|\s)(1\.\s.*)$",last)
        if m: tail=[m.group(1)]
    if len(tail)==1: tail=[x.strip() for x in re.split(r"\s{2,}(?=\d+\.\s)",tail[0])]
    if not tail: return "FAIL","no closing numbered list"
    nums=[int(re.match(r"(\d+)\.",x).group(1)) for x in tail]; opts=[re.sub(r"^\d+\.\s*","",x).lower().strip(" .") for x in tail]
    if nums!=list(range(1,len(nums)+1)): return "FAIL",f"numbering {nums} is not 1..n"
    if not 2<=len(opts)<=4: return "FAIL",f"{len(opts)} options (need 2-4)"
    if len(set(opts))!=len(opts): return "FAIL","duplicate options (padding)"
    return "PASS",f"{len(opts)} options"
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1] in ("-h","--help"): print(__doc__); sys.exit(0)
    if sys.stdin.isatty(): sys.exit("pipe a reply in: python3 check_closing.py < reply.txt")
    v,why=check(sys.stdin.read()); print(v,"-",why); sys.exit(0 if v in ("PASS","EXEMPT") else 1)
