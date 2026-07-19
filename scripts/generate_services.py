#!/usr/bin/env python3
"""Genera las páginas estáticas de servicios de MarketinAI."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "public"
SERVICIOS_DIR = BASE_DIR / "servicios"

NAV = """
<nav class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo">Marketin<span>AI</span></a>
    <button class="nav-toggle" aria-label="Menú" onclick="document.querySelector('.nav-links').classList.toggle('open')">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
    </button>
    <div class="nav-links">
      <a href="/">Inicio</a>
      <a href="/servicios/">Servicios</a>
      <a href="/pricing/">Precios</a>
      <a href="/contact/">Contacto</a>
      <a href="/" class="nav-cta">Kit IA — €397</a>
    </div>
  </div>
</nav>
""".strip()

FOOTER = """
<footer>
  <div class="container">
    <p>
      © 2026 MarketinAI · <a href="mailto:hola@marketinai.net">hola@marketinai.net</a>
      · <a href="/privacidad/">Privacidad</a> · <a href="/terminos/">Términos</a>
    </p>
  </div>
</footer>
""".strip()

HEAD_COMMON = """
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/servicios/style.css" />
<link rel="canonical" href="{canonical}" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
""".strip()

SCRIPT_FAQ = """
<script>
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement;
      const isActive = item.classList.contains('active');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
      if (!isActive) item.classList.add('active');
    });
  });
