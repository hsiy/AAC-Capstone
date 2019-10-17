from django import forms

class DecisionsActionsForm(forms.Form):
    decisionProcess = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Process")
    decisionMakers = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Makers")
    decisionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Decision Timeline")
    dataUsed = forms.CharField(widget= forms.Textarea, max_length=3000, label="Data Used")
    actionTimeline = forms.CharField(widget= forms.Textarea, max_length=3000, label="Action Timeline")