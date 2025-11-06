from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from mistery_boxes.models import MysteryBox


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["boxes"] = MysteryBox.objects.all()[:4]

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
