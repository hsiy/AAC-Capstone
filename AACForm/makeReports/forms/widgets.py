from django import forms
from django.conf import settings
import os
"""
Includes custom widgets
"""
class SLOChoicesJSWidget(forms.widgets.Select):
    """
    Widget that uses the Choices Javascript plugin for a drop-down
    """
    template_name = 'widgets/select.html'
    option_template_name = 'widgets/option.html'
    class Media:
        css = {'all': (
            "https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css",
            os.path.join(settings.STATIC_URL,'css/slo_choices.css')
             )}
        js = (
            "https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js",
            os.path.join(settings.STATIC_URL,'extPlugin/choices-widget.js'))