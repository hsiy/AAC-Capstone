from django import forms

class SubmitReportForm(forms.Form):
    hidden = forms.CharField(max_length=5,widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        self.valid = kwargs.pop('valid')
        self.error = kwargs.pop('eMsg')
        super(SubmitReportForm, self).__init__(*args, **kwargs)
    def clean(self):
      super().clean()
      if not self.valid:
          raise forms.ValidationError(self.error)