</script>
""".strip()

SCRIPT_FORM = """
<script>
(function(){
  const form = document.getElementById('lead-form');
  if (!form) return;
  const status = document.getElementById('form-status');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Enviando...';
    status.className = 'form-status';
    status.textContent = '';

    const data = Object.fromEntries(new FormData(form).entries());
    data.service = form.dataset.service;
    data.source = 'marketinai.net' + window.location.pathname;
    data.ts = new Date().toISOString();
    data.extras = {};
    form.querySelectorAll('[data-extra]').forEach(el => {
      data.extras[el.name] = el.value;
    });
    data.consent_rgpd = !!data.consent_rgpd;
    data.consent_marketing = !!data.consent_marketing;

    try {
      const res = await fetch('/api/marketinai/lead-capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const json = await res.json().catch(() => ({}));
      if (res.ok || json.success || json.status === 'ok') {
        status.className = 'form-status success';
        status.textContent = 'Solicitud enviada. Te contactamos en menos de 24h.';
        form.reset();
        window.gtag && gtag('event', 'lead_enviado', { service: data.service });
      } else {
        throw new Error(json.message || 'Error al enviar');
      }
    } catch (err) {
      status.className = 'form-status error';
      status.textContent = 'No se pudo enviar automáticamente. Escríbenos a hola@marketinai.net o por Telegram y te atendemos enseguida.';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Enviar solicitud';
    }
  });
})();
</script>
""".strip()

GA4_SCRIPT = """
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-LG5S74BFF4"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-LG5S74BFF4');
</script>
""".strip()

SERVICES = {
    "auditoria-express": {
        "title": "Auditoría Web Express en 24h — 99€ | MarketinAI",
        "description": "Auditoría web profesional con evidencia real: velocidad, SEO, UX, móvil y formularios. Informe accionable en 24h con prioridades P0/P1/P2. 99€, precio cerrado.",
        "h1": "Auditoría Express: descubre en 24h qué le cuesta clientes a tu web",
        "subtitle": "Radiografía completa de tu web con navegador real y métricas objetivas. No es un PDF genérico de PageSpeed: es un informe accionable con capturas de TU web, prioridades claras y el impacto estimado de cada problema.",
        "price": "99€",
        "price_note": "pago único · sin IVA",
        "sku": "MKAI-AE-99",
        "stripe_link": "https://buy.stripe.com/fZu14of9OcF7goN7DldfG05",
        "includes": [
            "Análisis de velocidad y rendimiento (tiempos de carga reales, móvil y escritorio)",
            "Revisión SEO técnica: indexación, títulos, metas, estructura de encabezados, errores 404",
            "Auditoría UX y conversión: recorrido del visitante, claridad del mensaje, llamadas a la acción",
            "Test de formularios y puntos de contacto (verificamos que realmente funcionan)",
            "Informe PDF profesional de 10-15 páginas con capturas, métricas y prioridades P0/P1/P2",
        ],
        "differentiation": [
            "Las agencias te dan recomendaciones vagas; nosotros te damos <strong>la solución concreta de cada hallazgo</strong>, lista para aplicar",
            "Cada problema viene con <strong>captura real de tu web</strong>, no con teoría",
            "Priorizamos por <strong>impacto en ingresos</strong>, no por checklist técnico",
            "Si contratas el Fix 48h después, <strong>los 99€ se descuentan íntegros</strong>",
            "Garantía: si no encontramos al menos 5 problemas accionables, <strong>te devolvemos el dinero</strong>",
        ],
        "faq": [
            ("¿Cuándo recibo el informe?", "En 24h laborables desde que nos facilitas la URL de tu web."),
            ("¿Necesitas acceso a mi web?", "No. La auditoría se hace desde fuera, como la vería cualquier cliente (y Google)."),
            ("¿Y si mi web está bien?", "Entonces te lo decimos con datos, te devolvemos el importe si no hay 5 hallazgos accionables, y te vas con la tranquilidad gratis."),
            ("¿El informe lo entenderé si no soy técnico?", "Sí. Cada hallazgo tiene explicación en lenguaje de negocio + detalle técnico para tu desarrollador."),
            ("¿Puedo aplicar yo mismo las correcciones?", "Sí, el informe incluye cómo. Si prefieres que lo hagamos nosotros, existe la Auditoría + Fix 48h (y te descontamos los 99€)."),
        ],
        "cta": "Comprar Auditoría Express — 99€",
        "cta_secondary": "Ver un informe de ejemplo",
        "fields": [
            ("web", "url", True, "URL de tu web", "https://www.tuempresa.es"),
        ],
    },
    "auditoria-fix-48h": {
        "title": "Auditoría Web + Reparación en 48h — 399€ | MarketinAI",
        "description": "Diagnóstico y reparación de tu web en un solo producto. Corregimos los problemas críticos en 48h y te entregamos la comparativa antes/después. 399€ cerrados.",
        "h1": "Auditoría + Fix 48h: diagnosticamos y reparamos. Tú solo ves el antes y el después",
        "subtitle": "El único producto del mercado que no se queda en el diagnóstico. Auditamos tu web, corregimos los problemas críticos en 48 horas y te entregamos la comparativa medible del antes y el después.",
        "price": "399€",
        "price_note": "pago único · sin IVA",
        "sku": "MKAI-AF-399",
        "stripe_link": "https://buy.stripe.com/dRm00ke5KbB3b4tcXFdfG06",
        "includes": [
            "Todo lo de la Auditoría Express (informe completo con prioridades)",
            "Corrección implementada de los 5-10 hallazgos críticos: rendimiento, SEO on-page, formularios rotos, errores de maquetación móvil",
            "Optimización de velocidad de carga de las páginas principales",
            "Re-auditoría comparativa: informe 'antes/después' con métricas",
            "7 días de soporte post-reparación por email",
        ],
        "differentiation": [
            "Las agencias facturan diagnóstico y reparación por separado (800-2.000€); aquí es <strong>un solo producto a precio cerrado</strong>",
            "Plazo cerrado: <strong>48h laborables</strong> desde el acceso. Si no llegamos, trabajamos gratis hasta terminar",
            "No te pedimos fe: te entregamos <strong>mediciones del antes y el después</strong>",
            "Sin reuniones infinitas: un formulario, un acceso, un resultado",
        ],
        "faq": [
            ("¿Qué necesitas de mí?", "Acceso al panel de tu web (WordPress, Shopify, etc.) o al hosting. Te decimos exactamente qué permisos mínimos hacen falta. Nunca pedimos contraseñas por formulario web: lo acordamos por email tras la compra."),
            ("¿Qué pasa si mi web necesita más de lo que cubre?", "Te lo decimos antes de tocar nada, con presupuesto cerrado para el extra. Tú decides. El Fix nunca se infla por sorpresa."),
            ("¿Y si no puedes arreglar algo?", "Se te informa en el diagnóstico inicial y se descuenta del alcance o se presupuesta aparte. Transparencia total."),
            ("¿Hacéis cambios de diseño o redacción?", "El Fix cubre problemas técnicos y de conversión. Rediseños y copy nuevo son servicios aparte (ver Plan Crecimiento)."),
            ("¿Y si ya compré la Auditoría Express?", "Te descontamos los 99€ íntegros con el cupón que recibiste con tu informe."),
        ],
        "cta": "Pedir Auditoría + Fix — 399€",
        "cta_secondary": "Empezar solo con la Auditoría Express (99€)",
        "fields": [
            ("web", "url", True, "URL de tu web", "https://www.tuempresa.es"),
            ("cms", "select", True, "¿En qué está hecha tu web?", None),
        ],
        "extras": [
            ("cms", ["WordPress", "Shopify", "Wix", "PrestaShop", "A medida", "No lo sé"]),
        ],
    },
    "plan-crecimiento": {
        "title": "Plan Crecimiento Web — 199€/mes sin permanencia | MarketinAI",
        "description": "Tu web monitorizada y mejorando cada mes: vigilancia 24/7, mini-mejoras continuas e informe mensual con resultados. Sin permanencia.",
        "h1": "Plan Crecimiento: tu web mejorando cada mes mientras tú atiendes tu negocio",
        "subtitle": "Las webs se degradan solas: se rompen formularios, cae la velocidad, Google cambia las reglas. Con el Plan Crecimiento tu web está vigilada y mejorando de forma continua, y tú recibes un informe mensual que entiendes.",
        "price": "199€/mes",
        "price_note": "sin permanencia · sin IVA",
        "sku": "MKAI-PC-199",
        "stripe_link": "https://buy.stripe.com/bJedRaaTycF71tTe1JdfG07",
        "includes": [
            "Monitorización continua: caídas, velocidad y formularios (te avisamos antes de que lo note un cliente)",
            "2 mini-mejoras implementadas al mes (ajustes de conversión, SEO, contenido menor, correcciones)",
            "Informe mensual en español claro: qué se hizo, qué mejoró, qué recomendamos",
            "Re-auditoría trimestral completa incluida",
            "Soporte prioritario por email y WhatsApp",
            "Sin permanencia: cancela cuando quieras",
        ],
        "differentiation": [
            "El mantenimiento típico es 'actualizar plugins y rezar'; nosotros hacemos <strong>mejoras orientadas a conversión</strong> cada mes",
            "<strong>Monitorización proactiva</strong>: detectamos el problema antes de que te llame un cliente cabreado",
            "Informe mensual <strong>en lenguaje de negocio</strong>: horas, leads y euros, no jerga técnica",
            "Precio cerrado y sin permanencia. Las agencias te atan 12 meses; nosotros te retenemos con resultados",
        ],
        "faq": [
            ("¿Qué son exactamente las 'mini-mejoras'?", "Ajustes de hasta ~2h de trabajo: mejorar un formulario, optimizar una página lenta, corregir SEO on-page, actualizar una sección. Si necesitas algo mayor, te presupuestamos aparte con descuento de cliente."),
            ("¿Hay permanencia?", "No. Cancelas con un email y el servicio termina a fin de mes."),
            ("¿Necesito haber contratado el Fix 48h antes?", "No es obligatorio, pero es lo recomendable: el Plan rinde mucho mejor sobre una web ya sana."),
            ("¿Incluye crear contenido nuevo (blog, redes)?", "No. Para contenido continuo está el Pack Presencia Local o el SaaS de MarketinAI, y combinamos con descuento."),
            ("¿Cómo sé que estoy recuperando los 199€?", "El informe mensual muestra métricas de antes/después: velocidad, visibilidad y leads. Si en 3 meses no ves mejora medible, te lo diremos nosotros mismos y te recomendaremos cancelar."),
        ],
        "cta": "Empezar Plan Crecimiento — 199€/mes",
        "cta_secondary": "Háblanos por WhatsApp y te contamos si te encaja",
        "fields": [
            ("web", "url", True, "URL de tu web", "https://www.tuempresa.es"),
        ],
    },
    "presencia-local": {
        "title": "Pack Presencia Local para PYMEs — 199€ + 99€/mes | MarketinAI",
        "description": "Google Business Profile optimizado, landing de captación y contenido mensual para tu negocio local. Que te encuentren cuando buscan cerca de ti.",
        "h1": "Pack Presencia Local: que te encuentren los clientes que ya te están buscando cerca",
        "subtitle": "El 46% de las búsquedas en Google tienen intención local. Si tu negocio no aparece ahí con buena pinta, esos clientes se van al competidor de al lado. Montamos tu presencia local completa y la mantenemos viva cada mes.",
        "price": "199€ + 99€/mes",
        "price_note": "setup + mensualidad · sin permanencia · sin IVA",
        "sku": "MKAI-PL-SETUP",
        "stripe_link": "https://buy.stripe.com/bJebJ23r634x4G5e1JdfG08",
        "includes_setup": [
            "Google Business Profile creado u optimizado: categorías, descripción, fotos, horarios, atributos",
            "Landing page de captación local (diseño + copy + formulario) conectada a tu email/WhatsApp",
            "Configuración de reseñas: enlace directo para pedirlas + plantillas de respuesta",
            "Alta y coherencia de datos (nombre, dirección, teléfono) en los principales directorios",
        ],
        "includes_monthly": [
            "8-12 piezas de contenido visual al mes para Google Business Profile y tus redes (imágenes generadas con IA, adaptadas a tu marca)",
            "Gestión de reseñas: respuesta profesional a las nuevas, alerta inmediata si llega una negativa",
            "Informe mensual: búsquedas, llamadas, solicitudes de direcciones, visitas a la landing",
            "Ajustes continuos de la landing y del perfil",
        ],
        "differentiation": [
            "No publicamos por publicar: todo el contenido apunta a <strong>llamadas, direcciones y mensajes</strong>",
            "Precio de PYME real: una agencia local cobra 300-600€/mes por menos de la mitad",
            "El contenido se produce con IA supervisada: <strong>más volumen, más barato, misma calidad</strong>",
            "Sin permanencia. Si no ves movimiento en el informe mensual, te vas y ya",
        ],
        "faq": [
            ("¿Sirve si no tengo local físico?", "Sí, si tu negocio atiende una zona (fontaneros, abogados, clínicas...). Google Business Profile admite negocios de área de servicio."),
            ("¿Necesito web?", "No. La landing de captación incluida funciona como tu web de captación. Si ya tienes web, la conectamos."),
            ("¿Quién hace las fotos del contenido?", "Partimos de tu material si lo tienes y lo completamos con imágenes generadas con IA adaptadas a tu marca. Nunca fotos de stock genéricas con marca de agua."),
            ("¿Las reseñas negativas se pueden borrar?", "No, y desconfía de quien prometa eso. Lo que sí hacemos: responderlas de forma profesional y rápida, y activar un flujo para conseguir más reseñas positivas reales que las diluyan."),
            ("¿Cuándo se ven resultados?", "Los perfiles locales suelen mostrar movimiento en 4-8 semanas. El informe mensual te lo mostrará con datos."),
        ],
        "cta": "Activar mi Presencia Local — 199€",
        "cta_secondary": "Solicitar diagnóstico gratuito de mi ficha de Google",
        "fields": [
            ("direccion_negocio", "text", True, "Dirección o zona de servicio", "Calle Mayor 12, Madrid o atiendo zona norte de Madrid"),
            ("tiene_gbp", "radio", True, "¿Tienes ficha de Google?", None),
        ],
        "extras": [
            ("tiene_gbp", ["Sí, tengo ficha de Google", "No / No lo sé"]),
        ],
    },
    "automatizacion": {
        "title": "Automatización de Procesos a Medida — desde 500€ | MarketinAI",
        "description": "Automatizamos captación, seguimiento y comunicación con clientes: formularios, WhatsApp, email y CRM trabajando solos. Propuesta cerrada en 48h.",
        "h1": "Automatización a Medida: procesos que venden y responden mientras duermes",
        "subtitle": "Cada lead que espera 1 hora respuesta vale la mitad. Automatizamos el proceso exacto que hoy te roba horas: captación, respuesta inmediata por WhatsApp/email, seguimiento y recordatorios. Propuesta cerrada en 48h, sin compromiso.",
        "price": "desde 500€",
        "price_note": "presupuesto cerrado · sin IVA",
        "sku": "MKAI-AUTO",
        "stripe_link": "https://buy.stripe.com/fZu4gA0eUfRj2xXbTBdfG0a",
        "includes": [
            "Captación automática: formulario → WhatsApp/email de bienvenida inmediato → aviso a tu equipo",
            "Secuencias de seguimiento de leads que no responden (3-5 toques automáticos)",
            "Recordatorios de citas y presupuestos pendientes",
            "Sincronización entre tus herramientas (web, email, WhatsApp, hojas de cálculo, CRM)",
            "Todo montado sobre la plataforma MarketinAI: lo ves funcionando y controlas desde un solo panel",
        ],
        "differentiation": [
            "No cobramos por horas ni por 'consultoría': <strong>precio cerrado por proyecto</strong>, conocido antes de empezar",
            "Trabajamos sobre <strong>nuestra propia plataforma probada con PYMEs españolas</strong>, no sobre experimentos",
            "Entregamos documentación y te formamos: <strong>la automatización es tuya</strong>, no dependes de nosotros",
            "Si el proceso crece, escala dentro de la misma plataforma (desde 99€/mes) sin rehacer nada",
        ],
        "faq": [
            ("¿Cuánto cuesta?", "Proyectos desde 500€. Tras el formulario te enviamos propuesta cerrada en 48h: alcance, precio y plazo. Sin sorpresas."),
            ("¿Cuánto tarda?", "Automatizaciones típicas: 1-2 semanas desde el visto bueno."),
            ("¿Necesito cambiar mis herramientas?", "Normalmente no. Conectamos lo que ya usas (WhatsApp Business, tu email, tu web, tu hoja de cálculo)."),
            ("¿Y si después quiero cambiar algo?", "El primer mes de ajustes menores está incluido. Después, cambios puntuales presupuestados o dentro del Plan Crecimiento."),
            ("¿Puedo ver una demo antes de pagar?", "Sí. En la propuesta te incluimos un vídeo de una automatización real equivalente funcionando."),
        ],
        "cta": "Solicitar Propuesta — respuesta en 48h",
        "cta_secondary": "Ver la plataforma MarketinAI (prueba 14 días gratis)",
        "fields": [
            ("proceso", "textarea", True, "Describe el proceso que te roba más horas", "Recibo leads por formulario, los paso a WhatsApp manualmente, y muchos se me olvidan seguir..."),
            ("presupuesto", "select", True, "Presupuesto orientativo", None),
        ],
        "extras": [
            ("presupuesto", ["500-1.000€", "1.000-2.500€", "Más de 2.500€", "Necesito orientación"]),
        ],
    },
}


def build_head(title, description, canonical, og_image="https://marketinai.net/og-image.png"):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  {HEAD_COMMON.format(canonical=canonical)}
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  {GA4_SCRIPT}
</head>
"""


