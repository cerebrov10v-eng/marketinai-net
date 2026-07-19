import { useState } from 'react'
import { Helmet } from 'react-helmet-async'

const STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/7sY3cw2DL4cec3t4LP0co02'
const STRIPE_PAYMENT_LINK_NORMAL = 'https://buy.stripe.com/5kQeVe2DL6km7Nd2DH0co03'

const KIT_ITEMS = [
  {
    n: '01',
    title: 'Cualificación de Leads con IA',
    desc: 'Flujo n8n que capta leads desde formularios o ads, los analiza con GPT-4 y los clasifica automáticamente. Solo hablas con los leads calientes.',
    tag: 'n8n + OpenAI',
  },
  {
    n: '02',
    title: 'Soporte 24/7 sin equipo humano',
    desc: 'Agente conversacional entrenado con tu base de conocimiento. Responde FAQs, gestiona incidencias y escala a humano solo cuando es necesario.',
    tag: 'n8n + Webhook + Telegram',
  },
  {
    n: '03',
    title: 'Email Marketing con IA',
    desc: 'Secuencia automática de emails generados con IA según el comportamiento del usuario. Onboarding, nurturing y ventas en piloto automático.',
    tag: 'n8n + SMTP + GPT-4',
  },
  {
    n: '04',
    title: 'Publicación Automática en RRSS',
    desc: 'Tu contenido de blog o producto se convierte en posts para LinkedIn, Instagram y Twitter/X automáticamente. Sin copiar, sin pegar.',
    tag: 'n8n + Social API',
  },
  {
    n: '05',
    title: 'Facturación e Informes Automáticos',
    desc: 'Genera facturas PDF, envía por email y alimenta tu hoja de resultados — todo sin tocar un solo archivo manualmente.',
    tag: 'n8n + PDF + Google Sheets',
  },
  {
    n: '06',
    title: 'Sesión 1-a-1 de Implementación',
    desc: '60 minutos contigo para configurar tu primer flujo en tu negocio real. No teoría — salimos con algo funcionando.',
    tag: '60 min live',
  },
]

const PAIN_ITEMS = [
  {
    title: 'Pierdes horas en tareas repetitivas',
    desc: 'Responder emails, clasificar leads, hacer informes, publicar en redes... todo consume tiempo que debería ir a crecer.',
  },
  {
    title: 'Contratar equipo sale muy caro',
    desc: 'Un community manager, un asistente, un comercial... Para un negocio mediano es inviable. La IA puede hacer el trabajo de tres.',
  },
  {
    title: 'Las herramientas de IA te abruman',
    desc: 'ChatGPT, Zapier, Make, n8n, agentes... Hay demasiadas opciones y no sabes por dónde empezar ni cómo conectarlo todo.',
  },
]

const PAIN_SVGS = [
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>,
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f87171" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
]

const FAQS = [
  {
    q: '¿Necesito saber programar?',
    a: 'No. n8n es visual — arrastras y conectas bloques. El Kit incluye los flujos ya montados. Solo los importas, configuras tus credenciales y funcionan.',
  },
  {
    q: '¿Funciona para mi tipo de negocio?',
    a: 'El Kit es genérico y se adapta a cualquier negocio digital: agencias, consultoras, tiendas online, infoproductores, SaaS, coaches... Si tienes clientes y procesos repetitivos, esto funciona para ti.',
  },
  {
    q: '¿Cuánto tiempo tarda en estar funcionando?',
    a: 'En 4 horas tienes el primer flujo activo. Con la sesión 1-a-1 incluida salimos con al menos uno corriendo en tu negocio real el mismo día.',
  },
  {
    q: '¿Qué pasa si tengo dudas después de comprar?',
    a: 'Tienes acceso a un canal privado de Telegram durante 30 días. Resuelvo dudas de implementación directamente.',
  },
  {
    q: '¿La garantía es real?',
    a: 'Sí. Si en 14 días no has automatizado al menos una tarea que te ahorre 2h/semana, te devuelvo el dinero sin preguntas.',
  },
]

