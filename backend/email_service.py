"""Email service for MarketinAI backend."""
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
LEAD_MAGNET_PDF = BASE_DIR.parent / "content" / "lead_magnets" / "auditoria_marketing_ia_10_puntos.pdf"
LEAD_MAGNET_URL = "https://marketinai.net/assets/lead_magnets/auditoria_marketing_ia_10_puntos.pdf"
EMAIL_TEMPLATES_DIR = BASE_DIR.parent / "content" / "emails" / "marketinai" / "lead_magnet_sequence"


def _load_template(filename: str, name: str, email: str) -> tuple[str, str]:
    """Load an email template and return (subject, body_text)."""
    path = EMAIL_TEMPLATES_DIR / filename
    if not path.exists():
        return "", ""

    content = path.read_text(encoding="utf-8")
    # Parse front matter
    lines = content.split("\n")
    meta = {}
    body_lines = []
    in_meta = False
    meta_done = False

    for line in lines:
        if line.strip() == "---":
            if not in_meta:
                in_meta = True
                continue
            else:
                in_meta = False
                meta_done = True
                continue
        if in_meta and ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
        elif meta_done:
            body_lines.append(line)

    subject = meta.get("subject", "MarketinAI")
    body = "\n".join(body_lines).strip()
    body = body.replace("{{lead.email}}", email)
    body = body.replace("{{lead.name}}", name or "")
    body = body.replace("{{lead.name|amigo}}", name or "amigo")
    return subject, body


def _markdown_to_html(text: str) -> str:
    """Naive markdown to HTML for email bodies."""
    import re
    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Lists
    lines = text.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("• ") or stripped.startswith("- ") or stripped.startswith("✅ "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if stripped:
                html_lines.append(f"<p>{line}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def send_email(
    to_email: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    attachment_path: Optional[Path] = None,
) -> bool:
    """Send an email via SMTP."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.hostinger.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER", "hola@marketinai.net")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)
    smtp_from_name = os.getenv("SMTP_FROM_NAME", "MarketinAI")

    if not smtp_pass:
        raise RuntimeError("SMTP_PASS not configured")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{smtp_from_name} <{smtp_from}>"
    msg["To"] = to_email

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    if attachment_path and attachment_path.exists():
        from email.mime.base import MIMEBase
        from email import encoders

        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_path.read_bytes())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=\"{attachment_path.name}\"",
        )
        msg.attach(part)

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg["From"], [to_email], msg.as_string())

    return True


def _get_lead_magnet_pdf() -> Path:
    """Return local PDF path, downloading from production if not present."""
    if LEAD_MAGNET_PDF.exists():
        return LEAD_MAGNET_PDF

    # Fallback: download from public URL (useful inside Docker container)
    import urllib.request
    import tempfile

    temp_dir = Path(tempfile.gettempdir()) / "marketinai"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / "auditoria_marketing_ia_10_puntos.pdf"

    urllib.request.urlretrieve(LEAD_MAGNET_URL, temp_path)
    return temp_path


DEFAULT_LEAD_MAGNET_SUBJECT = "Tu auditoría de Marketing IA está aquí"
DEFAULT_LEAD_MAGNET_BODY = """Hola {name},

Gracias por descargar la Auditoría de Marketing IA para PYMEs.

Adjunta encontrarás el PDF con los 10 puntos clave para saber si tu negocio está preparado para escalar con inteligencia artificial.

Cómo usarla en 3 pasos:

1. Reserva 15 minutos sin distracciones.
2. Responde los 10 puntos con honestidad.
3. Suma tu puntuación y lee la recomendación final.

Si tu puntuación está por debajo de 60, no te preocupes: la mayoría de las PYMEs empieza ahí. Lo importante es identificar los puntos de mayor impacto.

El punto que más ROI suele generar

En nuestra experiencia, automatizar la captación + email de bienvenida + nurturing es el punto que más clientes genera en las primeras 4 semanas.

¿Quieres ver cómo funciona en la práctica? Te invito a probar MarketinAI 14 días gratis:

👉 Ver demo interactiva: https://marketinai.net/demo

Sin tarjeta, sin permanencia.

Saludos,

Equipo MarketinAI
hola@marketinai.net
"""


def send_lead_magnet_welcome(name: Optional[str], email: str) -> bool:
    """Send the lead magnet welcome email with PDF attachment."""
    subject, body_text = _load_template("email_1_welcome.md", name or "", email)
    if not subject:
        subject = DEFAULT_LEAD_MAGNET_SUBJECT
        body_text = DEFAULT_LEAD_MAGNET_BODY.format(name=name or "amigo")

    body_html = _markdown_to_html(body_text)
    pdf_path = _get_lead_magnet_pdf()
    return send_email(
        to_email=email,
        subject=subject,
        body_text=body_text,
        body_html=body_html,
        attachment_path=pdf_path,
    )
