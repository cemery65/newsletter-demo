import re
import sys
import textwrap


def _parse_bullet_points(text: str) -> list[str]:
    lines = text.splitlines()
    bullets = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^[-*•]\s+", stripped):
            bullets.append(re.sub(r"^[-*•]\s+", "", stripped))
        elif re.match(r"^\d+\.\s+", stripped):
            bullets.append(re.sub(r"^\d+\.\s+", "", stripped))
    return bullets


def _extract_overview(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        if not re.match(r"^[-*•\d]", line) and len(line) > 40:
            return line
    return lines[0] if lines else ""


def generate_newsletter(topic: str, research: str, logo_url: str = "") -> dict:
    subject = f"{topic}: Everything You Need to Know"

    overview = _extract_overview(research)
    bullets = _parse_bullet_points(research)

    logo_html = (
        f'<img src="{logo_url}" alt="Logo" '
        f'style="max-height:80px;margin-bottom:16px;border-radius:6px;display:block;margin-left:auto;margin-right:auto;">\n                      '
        if logo_url else ""
    )

    bullet_items = "\n".join(
        f'                      <div style="border-left:4px solid #FFDF00;padding-left:12px;margin-bottom:10px;color:#333333;font-size:15px;line-height:1.7;">{b}</div>'
        for b in bullets
    ) or (
        f'                      <div style="border-left:4px solid #FFDF00;padding-left:12px;margin-bottom:10px;color:#333333;font-size:15px;line-height:1.7;">{overview}</div>'
    )

    html_body = textwrap.dedent(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>{subject}</title>
        </head>
        <body style="margin:0;padding:0;background-color:#f0f4f0;font-family:Arial,sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0f4f0;padding:40px 0;">
            <tr>
              <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.10);">

                  <!-- Header -->
                  <tr>
                    <td style="background-color:#009C3B;padding:32px 40px;text-align:center;">
                      {logo_html}<h1 style="margin:0;color:#ffffff;font-size:26px;font-weight:700;letter-spacing:-0.5px;">
                        {topic}
                      </h1>
                    </td>
                  </tr>

                  <!-- Gold accent bar -->
                  <tr>
                    <td style="background-color:#FFDF00;height:6px;font-size:0;line-height:0;">&nbsp;</td>
                  </tr>

                  <!-- Body -->
                  <tr>
                    <td style="padding:36px 40px;">
                      <p style="margin:0 0 24px;color:#333333;font-size:16px;line-height:1.7;">
                        {overview}
                      </p>

                      <h2 style="margin:0 0 16px;color:#009C3B;font-size:18px;font-weight:700;">
                        Key Highlights
                      </h2>
{bullet_items}
                    </td>
                  </tr>

                  <!-- Footer -->
                  <tr>
                    <td style="background-color:#002776;padding:20px 40px;text-align:center;">
                      <p style="margin:0;color:#ffffff;font-size:12px;">
                        You're receiving this because you subscribed to our newsletter.
                      </p>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
    """).strip()

    return {"subject": subject, "html_body": html_body}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_newsletter.py <topic> <research_text>")
        sys.exit(1)
    topic = sys.argv[1]
    research = sys.argv[2]
    result = generate_newsletter(topic, research)
    print("Subject:", result["subject"])
    print("\n--- HTML ---\n")
    print(result["html_body"])
