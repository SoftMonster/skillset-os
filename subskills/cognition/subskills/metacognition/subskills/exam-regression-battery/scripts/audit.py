"""Read battery output on stdin. Rule 1: every PASS check has an NC line. Rule 8: every NC counts only if its main PASSed."""
import re,sys
if len(sys.argv)>1 and sys.argv[1] in ("-h","--help"): print(__doc__.strip()); print("usage: python3 audit.py < battery.out"); sys.exit(0)
if sys.stdin.isatty(): sys.exit("audit.py reads battery output on stdin: python3 audit.py < battery.out")
t=sys.stdin.read(); st={m:s for s,m in re.findall(r"^(PASS|FAIL|KNOWN)\s+(\S+)",t,re.M)}
mains=[m for m,s in st.items() if not m.startswith("NC:") and s=="PASS"]
no_ctrl=[m for m in mains if f"NC:{m}" not in st]; invalid=[m[3:] for m,s in st.items() if m.startswith("NC:") and st.get(m[3:])!="PASS"]
failed=[m for m,s in st.items() if s=="FAIL"]
print(f"checks {len(mains)} | uncontrolled {no_ctrl or 'none'} | invalid controls {invalid or 'none'} | failures {failed or 'none'}")
sys.exit(1 if (no_ctrl or invalid or failed) else 0)
