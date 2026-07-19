"""Create Stripe products and payment links for MarketinAI services."""
import os
import stripe

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    raise SystemExit("Set STRIPE_SECRET_KEY env var")
stripe.api_key = STRIPE_SECRET_KEY

SERVICES = [
    {
        "id": "auditoria-express",
        "name": "Auditoría Express — MarketinAI",
        "description": "Radiografía completa de tu web con evidencia real y prioridades P0/P1/P2. Informe en 24h.",
        "price_cents": 9900,
        "recurring": False,
        "service_code": "MKAI-AE-99",
    },
    {
        "id": "auditoria-fix-48h",
        "name": "Auditoría + Fix 48h — MarketinAI",
        "description": "Auditoría completa + aplicación de fixes críticos en 48 horas.",
        "price_cents": 39900,
        "recurring": False,
        "service_code": "MKAI-FIX-399",
    },
    {
        "id": "plan-crecimiento",
        "name": "Plan Crecimiento — MarketinAI",
        "description": "Mantenimiento SEO, velocidad y contenidos cada mes. Sin permanencia.",
        "price_cents": 19900,
        "recurring": True,
        "interval": "month",
        "service_code": "MKAI-PC-199",
    },
    {
        "id": "presencia-local-setup",
        "name": "Pack Presencia Local (Setup) — MarketinAI",
        "description": "Google Business Profile optimizado + SEO local inicial.",
        "price_cents": 19900,
        "recurring": False,
        "service_code": "MKAI-PL-199",
    },
    {
        "id": "presencia-local-mensual",
        "name": "Pack Presencia Local (Mensual) — MarketinAI",
        "description": "Gestión continua de Google Business Profile y SEO local.",
        "price_cents": 9900,
        "recurring": True,
        "interval": "month",
        "service_code": "MKAI-PL-99M",
    },
    {
        "id": "automatizacion-medida",
        "name": "Automatización a Medida — MarketinAI",
        "description": "Flujos n8n y agentes IA diseñados para tu proceso concreto. Presupuesto cerrado.",
        "price_cents": 50000,
        "recurring": False,
        "service_code": "MKAI-AM-500",
    },
]

SUCCESS_URL = "https://marketinai.net/gracias/?service={service_code}"
CANCEL_URL = "https://marketinai.net/servicios/"


def create_product_and_price(service):
    product = stripe.Product.create(
        name=service["name"],
        description=service["description"],
        metadata={"service_id": service["id"], "service_code": service["service_code"]},
    )
    print(f"Product created: {product.id} — {service['name']}")

    price_data = {
        "product": product.id,
        "unit_amount": service["price_cents"],
        "currency": "eur",
        "metadata": {"service_id": service["id"], "service_code": service["service_code"]},
    }
    if service.get("recurring"):
        price_data["recurring"] = {"interval": service["interval"]}

    price = stripe.Price.create(**price_data)
    print(f"Price created: {price.id} — {service['price_cents']/100}€")

    payment_link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        after_completion={
            "type": "redirect",
            "redirect": {"url": SUCCESS_URL.format(service_code=service["service_code"])},
        },
        metadata={"service_id": service["id"], "service_code": service["service_code"]},
    )
    print(f"PaymentLink created: {payment_link.url}")

    return {
        "service_id": service["id"],
        "service_code": service["service_code"],
        "product_id": product.id,
        "price_id": price.id,
        "payment_link": payment_link.url,
    }


def main():
    results = []
    for service in SERVICES:
        try:
            result = create_product_and_price(service)
            results.append(result)
        except Exception as exc:
            print(f"ERROR creating {service['id']}: {exc}")
    return results


if __name__ == "__main__":
    results = main()
    print("\n=== RESULTS ===")
    for r in results:
        print(f"{r['service_code']}: {r['payment_link']}")
