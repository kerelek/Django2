from django import forms
from .models import JSONFile 

class MedicalRecordForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    patient_name = forms.CharField(
        max_length=100,
        label="Имя пациента",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        min_value=0,
        max_value=150,
        label="Возраст",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Пол",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    height = forms.FloatField(
        min_value=0,
        max_value=300,
        label="Рост (см)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    weight = forms.FloatField(
        min_value=0,
        max_value=500,
        label="Вес (кг)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    blood_pressure = forms.CharField(
        max_length=10,
        required=False,
        label="Артериальное давление",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    heart_rate = forms.IntegerField(
        min_value=0,
        max_value=300,
        required=False,
        label="Частота сердечных сокращений",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    temperature = forms.FloatField(
        min_value=30,
        max_value=45,
        initial=36.6,
        required=False,
        label="Температура тела (°C)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    symptoms = forms.CharField(
        required=False,
        label="Симптомы",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    diagnosis = forms.CharField(
        max_length=200,
        required=False,
        label="Диагноз",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class JSONUploadForm(forms.ModelForm):
    class Meta:
        model = JSONFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.json'
            }),
        }
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("Файл слишком большой. Максимальный размер: 5MB")
        return file
