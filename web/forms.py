from django import forms
from django.core.validators import RegexValidator
from .models import Orden

class OrdenForm(forms.ModelForm):
    METODOS_PAGO = [
        ('nequi', 'Nequi'),
        ('bancolombia', 'Bancolombia'),
    ]

    metodo_pago = forms.ChoiceField(
        choices=METODOS_PAGO,
        widget=forms.RadioSelect,
        required=True,
        label="Método de pago"
    )

    telefono = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d{7,15}$', message="Ingresa un número de teléfono válido.")],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: 3001234567'
        })
    )
    
    comprobante = forms.ImageField(
        required=False,
        label="Comprobante de pago",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Orden
        fields = ['nombre', 'email', 'telefono', 'direccion', 'ciudad', 'metodo_pago', 'comprobante']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tucorreo@ejemplo.com'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de entrega'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
        }