from django.contrib import admin
from .models import Aluno, Empresa, Vaga, Candidatura
admin.site.register(Aluno)
admin.site.register(Empresa)
admin.site.register(Vaga)
admin.site.register(Candidatura)
