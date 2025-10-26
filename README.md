PrimeiroEmprego - Versão final funcional (starter)
-------------------------------------------------

Funcionalidades incluídas:
- Backend Django + Django REST Framework (SQLite)
- Templates com Tailwind via CDN (sem npm)
- Páginas:
  - /     -> Landing
  - /vagas/ -> Lista todas vagas (com filtro)
  - /candidato/ -> Visualiza vagas e pode candidatar (form)
  - /empresa/ -> Visualiza vagas da empresa e pode criar vaga (form)
- API endpoints: /api/alunos/, /api/empresas/, /api/vagas/, /api/candidaturas/
- Management command: `python manage.py seed_data` para criar dados de teste

Rápido para rodar:
1. python -m venv venv
2. source venv/bin/activate   (ou venv\Scripts\activate no Windows)
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py seed_data
6. python manage.py runserver
7. Abrir http://127.0.0.1:8000/

OBS: Senhas nos modelos são campos simples para facilitar testes. Troque para auth do Django antes de produção.
