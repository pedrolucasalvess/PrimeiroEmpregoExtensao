from rest_framework import serializers
from .models import Aluno, Empresa, Vaga, Candidatura
class AlunoSerializer(serializers.ModelSerializer):
    class Meta: model = Aluno; fields = '__all__'
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta: model = Empresa; fields = '__all__'
class VagaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(), source='empresa', write_only=True)
    class Meta: model = Vaga; fields = ['id','titulo','descricao','requisitos','cidade','empresa','empresa_id','ativo','criado_em']
class CandidaturaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    aluno_id = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), source='aluno', write_only=True)
    vaga = VagaSerializer(read_only=True)
    vaga_id = serializers.PrimaryKeyRelatedField(queryset=Vaga.objects.all(), source='vaga', write_only=True)
    class Meta: model = Candidatura; fields = ['id','aluno','aluno_id','vaga','vaga_id','status','criado_em']
