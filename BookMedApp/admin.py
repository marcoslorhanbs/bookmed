from .models import Profissional, Agendamento
from django.contrib import admin

admin.site.site_title = "Painel do BookMed"

# Muda o cabeçalho que aparece no topo da página
admin.site.site_header = "Administração do BookMed"

# Muda o texto da página inicial do admin
admin.site.index_title = "Bem-vindo à Area do Profissional"



@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('profissional', 'paciente', 'data', 'hora', 'status')
    list_filter = ('status', 'data')
    search_fields = ('paciente__nome', 'profissional__nome')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # filtra apenas os agendamentos do profissional logado
        return qs.filter(profissional__user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # só permite alterar se for do próprio profissional ou superuser
        return obj.profissional.user == request.user or request.user.is_superuser



@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
      # <-- ESSENCIAL
    list_display = ('nome', 'email', 'tipo_consulta', 'valor_consulta')
    readonly_fields = ('user',)
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser