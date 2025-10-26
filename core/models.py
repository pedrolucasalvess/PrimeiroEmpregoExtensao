from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=40, blank=True)
    curso = models.CharField(max_length=200, blank=True)
    semestre = models.PositiveIntegerField(default=1)
    habilidades = models.TextField(blank=True)
    senha = models.CharField(max_length=128)
    def __str__(self): return self.nome

class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=40, blank=True)
    area_atuacao = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=20, blank=True)
    senha = models.CharField(max_length=128)
    def __str__(self): return self.nome

class Vaga(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    requisitos = models.TextField(blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.titulo

class Candidatura(models.Model):
    STATUS_CHOICES = [('pendente','Pendente'), ('aceita','Aceita'), ('rejeitada','Rejeitada')]
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='candidaturas')
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('aluno','vaga')
    def __str__(self): return f"{self.aluno} -> {self.vaga}"
