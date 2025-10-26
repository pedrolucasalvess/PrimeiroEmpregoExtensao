from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, EmpresaViewSet, VagaViewSet, CandidaturaViewSet
router = DefaultRouter()
router.register('alunos', AlunoViewSet)
router.register('empresas', EmpresaViewSet)
router.register('vagas', VagaViewSet)
router.register('candidaturas', CandidaturaViewSet)
urlpatterns = [ path('', include(router.urls)), ]
