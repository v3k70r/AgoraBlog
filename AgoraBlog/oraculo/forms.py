from django import forms

class PreguntaDestinoForm(forms.Form):
    pregunta = forms.CharField(
        label="Haz tu pregunta al I Ching",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=300
    )