from django.contrib import admin
from django.urls import path, include
from web import views as web_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', web_views.home, name='home'),
    path('vagas/', web_views.vagas, name='vagas'),
    path('candidato/', web_views.candidato, name='candidato'),
    path('empresa/', web_views.empresa, name='empresa'),
    path('candidatar/', web_views.candidatar, name='candidatar'),
    path('criar-vaga/', web_views.criar_vaga, name='criar_vaga'),
    path('cadastro/aluno/', web_views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/empresa/', web_views.cadastro_empresa, name='cadastro_empresa'),
    path('login/', web_views.login, name='login'),
    path('logout/', web_views.logout, name='logout'),
    path('perfil/', web_views.perfil_candidato, name='perfil_candidato'),
    path('gerenciar-candidatura/<int:candidatura_id>/', web_views.gerenciar_candidatura, name='gerenciar_candidatura'),
]