def build_footer():
    return FOOTER


def build_nav():
    return NAV


def build_faq(faq_items):
    if not faq_items:
        return ""
    items = "\n".join([
        f"""<div class="faq-item">
          <div class="faq-q">{q}<span class="toggle">+</span></div>
          <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
        </div>"""
        for q, a in faq_items
    ])
    return f"""
    <section class="section">
      <div class="container">
        <h2 class="section-title">Preguntas frecuentes</h2>
        <div class="faq-list">
          {items}
        </div>
      </div>
    </section>
    """


def build_list(title, items, icon="✓"):
    lis = "\n".join([f'<li>{i}</li>' for i in items])
    return f"""
    <div class="block">
      <h2><span class="icon">{icon}</span>{title}</h2>
      <ul>
        {lis}
      </ul>
    </div>
    """


def build_form(service_id, service, is_automation=False):
    fields = [
        ("nombre", "text", True, "Nombre", "María García"),
        ("email", "email", True, "Email", "maria@empresa.es"),
        ("telefono", "tel", service_id != "auditoria-express", "Teléfono", "+34 600 111 222"),
        ("empresa", "text", False, "Empresa", "Empresa SL"),
        ("web", "url", service_id not in ("presencia-local", "automatizacion"), "Web", "https://www.tuempresa.es"),
        ("vertical", "select", False, "Sector", None),
        ("mensaje", "textarea", False, "Mensaje opcional", "Cuéntanos más sobre tu proyecto..."),
    ]

    field_html = ""
    for name, ftype, required, label, placeholder in fields:
        # Skip web if not required and not automation/presencia-local optional
        if name == "web" and service_id == "automatizacion":
            continue
        if name == "telefono" and service_id == "auditoria-express":
            continue

        req_attr = ' required' if required else ''
        req_star = '<span class="req">*</span>' if required else ''
        ph = f' placeholder="{placeholder}"' if placeholder else ''

        if ftype == "select" and name == "vertical":
            options = ["Legal/Abogacía", "Inmobiliaria", "Salud/Clínica", "Hostelería", "Comercio local", "Servicios profesionales", "Industria", "Otro"]
            opts = "\n".join([f'<option value="{o}">{o}</option>' for o in options])
            field_html += f"""
            <div class="form-group">
              <label for="vertical">{label}{req_star}</label>
              <select id="vertical" name="vertical"{req_attr}>
                <option value="">Selecciona tu sector</option>
                {opts}
              </select>
            </div>
            """
        elif ftype == "textarea":
            field_html += f"""
            <div class="form-group">
              <label for="{name}">{label}{req_star}</label>
              <textarea id="{name}" name="{name}"{ph}{req_attr}></textarea>
            </div>
            """
        elif ftype == "radio":
            # handled via extras
            pass
        else:
            field_html += f"""
            <div class="form-group">
              <label for="{name}">{label}{req_star}</label>
              <input type="{ftype}" id="{name}" name="{name}"{ph}{req_attr} />
            </div>
            """

    # Service-specific extras
    extras = service.get("extras", [])
    for extra_name, options in extras:
        if extra_name == "cms":
            opts = "\n".join([f'<option value="{o}">{o}</option>' for o in options])
            field_html += f"""
            <div class="form-group">
              <label for="cms">¿En qué está hecha tu web?<span class="req">*</span></label>
              <select id="cms" name="cms" data-extra="cms" required>
                <option value="">Selecciona una opción</option>
                {opts}
              </select>
              <p class="hint">Nunca pedimos contraseñas por formulario. Los accesos se acuerdan por email tras la compra.</p>
            </div>
            """
        elif extra_name == "tiene_gbp":
            radios = "\n".join([f'<label style="display:flex;align-items:center;gap:8px;font-weight:500;color:var(--text2);"><input type="radio" name="tiene_gbp" value="{o}" data-extra="tiene_gbp" required style="width:auto;">{o}</label>' for o in options])
            field_html += f"""
            <div class="form-group">
              <label>¿Tienes ficha de Google?<span class="req">*</span></label>
              <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px;">
                {radios}
              </div>
            </div>
            """
        elif extra_name == "presupuesto":
            opts = "\n".join([f'<option value="{o}">{o}</option>' for o in options])
            field_html += f"""
            <div class="form-group">
              <label for="presupuesto">Presupuesto orientativo<span class="req">*</span></label>
              <select id="presupuesto" name="presupuesto" data-extra="presupuesto" required>
                <option value="">Selecciona un rango</option>
                {opts}
              </select>
            </div>
            """

    # RGPD consent
    rgpd_text = """☑ He leído y acepto la <a href="/privacidad/">Política de Privacidad</a>. Consiento que <strong>MarketinAI</strong> trate mis datos para gestionar mi solicitud, prestar el servicio contratado y comunicarme lo necesario para su ejecución. Puedo ejercer mis derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <strong>hola@marketinai.net</strong>."""

    return f"""
    <section class="section" id="formulario">
      <div class="container">
        <div class="form-block">
          <h2>Solicita tu {service['h1'].split(':')[0]}</h2>
          <p class="subtitle">Rellena el formulario y te contactamos en menos de 24h para confirmar el alcance y el pago.</p>
          <form id="lead-form" data-service="{service['sku']}">
            {field_html}
            <div class="checkbox">
              <input type="checkbox" id="consent_rgpd" name="consent_rgpd" required />
              <label for="consent_rgpd">{rgpd_text}</label>
            </div>
            <div class="checkbox">
              <input type="checkbox" id="consent_marketing" name="consent_marketing" />
              <label for="consent_marketing">Quiero recibir consejos de marketing digital y ofertas de MarketinAI. Puedo darme de baja en cualquier momento con un clic.</label>
            </div>
            <button type="submit" class="btn-submit">{service['cta']}</button>
            <p class="small mt-2">Responsable: MarketinAI. Finalidad: gestión de tu solicitud y prestación del servicio. No cedemos datos a terceros salvo obligación legal.</p>
          </form>
          <div id="form-status" class="form-status"></div>
        </div>
      </div>
    </section>
    """


