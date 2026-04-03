"""
Custom panels for the DrawIO admin interface.

This code is distributed under the MIT License.
"""

from wagtail.admin.panels import Panel


class DrawioUsagePanel(Panel):
    """
    Read-only panel that lists every page (or other Wagtail object) that
    references this diagram, each with a direct link to its edit view.
    """

    class_name = "drawio-usage-panel"

    class BoundPanel(Panel.BoundPanel):
        template_name = "wagtail_drawio/panels/usage_panel.html"

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)

            if self.instance and self.instance.pk:
                from wagtail.admin.admin_url_finder import AdminURLFinder
                from wagtail.models import ReferenceIndex

                url_finder = AdminURLFinder(self.request.user)
                usages = []
                for obj, _refs in (
                    ReferenceIndex.get_references_to(self.instance)
                    .group_by_source_object()
                ):
                    usages.append(
                        {
                            "object": obj,
                            "label": str(obj),
                            "type": obj._meta.verbose_name,
                            "edit_url": url_finder.get_edit_url(obj),
                        }
                    )
                context["usages"] = usages
            else:
                context["usages"] = []

            return context
