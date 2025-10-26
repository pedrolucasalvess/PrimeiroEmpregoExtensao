from django.shortcuts import render, redirect, get_object_or_404
from core.models import Vaga, Empresa, Aluno, Candidatura
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    # Se não estiver logado, redireciona para login
    if not request.session.get('user_type'):
        return redirect('/login/')

    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')

    # Redireciona cada tipo de usuário para sua área
    if user_type == 'aluno':
        return redirect('/candidato/')
    elif user_type == 'empresa':
        return redirect('/empresa/')
    elif user_type == 'admin':
        return redirect('/admin/')

    return render(request, 'web/index.html', {
        'user_type': user_type,
        'user_id': user_id,
        'user_name': user_name
    })

def vagas(request):
    # Só usuários logados podem ver vagas
    if not request.session.get('user_type'):
        messages.error(request, 'Você precisa fazer login para ver as vagas.')
        return redirect('/login/')

    q = request.GET.get('q','')
    vagas = Vaga.objects.filter(ativo=True)
    if q:
        vagas = vagas.filter(
            Q(titulo__icontains=q) |
            Q(descricao__icontains=q) |
            Q(requisitos__icontains=q)
        )
    return render(request, 'web/vagas.html', {'vagas': vagas, 'query': q})

def candidato(request):
    # Só alunos podem acessar
    if request.session.get('user_type') != 'aluno':
        messages.error(request, 'Você precisa estar logado como aluno para acessar esta página.')
        return redirect('/login/')

    vagas = Vaga.objects.filter(ativo=True).order_by('-criado_em')
    return render(request, 'web/candidato.html', {'vagas': vagas})

def empresa(request):
    # Só empresas podem acessar
    if request.session.get('user_type') != 'empresa':
        messages.error(request, 'Você precisa estar logado como empresa para acessar esta página.')
        return redirect('/login/')

    empresa_id = request.session.get('user_id')
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    vagas = empresa.vagas.all().order_by('-criado_em')

    # Buscar candidaturas para cada vaga
    vagas_com_candidaturas = []
    for vaga in vagas:
        candidaturas = vaga.candidaturas.select_related('aluno').order_by('-criado_em')
        vagas_com_candidaturas.append({
            'vaga': vaga,
            'candidaturas': candidaturas
        })

    return render(request, 'web/empresa.html', {
        'empresas': Empresa.objects.all(),
        'vagas': vagas,
        'vagas_com_candidaturas': vagas_com_candidaturas,
        'selected': empresa
    })

@require_POST
def candidatar(request):
    aluno_id = request.POST.get('aluno_id')
    vaga_id = request.POST.get('vaga_id')
    if not aluno_id or not vaga_id:
        messages.error(request, 'Aluno e vaga obrigatórios.')
        return redirect(request.META.get('HTTP_REFERER','/candidato/'))
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    vaga = get_object_or_404(Vaga, pk=vaga_id)
    candidatura, created = Candidatura.objects.get_or_create(aluno=aluno, vaga=vaga)
    if not created:
        messages.info(request, 'Você já se candidatou a essa vaga.')
    else:
        messages.success(request, 'Candidatura enviada com sucesso.')
    return redirect(request.META.get('HTTP_REFERER','/candidato/'))

@require_POST
def criar_vaga(request):
    empresa_id = request.POST.get('empresa_id')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    requisitos = request.POST.get('requisitos')
    cidade = request.POST.get('cidade')
    if not empresa_id or not titulo:
        messages.error(request, 'Empresa e título são obrigatórios.')
        return redirect(request.META.get('HTTP_REFERER','/empresa/'))
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    Vaga.objects.create(titulo=titulo, descricao=descricao or '', requisitos=requisitos or '', cidade=cidade or '', empresa=empresa)
    messages.success(request, 'Vaga criada com sucesso.')
    return redirect(request.META.get('HTTP_REFERER','/empresa/'))

