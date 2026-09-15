import argparse
import json
from pathlib import Path
from .metrics import summarize
from .validation import readiness

parser = argparse.ArgumentParser(description='Everything AI research scaffolding — no trading')
parser.add_argument('command', choices=['preflight', 'demo'])
parser.add_argument('--protocol', default='protocol.json')
args = parser.parse_args()
if args.command == 'preflight':
    missing = readiness(json.loads(Path(args.protocol).read_text()))
    print(json.dumps({'status': 'BLOCKED' if missing else 'FIELDS_PRESENT_REVIEW_REQUIRED',
                      'missing_fields': missing,
                      'note': 'Presence of fields is not validation of their contents.'}, indent=2))
    raise SystemExit(2 if missing else 0)
else:
    print(json.dumps({'evidence': 'SYNTHETIC_NOT_MARKET_RESULTS',
                      'integration_decision': 'NEED MORE DATA',
                      'metrics': summarize([100, 110, 105, 105, 108], [10, -5, 0, 3])}, indent=2, allow_nan=False))
