"""
One-time seeder: creates all accounts from accounts.csv against the API.

Run ONCE before load testing (idempotent — re-running is safe, existing
accounts just report "already exists"):

    kubectl port-forward svc/fastapi-app 5000:5000   # in another pane
    python seed_accounts.py --host http://localhost:5000

Then run locust with the seeded accounts; the locustfile only logs in.
"""

import csv
import sys
import argparse
from pathlib import Path

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://localhost:5000",
                        help="Base URL of the API (default: http://localhost:5000)")
    parser.add_argument("--csv", default="accounts.csv",
                        help="Path to accounts CSV (default: accounts.csv)")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"CSV not found: {csv_path}")

    with csv_path.open(newline="") as f:
        accounts = list(csv.DictReader(f))

    if not accounts:
        sys.exit(f"No accounts in {csv_path}")

    created, existed, failed = 0, 0, 0

    for acct in accounts:
        email = acct["email"]
        try:
            resp = requests.post(
                f"{args.host}/users/",
                json={"email": email, "password": acct["password"]},
                timeout=10,
            )
        except requests.RequestException as e:
            print(f"[ERR ] {email}: request failed — {e}")
            failed += 1
            continue

        if resp.status_code == 201:
            print(f"[NEW ] {email}")
            created += 1
        elif resp.status_code in (400, 409, 500):
            # already exists / unique-constraint violation — fine for a re-run
            print(f"[SKIP] {email} (already exists)")
            existed += 1
        else:
            print(f"[FAIL] {email}: {resp.status_code} {resp.text[:120]}")
            failed += 1

    print("-" * 40)
    print(f"created={created}  existed={existed}  failed={failed}  total={len(accounts)}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()