def cadastro_aluno(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone', '')
        curso = request.POST.get('curso', '')
        semestre = request.POST.get('semestre', 1)
        habilidades = request.POST.get('habilidades', '')
        senha = request.POST.get('senha')

        if not nome or not email or not senha:
            messages.error(request, 'Nome, email e senha são obrigatórios.')
            return redirect('/cadastro/aluno/')

        if Aluno.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('/cadastro/aluno/')

        Aluno.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            curso=curso,
            semestre=semestre,
            habilidades=habilidades,
            senha=senha
        )
        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        return redirect('/login/')

    return render(request, 'web/cadastro_aluno.html')

def cadastro_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone', '')
        area_atuacao = request.POST.get('area_atuacao', '')
        cnpj = request.POST.get('cnpj', '')
        senha = request.POST.get('senha')

        if not nome or not email or not senha:
            messages.error(request, 'Nome, email e senha são obrigatórios.')
            return redirect('/cadastro/empresa/')

        if Empresa.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('/cadastro/empresa/')

        Empresa.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            area_atuacao=area_atuacao,
            cnpj=cnpj,
            senha=senha
        )
        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        return redirect('/login/')

    return render(request, 'web/cadastro_empresa.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user_type = request.POST.get('user_type')

        if not email or not senha or not user_type:
            messages.error(request, 'Preencha todos os campos.')
            return redirect('/login/')

        if user_type == 'aluno':
            try:
                user = Aluno.objects.get(email=email, senha=senha)
                request.session['user_type'] = 'aluno'
                request.session['user_id'] = user.id
                request.session['user_name'] = user.nome
                messages.success(request, f'Bem-vindo, {user.nome}!')
                return redirect('/candidato/')
            except Aluno.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos.')

        elif user_type == 'empresa':
            try:
                user = Empresa.objects.get(email=email, senha=senha)
                request.session['user_type'] = 'empresa'
                request.session['user_id'] = user.id
                request.session['user_name'] = user.nome
                messages.success(request, f'Bem-vindo, {user.nome}!')
                return redirect('/empresa/')
            except Empresa.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos.')

        elif user_type == 'admin':
            # Para admin, usar username no campo email
            user = authenticate(request, username=email, password=senha)
            if user is not None and user.is_staff:
                auth_login(request, user)
                request.session['user_type'] = 'admin'
                request.session['user_name'] = 'Administrador'
                messages.success(request, 'Bem-vindo, Administrador!')
                return redirect('/admin/')
            else:
                messages.error(request, 'Usuário ou senha de administrador incorretos.')

        return redirect('/login/')

    return render(request, 'web/login.html')

def logout(request):
    request.session.flush()
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('/')

def perfil_candidato(request):
    if request.session.get('user_type') != 'aluno':
        messages.error(request, 'Você precisa estar logado como aluno.')
        return redirect('/login/')

    aluno_id = request.session.get('user_id')
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    candidaturas = Candidatura.objects.filter(aluno=aluno).select_related('vaga', 'vaga__empresa').order_by('-criado_em')

    return render(request, 'web/perfil_candidato.html', {
        'aluno': aluno,
        'candidaturas': candidaturas
    })

@require_POST
def gerenciar_candidatura(request, candidatura_id):
    # Só empresas podem gerenciar candidaturas
    if request.session.get('user_type') != 'empresa':
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('/login/')

    empresa_id = request.session.get('user_id')
    candidatura = get_object_or_404(Candidatura, pk=candidatura_id)

    # Verificar se a vaga pertence à empresa logada
    if candidatura.vaga.empresa.id != empresa_id:
        messages.error(request, 'Você não tem permissão para gerenciar esta candidatura.')
        return redirect('/empresa/')

    acao = request.POST.get('acao')

    if acao == 'aceitar':
        candidatura.status = 'aceita'
        candidatura.save()
        messages.success(request, f'Candidatura de {candidatura.aluno.nome} aceita com sucesso!')
    elif acao == 'recusar':
        candidatura.status = 'rejeitada'
        candidatura.save()
        messages.success(request, f'Candidatura de {candidatura.aluno.nome} recusada.')
    else:
        messages.error(request, 'Ação inválida.')

    return redirect('/empresa/')