def build_service_page(sid, service):
    canonical = f"https://marketinai.net/servicios/{sid}/"
    head = build_head(service["title"], service["description"], canonical)

    if sid == "presencia-local":
        includes = build_list("Lo que incluye (setup, 199€)", service["includes_setup"], "✓")
        includes += build_list("Lo que incluye (99€/mes)", service["includes_monthly"], "✓")
    else:
        includes = build_list("Lo que incluye", service["includes"], "✓")
    diff = build_list("Por qué no es 'otra agencia'", service["differentiation"], "★")
    faq = build_faq(service["faq"])
    form = build_form(sid, service)

    cta_primary = f'<a href="#formulario" class="btn-primary">{service["cta"]}</a>'
    if service.get("stripe_link"):
        cta_primary = f'<a href="{service["stripe_link"]}" target="_blank" rel="noopener noreferrer" class="btn-primary">{service["cta"]}</a>'
    cta_secondary = ""
    if sid == "auditoria-express":
        cta_secondary = '<a href="/downloads/guia-7-errores.pdf" class="btn-secondary">Ver un informe de ejemplo</a>'
    elif sid == "auditoria-fix-48h":
        cta_secondary = '<a href="/servicios/auditoria-express/" class="btn-secondary">Empezar solo con la Auditoría Express (99€)</a>'
    elif sid == "plan-crecimiento":
        cta_secondary = '<a href="https://t.me/MarketinAIBot" target="_blank" rel="noopener" class="btn-secondary">Háblanos por WhatsApp</a>'
    elif sid == "presencia-local":
        cta_secondary = '<a href="#formulario" class="btn-secondary">Solicitar diagnóstico gratuito de mi ficha de Google</a>'
    elif sid == "automatizacion":
        cta_secondary = '<a href="/" class="btn-secondary">Ver la plataforma MarketinAI</a>'

    return f"""{head}
<body>
  {build_nav()}

  <header class="page-header">
    <div class="container">
      <h1>{service['h1']}</h1>
      <p class="subtitle">{service['subtitle']}</p>
      <div class="price-tag">
        <span class="amount">{service['price']}</span>
        <span class="period">{service['price_note']}</span>
      </div>
      <div class="mt-3">
        {cta_primary}
        {cta_secondary}
      </div>
    </div>
  </header>

  <section class="section" style="padding-top:0;">
    <div class="container content-block">
      {includes}
      {diff}
    </div>
  </section>

  <div class="guarantee-box">
    <h3>Garantía MarketinAI</h3>
    <p>{"Si la Auditoría Express no detecta al menos 5 problemas accionables, te devolvemos el importe. Sin letra pequeña." if sid == "auditoria-express" else "Sin permanencia. Cancela cuando quieras. Si no ves resultados medibles en el primer mes, te lo decimos nosotros."}</p>
  </div>

  {faq}
  {form}

  {build_footer()}
  {SCRIPT_FAQ}
  {SCRIPT_FORM}
</body>
</html>
"""


