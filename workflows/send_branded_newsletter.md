# Workflow: Send Branded Newsletter

## Objective
Research a topic with Perplexity, generate a branded HTML newsletter, and send it via Gmail in one command.

## Required Inputs
| Input | Flag | Required | Description |
|-------|------|----------|-------------|
| Topic | `--topic` | Yes | The subject to research and write about |
| Recipient | `--to` | Yes | Destination email address |
| Sender | `--from` | Yes | Gmail address in GMAIL_SMTP_USER |
| Logo URL | `--logo` | No | Hosted image URL embedded in the header |

## Environment Variables (`.env`)
```
PREPLEXITY_API_KEY=...
GMAIL_SMTP_USER=...
GMAIL_SMTP_PASSWORD=...   # Gmail App Password (not account password)
```

## Tools (in order)
1. `tools/fetch_perplexity.py` — queries Perplexity `sonar` model, returns overview + bullet points
2. `tools/generate_newsletter.py` — renders branded HTML email from research text
3. **Manual review** — draft saved to `.tmp/newsletter_draft.html`; open in a browser and approve at the prompt
4. `tools/send_gmail.py` — sends via smtp.gmail.com:587 with STARTTLS (only runs after `y` approval)

Orchestrated by `tools/newsletter_run.py`.

## Brand Design
- **Header**: `#009C3B` green background, white title, optional logo image
- **Accent bar**: `#FFDF00` gold, 6px, separates header from body
- **Bullet points**: gold left-border (`#FFDF00`) divs, no plain `<ul>`
- **Section heading**: `#009C3B` green
- **Footer**: `#002776` blue background, white text
- **Body background**: `#f0f4f0` light green tint

## Run Command
```powershell
cd c:\Users\cemer\newsletter-demo
python tools/newsletter_run.py `
  --topic "Your Topic Here" `
  --to "recipient@example.com" `
  --from "cemery65@gmail.com" `
  --logo "https://your-logo-url.com/logo.png"
```

## Expected Output
```
[1/3] Fetching research for: <topic>
[2/3] Generating newsletter...
      Subject: <topic>: Everything You Need to Know
      Draft saved to: ...\.tmp\newsletter_draft.html
      Open it in a browser to review before sending.

Send this newsletter? [y/N]: y
[3/3] Sending to <recipient>...
Email sent to <recipient>
Done.
```

If you type anything other than `y`, the run aborts and the draft is preserved in `.tmp/newsletter_draft.html` for the next attempt.

## Edge Cases
- **No logo**: omit `--logo` — header renders cleanly without the image tag
- **Rate limits**: Perplexity `sonar` model has a 30s timeout; if it fails, retry once before checking quota
- **Gmail auth failure**: ensure `GMAIL_SMTP_PASSWORD` is an App Password (Google Account > Security > 2-Step Verification > App passwords), not the account password
- **Bullet parsing**: if Perplexity returns numbered lists, the parser handles both `- item` and `1. item` formats
