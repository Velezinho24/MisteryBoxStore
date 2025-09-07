from django.views.generic import TemplateView
from django.utils.translation import gettext as _

class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Datos mock
        ctx["boxes"] = [
            {
                "slug": "fashion-mystery",
                "name": _("Fashion Mystery"),
                "desc": _("Premium clothing, shoes, and accessories from top brands"),
                "price": 49,
                "value_text": _("Value up to $200"),
                "premium": False,
                "icon": "bi-bag",
                "cta": _("Open Box"),
                "cta_premium": _("Open Premium"),
            },
            {
                "slug": "tech-mystery",
                "name": _("Tech Mystery"),
                "desc": _("Latest gadgets, accessories, and electronic devices"),
                "price": 99,
                "value_text": _("Value up to $500"),
                "premium": False,
                "icon": "bi-cpu-fill",
                "cta": _("Open Box"),
                "cta_premium": _("Open Premium"),
            },
            {
                "slug": "home-mystery",
                "name": _("Home Mystery"),
                "desc": _("Unique decorations, furniture, and home essentials"),
                "price": 79,
                "value_text": _("Value up to $300"),
                "premium": False,
                "icon": "bi-house-heart-fill",
                "cta": _("Open Box"),
                "cta_premium": _("Open Premium"),
            },
            {
                "slug": "ultimate-mystery",
                "name": _("Ultimate Mystery"),
                "desc": _("The highest tier with exclusive luxury items"),
                "price": 199,
                "value_text": _("Value up to $1000"),
                "premium": True,
                "icon": "bi-trophy-fill",
                "cta": _("Open Box"),
                "cta_premium": _("Open Premium"),
                "badge": _("Premium"),
            },
        ]

        ctx["products"] = [
            {
                "title": _("Limited Edition Sneakers"),
                "alt": _("Designer Sneakers"),
                "desc": _("Exclusive designer sneakers from top luxury brands"),
                "price": 180,
                "found_in": [
                    (_("Fashion Mystery ($49)"), _("Save $131")),
                    (_("Ultimate Mystery ($199)"), _("Guaranteed + More")),
                ],
            },
            {
                "title": _("Pro Wireless Earbuds"),
                "alt": _("Wireless Earbuds"),
                "desc": _("Latest noise-canceling wireless earbuds with premium sound"),
                "price": 249,
                "found_in": [
                    (_("Tech Mystery ($99)"), _("Save $150")),
                    (_("Ultimate Mystery ($199)"), _("Save $50")),
                ],
            },
            {
                "title": _("Luxury Smart Watch"),
                "alt": _("Smart Watch"),
                "desc": _("Premium smartwatch with health tracking and luxury design"),
                "price": 399,
                "found_in": [
                    (_("Tech Mystery ($99)"), _("Save $300")),
                    (_("Ultimate Mystery ($199)"), _("Save $200")),
                ],
            },
        ]
        return ctx
