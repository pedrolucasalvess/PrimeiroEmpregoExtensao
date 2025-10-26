from django.core.management.base import BaseCommand
from core.models import Aluno, Empresa, Vaga

class Command(BaseCommand):
    help = 'Seed initial data (2 alunos, 2 empresas, 4 vagas)'

    def handle(self, *args, **kwargs):
        if Aluno.objects.exists() or Empresa.objects.exists() or Vaga.objects.exists():
            self.stdout.write('Dados já existem — pulando.')
            return
        a1 = Aluno.objects.create(nome='João Silva', email='joao@example.com', telefone='(41)90000-0001', curso='Engenharia de Software', semestre=3, habilidades='Python, Git', senha='senha1')
        a2 = Aluno.objects.create(nome='Maria Souza', email='maria@example.com', telefone='(41)90000-0002', curso='Sistemas de Informação', semestre=2, habilidades='HTML, CSS', senha='senha2')
        e1 = Empresa.objects.create(nome='Tech Solutions', email='contato@tech.com', telefone='(11)4000-0001', area_atuacao='Software', cnpj='12.345.678/0001-90', senha='senhaE1')
        e2 = Empresa.objects.create(nome='Office Plus', email='contato@office.com', telefone='(21)4000-0002', area_atuacao='Serviços', cnpj='98.765.432/0001-10', senha='senhaE2')
        Vaga.objects.create(titulo='Estágio em TI', descricao='Estágio para aprender backend.', requisitos='Noções de Python', cidade='São Paulo', empresa=e1)
        Vaga.objects.create(titulo='Auxiliar Administrativo', descricao='Suporte administrativo.', requisitos='Organização', cidade='Rio de Janeiro', empresa=e2)
        Vaga.objects.create(titulo='Desenvolvedor Frontend Jr', descricao='React + Tailwind', requisitos='React', cidade='Londrina', empresa=e1)
        Vaga.objects.create(titulo='Estágio Suporte', descricao='Suporte técnico', requisitos='Boa comunicação', cidade='Belo Horizonte', empresa=e2)
        self.stdout.write(self.style.SUCCESS('Seed concluído.'))
