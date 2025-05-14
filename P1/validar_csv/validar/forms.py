from django import forms

class UploadFileForm(forms.Form):
     file = forms.FileField(
        label="Selecciona archivo plano a validar",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

