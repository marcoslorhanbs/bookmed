from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from .models import Profissional
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Paciente, Agendamento
from django.contrib.auth import authenticate, login
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request, 'BookMedApp/home.html')  # caminho relativo à pasta templates

def agendamento(request):
    return render(request, 'BookMedApp/agendamento.html')

def perfil(request):
    return render(request, 'BookMedApp/perfil.html')


def cadastro_profissional(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        chave_pix = request.POST['pix']
        bio = request.POST['bio']
        registro = request.POST['registro']
        valor = request.POST['valor']
        username = request.POST['username']
        password = request.POST['password']

        # cria usuário admin
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_staff=True
            
        )

        # adiciona permissão de mudar o próprio Profissional
        content_type = ContentType.objects.get_for_model(Profissional)
        permission = Permission.objects.get(
            codename='change_profissional',
            content_type=content_type,
        )
        user.user_permissions.add(permission)


        # cria profissional vinculado ao usuário
        Profissional.objects.create(
            user=user,
            nome=nome,
            email=email,
            telefone_whatsapp=telefone,
            chave_pix=chave_pix,
            bio=bio,
            registro_profissional=registro,
            valor_consulta=valor,
            #link_agendamento=f"https://127.0.0.1:8000/agendar/{username}"
        )
        logout(request)

        # redireciona para página de login do admin
        return redirect('/admin/')

    return render(request, 'BookMedApp/cadastro_profissional.html')

def agendamento_cliente(request, username):
    profissional = get_object_or_404(Profissional, user__username=username)

    paciente = None
    if request.user.is_authenticated:
        paciente = get_object_or_404(Paciente, user=request.user)

    if request.method == 'POST':
        data = request.POST['data']
        hora = request.POST['hora']

        Agendamento.objects.create(
            profissional=profissional,
            paciente=paciente,
            data=data,
            hora=hora,
            status='marcado'
        )

        # passa o link do WhatsApp para o template
        numero = profissional.telefone_whatsapp  # exemplo
        mensagem = f"Consulta agendada via BookMed, \n Nome do Paciente: {paciente.nome},\n telefone do paciente: {paciente.telefone_whatsapp},\n data: {data}, horario: {hora}\n Profissional: {profissional.nome}\n chave pix: {profissional.chave_pix}, valor da consulta: {profissional.valor_consulta}\n Mandar Comprovante via whatsapp do profissional: {profissional.telefone_whatsapp}"
        #whatsapp_url = f"https://wa.me/+55{numero}?text=ola"
        
        return redirect(f"https://wa.me/+55{numero}?text={mensagem}")
    return render(request, 'BookMedApp/agendamento_cliente.html', {'profissional': profissional})



from .models import Paciente

def cadastro_paciente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        telefone = request.POST['telefone']
        username = request.POST['username']
        password = request.POST['password']


        # cria usuário
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        # cria paciente vinculado ao usuário
        Paciente.objects.create(
            user=user,
            nome=nome,
            email=email,
            telefone_whatsapp=telefone,
        )

        # redireciona para página de login
        return redirect('login_paciente')

    return render(request, 'BookMedApp/cadastro_paciente.html')



def login_paciente(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redireciona para a área do paciente (perfil)
            return redirect('perfil_paciente')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'BookMedApp/login_paciente.html')

@login_required
def perfil_paciente(request):
    # pega o paciente vinculado ao usuário logado
    paciente = Paciente.objects.get(user=request.user)

    # busca todas as consultas do paciente
    agendamentos = Agendamento.objects.filter(paciente=paciente).order_by('-data', '-hora')

    return render(request, 'BookMedApp/perfil_paciente.html', {
        'paciente': paciente,
        'agendamentos': agendamentos
    })


@login_required
def cancelar_consulta(request, agendamento_id):
    agendamento = Agendamento.objects.get(id=agendamento_id, paciente__user=request.user)
    agendamento.status = 'cancelado'
    agendamento.save()
    return redirect('perfil_paciente')

@login_required
def remarcar_consulta(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, paciente__user=request.user)

    if request.method == 'POST':
        nova_data = request.POST['data']
        nova_hora = request.POST['hora']

        agendamento.data = nova_data
        agendamento.hora = nova_hora
        agendamento.status = 'remarcado'
        agendamento.save()

        return redirect('perfil_paciente')

    # se acessar sem POST, redireciona
    return redirect('perfil_paciente')


def agendamento(request, profissional_nome):
    # busca o profissional pelo nome
    profissional = Profissional.objects.get(nome=profissional_nome)

    paciente = None
    if request.user.is_authenticated:
        try:
            paciente = Paciente.objects.get(user=request.user)
        except Paciente.DoesNotExist:
            paciente = None

    if request.method == 'POST':
        data = request.POST['data']
        hora = request.POST['hora']

        Agendamento.objects.create(
            profissional=profissional,
            paciente=paciente if paciente else None,
            data=data,
            hora=hora,
            status='marcado'
        )
        return redirect('perfil_paciente' if paciente else 'home')

    return render(request, 'BookMedApp/agendamento.html', {
        'profissional': profissional,
        'paciente': paciente
    })

def login_agendamento(request, username):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('agendamento_cliente', username=username)
        else:
            messages.error(request, "Usuário ou senha inválidos.")
            return redirect('agendamento_cliente', username=username)

def lucascorno():
    return redirect('BookMedApp/lucas_corno.html')