def build_hub_page():
    canonical = "https://marketinai.net/servicios/"
    head = build_head(
        "Servicios MarketinAI — Auditoría web, reparación y automatización para PYMEs",
        "Diagnóstico, reparación y mejora continua de tu presencia digital. Precios cerrados, plazos cerrados, resultados medibles. Servicios para PYMEs españolas.",
        canonical,
    )

    cards = []
    for sid, s in SERVICES.items():
        cards.append(f"""
        <a href="/servicios/{sid}/" class="service-card">
          <span class="badge">{s['price']}</span>
          <h2>{s['h1'].split(':')[0]}</h2>
          <p class="desc">{s['subtitle'].split('.')[0]}.</p>
          <p class="price">{s['price']} <span>{s['price_note']}</span></p>
          <span class="cta">Ver servicio →</span>
        </a>
        """)

    return f"""{head}
<body>
  {build_nav()}

  <header class="hero-servicios">
    <div class="container">
      <h1>Servicios que arreglan tu marketing <span>esta semana</span>, no el mes que viene</h1>
      <p class="subtitle">Diagnóstico, reparación y mejora continua de tu presencia digital. Precios cerrados, plazos cerrados, resultados medibles. Sin humo de agencia.</p>
      <p class="support">Todos los servicios incluyen informe con evidencia real: capturas, métricas y comparativa antes/después.</p>
    </div>
  </header>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="services-grid">
        {''.join(cards)}
      </div>
    </div>
  </section>

  <div class="guarantee-box">
    <h3>Garantía MarketinAI</h3>
    <p>Todos los servicios tienen garantía de resultado o te devolvemos el dinero. Sin permanencia en los planes mensuales. Sin letra pequeña.</p>
  </div>

  <section class="cta-section">
    <div class="container">
      <h2>¿No sabes por dónde empezar?</h2>
      <p>La Auditoría Express es la prueba de fuego: en 24h sabes exactamente qué le cuesta clientes a tu web y cómo arreglarlo.</p>
      <a href="/servicios/auditoria-express/" class="btn-primary">Empezar con la Auditoría Express — 99€</a>
    </div>
  </section>

  {build_footer()}
</body>
</html>
"""


def build_gracias_page():
    canonical = "https://marketinai.net/gracias/"
    head = build_head(
        "Gracias por tu compra — MarketinAI",
        "Completa los datos de tu proyecto para que podamos empezar a trabajar en tu servicio contratado.",
        canonical,
    )
    return f"""{head}
<body>
  {build_nav()}

  <header class="page-header">
    <div class="container">
      <h1>¡Gracias! Solo un paso más para empezar</h1>
      <p class="subtitle">Completa los datos de tu proyecto. Así vinculamos tu pago con el equipo que ejecutará el servicio.</p>
    </div>
  </header>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <div class="form-block">
        <form id="lead-form" data-service="GRACIAS">
          <div class="form-group">
            <label for="nombre">Nombre<span class="req">*</span></label>
            <input type="text" id="nombre" name="nombre" required />
          </div>
          <div class="form-group">
            <label for="email">Email<span class="req">*</span></label>
            <input type="email" id="email" name="email" required />
          </div>
          <div class="form-group">
            <label for="telefono">Teléfono</label>
            <input type="tel" id="telefono" name="telefono" />
          </div>
          <div class="form-group">
            <label for="empresa">Empresa</label>
            <input type="text" id="empresa" name="empresa" />
          </div>
          <div class="form-group">
            <label for="web">URL de tu web<span class="req">*</span></label>
            <input type="url" id="web" name="web" required />
          </div>
          <div class="form-group">
            <label for="servicio">Servicio contratado</label>
            <select id="servicio" name="servicio">
              <option value="MKAI-AE-99">Auditoría Express — 99€</option>
              <option value="MKAI-AF-399">Auditoría + Fix 48h — 399€</option>
              <option value="MKAI-PC-199">Plan Crecimiento — 199€/mes</option>
              <option value="MKAI-PL-SETUP">Pack Presencia Local — 199€ setup</option>
              <option value="MKAI-AUTO">Automatización a Medida</option>
            </select>
          </div>
          <div class="form-group">
            <label for="mensaje">Mensaje adicional</label>
            <textarea id="mensaje" name="mensaje" placeholder="Cuéntanos lo que necesites..."></textarea>
          </div>
          <div class="checkbox">
            <input type="checkbox" id="consent_rgpd" name="consent_rgpd" required />
            <label for="consent_rgpd">☑ He leído y acepto la <a href="/privacidad/">Política de Privacidad</a>. Consiento que <strong>MarketinAI</strong> trate mis datos para gestionar mi solicitud y prestar el servicio contratado.</label>
          </div>
          <button type="submit" class="btn-submit">Enviar datos del proyecto</button>
        </form>
        <div id="form-status" class="form-status"></div>
      </div>
    </div>
  </section>

  {build_footer()}
  {SCRIPT_FORM}
</body>
</html>
"""


def main():
    SERVICIOS_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "gracias").mkdir(parents=True, exist_ok=True)

    # Hub
    (SERVICIOS_DIR / "index.html").write_text(build_hub_page(), encoding="utf-8")

    # Service pages
    for sid, service in SERVICES.items():
        page_dir = SERVICIOS_DIR / sid
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(build_service_page(sid, service), encoding="utf-8")

    # Gracias
    (BASE_DIR / "gracias" / "index.html").write_text(build_gracias_page(), encoding="utf-8")

    print(f"Generated pages in {SERVICIOS_DIR}")


if __name__ == "__main__":
    main()
