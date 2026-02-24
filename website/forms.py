from django import forms

SMOKER_CHOICES = [("nao", "Não"), ("sim", "Sim")]
HEALTH_CHOICES = [
    ("sem_problemas", "Sem problemas"),
    ("pressao_alta", "Pressão alta"),
    ("diabetes", "Diabetes"),
    ("colesterol", "Colesterol alto"),
    ("outros", "Outros"),
]
COVERAGE_CHOICES = [
    
   
    ("1000000", "1 milhão"),
    ("700000", "700 mil"),
    ("500000", "500 mil"),
    ("300000", "300 mil"),
]
GENDER_CHOICES = [("masculino", "Masculino"), ("feminino", "Feminino"), ("outro", "Outro")]


class QuoteForm(forms.Form):
    full_name = forms.CharField(label="Nome completo", max_length=120)
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(label="Gênero", choices=GENDER_CHOICES)
    age = forms.IntegerField(label="Idade", min_value=0, max_value=120)
    coverage = forms.ChoiceField(label="Valor do Seguro", choices=COVERAGE_CHOICES)
    smoker = forms.ChoiceField(label="Fumante?", choices=SMOKER_CHOICES)
    health = forms.ChoiceField(label="Saúde", choices=HEALTH_CHOICES)
    details = forms.CharField(
        label="Detalhes (se tiver algo importante)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )
