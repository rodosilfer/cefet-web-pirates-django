from django.shortcuts import render,redirect
from django.views import View
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from . import models
from . import forms
from django.contrib import messages


class ListaTesourosView(View):
    def get(self, request):
        lista_tesouros = models.Tesouro.objects.annotate(
            total=ExpressionWrapper(
                F('preco') * F('quantidade'),
                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    blank=True
                )
            )
        ).all()
        return render(
            request,
            template_name='lista_tesouros.html',
            context=dict(
                lista_tesouros=lista_tesouros,
                total_geral=lista_tesouros.aggregate(Sum('total'))['total__sum']
            )
        )

class SalvarTesouroView(View):
    def get(self, request, pk=None):
        form = forms.TesouroForm()
        if pk:
            form = forms.TesouroForm(
                instance=models.Tesouro.objects.get(pk=pk)
            )
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=form,
                action=f'/editar/{pk}' if pk else 'novo'
            )
        )

    def post(self, request, pk=None):
        form = forms.TesouroForm(
            request.POST,
            request.FILES,
            instance=models.Tesouro.objects.get(pk=pk) if pk else None
        )
        if form.is_valid():
            
            form.save()
            return redirect('lista')
    
        
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=form,
                action=f'/editar/{pk}' if pk else 'novo'
            )
        )

class DeletarTesouroView(View):
    def get(self,request,pk=None):
        models.Tesouro.objects.get(pk=pk).delete()
        return redirect('lista')