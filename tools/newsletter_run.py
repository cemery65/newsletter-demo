import argparse
import os
import sys

from fetch_perplexity import fetch_research
from generate_newsletter import generate_newsletter
from send_gmail import send_email

DRAFT_PATH = os.path.join(os.path.dirname(__file__), "..", ".tmp", "newsletter_draft.html")


def main():
    parser = argparse.ArgumentParser(description="Generate and send a newsletter.")
    parser.add_argument("--topic", required=True, help="Newsletter topic to research")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--from", dest="sender", required=True, help="Sender email address")
    parser.add_argument("--logo", default="", help="Logo image URL to embed in header")
    args = parser.parse_args()

    print(f"[1/3] Fetching research for: {args.topic}")
    research = fetch_research(args.topic)

    print("[2/3] Generating newsletter...")
    newsletter = generate_newsletter(args.topic, research, logo_url=args.logo)
    print(f"      Subject: {newsletter['subject']}")

    draft_path = os.path.abspath(DRAFT_PATH)
    os.makedirs(os.path.dirname(draft_path), exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(newsletter["html_body"])
    print(f"\n      Draft saved to: {draft_path}")
    print("      Open it in a browser to review before sending.\n")

    answer = input("Send this newsletter? [y/N]: ").strip().lower()
    if answer != "y":
        print("Aborted. Draft is saved — run again and approve when ready.")
        return 0

    print(f"[3/3] Sending to {args.to}...")
    send_email(
        to=args.to,
        sender=args.sender,
        subject=newsletter["subject"],
        html_body=newsletter["html_body"],
    )

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