export default function App() {
  const [openFaq, setOpenFaq] = useState(null)

  return (
    <>
      <Helmet>
        <title>MarketinAI — Automatiza tu negocio con IA en 4 horas</title>
        <meta name="description" content="Kit completo de automatización con IA para negocios hispanohablantes. 6 flujos n8n listos para usar + sesión 1-a-1. Precio de fundadores: €397." />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://marketinai.net/" />
        <meta property="og:title" content="MarketinAI — Automatiza tu negocio con IA en 4 horas" />
        <meta property="og:description" content="Cualificación de leads, soporte 24/7 y email marketing en piloto automático. Kit de fundadores: €397." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://marketinai.net/" />
        <meta property="og:image" content="https://marketinai.net/og-image.png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="MarketinAI — Automatiza tu negocio con IA en 4 horas" />
        <meta name="twitter:description" content="Kit completo: 6 flujos n8n listos para instalar + sesión 1-a-1. Precio de fundadores: €397." />
        <meta name="twitter:image" content="https://marketinai.net/og-image.png" />
        <script type="application/ld+json">{JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'Product',
          name: 'Kit MarketinAI — Automatización con IA',
          description: 'Kit completo de automatización con IA para negocios hispanohablantes: 6 flujos n8n listos para instalar + sesión 1-a-1. España, EEUU hispano y Latinoamérica.',
          brand: { '@type': 'Brand', name: 'MarketinAI' },
          url: 'https://marketinai.net/',
          offers: {
            '@type': 'Offer',
            price: '397',
            priceCurrency: 'EUR',
            availability: 'https://schema.org/LimitedAvailability',
            url: 'https://marketinai.net/',
            seller: { '@type': 'Organization', name: 'MarketinAI' },
          },
        })}</script>
        <script type="application/ld+json">{JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'WebSite',
          name: 'MarketinAI',
          url: 'https://marketinai.net/',
          description: 'Automatización con IA para negocios hispanohablantes. 6 flujos n8n + sesión 1-a-1.',
          inLanguage: 'es',
        })}</script>
      </Helmet>

      {/* NAV */}
      <nav>
        <div className="container nav-inner">
          <div className="nav-logo">Marketin<span>AI</span></div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <a href="mailto:hola@marketinai.net" style={{ color: 'var(--text2)', fontSize: '0.9rem', fontWeight: 600, textDecoration: 'none' }}>hola@marketinai.net</a>
            <a href="/servicios/" style={{ color: 'var(--text2)', fontSize: '0.9rem', fontWeight: 600, textDecoration: 'none' }}>Servicios</a>
            <a className="nav-cta" href={STRIPE_PAYMENT_LINK} target="_blank" rel="noopener noreferrer">
              Acceder al Kit — €397
            </a>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="hero">
        <div className="container">
          <div className="hero-badge">
            <span className="hero-badge-dot"></span>
            Precio de fundadores — plazas limitadas
          </div>
          <h1>
            Automatiza tu negocio<br />
            con <span className="accent">IA</span> en <span className="accent2">4 horas</span>
          </h1>
          <p className="hero-sub">
            Kit completo: 6 flujos n8n listos para instalar + sesión 1-a-1 de implementación.
            Capta leads, gestiona soporte y publica contenido en piloto automático — sin contratar a nadie.
          </p>
          <div className="hero-cta-group">
            <a className="btn-primary" href={STRIPE_PAYMENT_LINK} target="_blank" rel="noopener noreferrer">
              Quiero automatizar mi negocio →
            </a>
            <a className="btn-secondary" href="#kit">
              Ver qué incluye ↓
            </a>
          </div>
          <div className="hero-social-proof">
            <div className="avatars">
              {['CR', 'MV', 'JL', 'AP', 'RG'].map((i) => (
                <div key={i} className="avatar">{i}</div>
              ))}
            </div>
            <p className="social-proof-text">
              <strong>+47 negocios</strong> ya automatizan con este kit
            </p>
          </div>
        </div>
      </section>

      {/* LOGOS STRIP */}
      <div className="logos-strip">
        <div className="container">
          <p className="logos-label">Funciona con las herramientas que ya usas</p>
          <div className="logos-row">
            {['n8n', 'OpenAI GPT-4', 'Telegram', 'Google Sheets', 'Stripe', 'LinkedIn', 'WhatsApp'].map((l) => (
              <span key={l} className="logo-item">{l}</span>
            ))}
          </div>
        </div>
      </div>

      {/* PROBLEM */}
      <section className="section">
        <div className="container">
          <span className="section-tag">El problema</span>
          <h2>Tu tiempo vale demasiado<br />para gastarlo en <span className="accent">tareas repetitivas</span></h2>
          <p className="section-sub">
            Cada hora que pasas en tareas manuales es una hora que no estás vendiendo, mejorando tu producto o descansando.
          </p>
          <div className="pain-grid">
            {PAIN_ITEMS.map((p, idx) => (
              <div key={p.title} className="pain-card">
                <div className="pain-icon">{PAIN_SVGS[idx]}</div>
                <h3>{p.title}</h3>
                <p>{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* KIT */}
      <section className="section" id="kit">
        <div className="container">
          <span className="section-tag green">La solución</span>
          <h2>6 automatizaciones listas<br />para conectar a tu <span className="accent">negocio hoy</span></h2>
          <p className="section-sub">
            No teoría. No cursos de 40 horas. Flujos n8n pre-construidos que importas, configuras en minutos y empiezan a trabajar.
          </p>
          <div className="kit-grid">
            {KIT_ITEMS.map((k) => (
              <div key={k.n} className="kit-card">
                <div className="kit-number">{k.n}</div>
                <h3>{k.title}</h3>
                <p>{k.desc}</p>
                <span className="kit-tag">{k.tag}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SERVICIOS */}
      <section className="section" id="servicios">
        <div className="container">
          <span className="section-tag purple">Servicios productizados</span>
          <h2>También lo hacemos <span className="accent">por ti</span></h2>
          <p className="section-sub">
            Si prefieres que auditamos, arreglamos y automatizamos tu web sin tocar código, estos son nuestros servicios cerrados.
          </p>
          <div className="kit-grid">
            {[
              { title: 'Auditoría Express', price: '99€', desc: 'Radiografía completa de tu web con evidencia real y prioridades P0/P1/P2.', href: '/servicios/auditoria-express/' },
              { title: 'Auditoría + Fix 48h', price: '399€', desc: 'No solo diagnóstico: aplicamos los fixes críticos en 48 horas.', href: '/servicios/auditoria-fix-48h/' },
              { title: 'Plan Crecimiento', price: '199€/mes', desc: 'Mantenimiento SEO, velocidad y contenidos cada mes. Sin permanencia.', href: '/servicios/plan-crecimiento/' },
              { title: 'Pack Presencia Local', price: '199€ + 99€/mes', desc: 'Google Business Profile optimizado + SEO local para captar clientes cerca.', href: '/servicios/presencia-local/' },
              { title: 'Automatización a Medida', price: 'desde 500€', desc: 'Flujos n8n y agentes IA diseñados para tu proceso concreto.', href: '/servicios/automatizacion/' },
            ].map((s) => (
              <a key={s.title} href={s.href} className="kit-card" style={{ textDecoration: 'none' }}>
                <div className="kit-number">{s.price}</div>
                <h3>{s.title}</h3>
                <p>{s.desc}</p>
                <span className="kit-tag">Ver servicio →</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* PRICING */}
      <section className="section" id="precio">
        <div className="container" style={{ textAlign: 'center' }}>
          <span className="section-tag blue">Precio</span>
          <h2>Invierte menos de lo que cobras<br />en <span className="accent2">dos clientes</span></h2>
          <p className="section-sub" style={{ margin: '0 auto 56px' }}>
            Una vez compras el Kit, es tuyo para siempre. Sin suscripción. Sin licencias por flujo.
          </p>
          <div className="pricing-wrapper">
            <div className="price-card featured">
              <div className="price-badge">Fundadores — plazas limitadas</div>
              <p className="price-title">Kit MarketinAI Completo</p>
              <p className="price-sub">Acceso de por vida · Sin suscripción</p>
              <div className="price-amount">
                <span className="price-currency">€</span>
                <span className="price-number">397</span>
              </div>
              <p className="price-old">Precio normal: €597</p>
              <ul className="price-features">
                <li><span className="check">✓</span> 6 flujos n8n listos para instalar</li>
                <li><span className="check">✓</span> Sesión 1-a-1 de implementación (60 min)</li>
                <li><span className="check">✓</span> Canal privado Telegram 30 días</li>
                <li><span className="check">✓</span> Actualizaciones de por vida</li>
                <li><span className="check">✓</span> Documentación paso a paso en español</li>
                <li><span className="check">✓</span> Garantía 14 días sin preguntas</li>
              </ul>
              <a className="btn-price primary" href={STRIPE_PAYMENT_LINK} target="_blank" rel="noopener noreferrer">
                Quiero el Kit por €397 →
              </a>
            </div>
            <div className="price-card">
              <p className="price-title">Precio normal</p>
              <p className="price-sub">Después del período de fundadores</p>
              <div className="price-amount">
                <span className="price-currency">€</span>
                <span className="price-number">597</span>
              </div>
              <p className="price-period">pago único</p>
              <ul className="price-features">
                <li><span className="check">✓</span> 6 flujos n8n</li>
                <li><span className="check">✓</span> Sesión 1-a-1</li>
                <li><span className="check">✓</span> Actualizaciones de por vida</li>
                <li><span className="check">✓</span> Garantía 14 días</li>
              </ul>
              <a className="btn-price secondary" href={STRIPE_PAYMENT_LINK_NORMAL} target="_blank" rel="noopener noreferrer">
                Comprar a precio normal
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* GARANTIA */}
      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="guarantee-box">
            <div className="guarantee-icon"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#34d399" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg></div>
            <h3>Garantía de resultados 14 días</h3>
            <p>
              Si en 14 días no has automatizado al menos una tarea que te ahorre 2 horas semanales,
              te devuelvo el 100% del dinero. Sin formularios. Sin burocracia.
              Solo escríbeme y listo.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="section" style={{ paddingTop: 0 }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <span className="section-tag">FAQ</span>
          <h2 style={{ marginBottom: 16 }}>Preguntas frecuentes</h2>
          <p className="section-sub" style={{ margin: '0 auto 48px' }}>
            Todo lo que necesitas saber antes de comprar.
          </p>
          <div className="faq-list">
            {FAQS.map((f, i) => (
              <div
                key={i}
                className={`faq-item${openFaq === i ? ' open' : ''}`}
                onClick={() => setOpenFaq(openFaq === i ? null : i)}
              >
                <div className="faq-q">
                  {f.q}
                  <span>{openFaq === i ? '−' : '+'}</span>
                </div>
                <div className="faq-a">{f.a}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA FINAL */}
      <section className="cta-final">
        <div className="container">
          <div className="urgency-bar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="#fca5a5" aria-hidden="true"><path d="M13 2L4.09 12.26a1 1 0 0 0 .91 1.74H11l-1 8 9.09-10.26a1 1 0 0 0-.91-1.74H13l1-8z"/></svg>
            Solo quedan plazas de fundadores a €397
          </div>
          <h2>Empieza a automatizar<br />esta semana</h2>
          <p>
            Cada semana que esperas son horas perdidas en tareas que una IA puede hacer por ti.
            El Kit está listo. Solo falta que tú lo instales.
          </p>
          <a className="btn-primary" href={STRIPE_PAYMENT_LINK} target="_blank" rel="noopener noreferrer">
            Acceder al Kit MarketinAI — €397 →
          </a>
        </div>
      </section>

      {/* FOOTER */}
      <footer>
        <div className="container">
          <p>
            © 2026 MarketinAI · <a href="mailto:hola@marketinai.net">hola@marketinai.net</a>
            {' · '}
            <a href="/pricing">Precios</a>
            {' · '}
            <a href="/servicios/">Servicios</a>
            {' · '}
            <a href="/contact">Contacto</a>
            {' · '}
            <a href="/privacidad">Privacidad</a>
            {' · '}
            <a href="/terminos">Términos</a>
          </p>
          <p style={{ marginTop: '0.75rem', fontSize: '0.8rem', opacity: 0.65 }}>
            ¿Necesitas asesoría legal para tu negocio? <a href="https://abogadoai.net" target="_blank" rel="noopener" style={{ color: 'inherit', textDecoration: 'underline' }}>AbogadoAI — consulta legal con IA</a>
            {' · '}
            <a href="https://cursosai.net" target="_blank" rel="noopener" style={{ color: 'inherit', textDecoration: 'underline' }}>Formación en IA — CursosAI</a>
          </p>
        </div>
      </footer>
    </>
  )
}
