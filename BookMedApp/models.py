from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # vincula ao usuário admin
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone_whatsapp = models.CharField(max_length=20)
    chave_pix = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    registro_profissional = models.CharField(max_length=50, help_text="CRP, OAB, CRM etc.")
    #link_agendamento = models.CharField()
    # Configurações da página de agendamento
    imagem_cabecalho = models.ImageField(upload_to='cabecalhos/', blank=True, null=True)
    tipo_consulta = models.CharField(
        max_length=50,
        choices=[
            ('medico', 'Médico'),
            ('psicologo', 'Psicólogo'),
            ('nutricionista', 'Nutricionista'),
            ('advogado', 'Advogado'),
        ]
    )
    dias_nao_atende = models.TextField(help_text="Informe os dias que não atende (ex: sábado, domingo)")
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # login do paciente
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone_whatsapp = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('marcado', 'Marcado'),
            ('cancelado', 'Cancelado'),
            ('remarcado', 'Remarcado'),
        ],
        default='marcado'
    )

    def __str__(self):
        return f"{self.paciente.nome} com {self.profissional.nome} em {self.data} às {self.hora}"