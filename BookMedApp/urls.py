from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('agendamento/<str:profissional_nome>/', views.agendamento, name='agendamento'),
    path('agendar/<str:username>/', views.agendamento_cliente, name='agendamento_cliente'),
    path("cadastro_profissional/", views.cadastro_profissional, name="cadastro_profissional"),
    path("pagina_agendamento/", views.agendamento, name="pagina_agendamento"),
    path('cadastro-paciente/', views.cadastro_paciente, name='cadastro_paciente'),
    path('login-paciente/', views.login_paciente, name='login_paciente'),  # futura view
    path('perfil-paciente/', views.perfil_paciente, name='perfil_paciente'),
    path('cancelar-consulta/<int:agendamento_id>/', views.cancelar_consulta, name='cancelar_consulta'),
    path('remarcar-consulta/<int:agendamento_id>/', views.remarcar_consulta, name='remarcar_consulta'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login-agendamento/<str:username>/', views.login_agendamento, name='login_agendamento'),
    path("lucas_corno/", views.lucascorno, name="lucas_corno")
    

]