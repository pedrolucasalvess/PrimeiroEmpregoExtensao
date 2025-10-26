from rest_framework import viewsets
from .models import Aluno, Empresa, Vaga, Candidatura
from .serializers import AlunoSerializer, EmpresaSerializer, VagaSerializer, CandidaturaSerializer
class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all(); serializer_class = AlunoSerializer
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all(); serializer_class = EmpresaSerializer
class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all(); serializer_class = VagaSerializer
class CandidaturaViewSet(viewsets.ModelViewSet):
    queryset = Candidatura.objects.all(); serializer_class = CandidaturaSerializer
