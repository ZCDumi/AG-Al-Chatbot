"""
CLI tool to create a staff account for the Analytics Group Chatbot admin API.

Deliberately NOT exposed as an HTTP endpoint — creating a staff account is
an action for whoever has shell access to the server, not something that
should ever be reachable over the network. Run this from the same machine/
deploy environment as the backend.

Usage:
    python3 -m app.create_staff --username jane --full-name "Jane Doe"

You'll be prompted for a password (hidden input, via getpass). To also
supply the password non-interactively (e.g. in a scripted deploy), use:
    python3 -m app.create_staff --username jane --password "..." --full-name "Jane Doe"

Run with --list to see existing staff accounts instead of creating one:
    python3 -m app.create_staff --list
"""
import argparse
import getpass
import sys

from .auth import hash_password
from . import crud, models
from .database import SessionLocal, engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or list Analytics Group staff accounts.")
    parser.add_argument("--username", help="Login username for the new staff account")
    parser.add_argument("--full-name", default=None, help="Display name (optional)")
    parser.add_argument(
        "--password",
        default=None,
        help="Password (optional — if omitted, you'll be prompted securely)",
    )
    parser.add_argument(
        "--list", action="store_true", help="List existing staff accounts and exit"
    )
    args = parser.parse_args()

    # Make sure tables exist (safe to call repeatedly; no-op if already created).
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if args.list:
            staff = db.query(models.StaffUser).order_by(models.StaffUser.created_at.asc()).all()
            if not staff:
                print("No staff accounts yet.")
                return
            print(f"{'username':<20} {'full_name':<25} {'active':<8} created_at")
            for s in staff:
                print(f"{s.username:<20} {(s.full_name or ''):<25} {str(s.is_active):<8} {s.created_at}")
            return

        if not args.username:
            parser.error("--username is required unless using --list")

        if crud.get_staff_by_username(db, args.username):
            print(f"Error: a staff account with username '{args.username}' already exists.", file=sys.stderr)
            sys.exit(1)

        password = args.password
        if not password:
            password = getpass.getpass("Password: ")
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                print("Error: passwords did not match.", file=sys.stderr)
                sys.exit(1)

        if len(password) < 8:
            print("Error: password must be at least 8 characters.", file=sys.stderr)
            sys.exit(1)

        hashed = hash_password(password)
        staff = crud.create_staff_user(
            db, username=args.username, hashed_password=hashed, full_name=args.full_name
        )
        print(f"Created staff account '{staff.username}' (id={staff.id}).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
