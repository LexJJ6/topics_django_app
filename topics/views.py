from django.http import HttpResponse
from django.template import loader
from .models import Topic
from django.views.decorators.csrf import csrf_exempt # para as rotas POST
from django.contrib.auth.models import User # para criar verificar autores
from django.shortcuts import redirect
from .utils import *
from .forms import *

def index(request):
    # get
    latest_topic_list = Topic.objects.order_by('-created_at')[:5] # o - antes do atributo created_at é para ordem descendente
    template = loader.get_template("topics/index.html")
    context = {
        "latest_topic_list": latest_topic_list
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def new_topic(request):
    # get e post
    if request.method == 'GET':
        # formulario para novo topico
        template = loader.get_template("topics/new_topic.html")
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        # acao de criacao de novo topico
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        if not title or not description or not author:
            template = loader.get_template("topics/new_topic.html")
            return HttpResponse(template.render({
                "message": "Não podem ficar campos vazios!"
            }, request))
        try:
            Topic.objects.create(
                title=title,
                description=description,
                author=User.objects.create(username=author)
                # author= User.objects.get(username='joaoalex') # unico user que tenho que é o superuser
                # em alternativa poderia fazer User.objects.get(author) e se nao existisse criava com User.objects.create(username=author) ou algo assim, mas o autor não parece ser muito importante para este trabalho, acabou por ficar assim
            )
        except:
            return redirect(".") # redireciona novamente para o formulario, sem informacao adicional
        sr_template = loader.get_template("topics/sm.html") # success return template
        return HttpResponse(sr_template.render({
            "message": gen_sm('Tópico', 'criado')
        }, request)) # se chegar aqui é porque nao ocorreu nenhuma excecao

def topic_details(request, topic_id):
    # get
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    else:
        topic_comments = Comment.objects.filter(topic=topic).order_by('-created_at')
        template = loader.get_template("topics/topic_details.html")
        context = {
            # o id nao vou querer mostrar por isso tambem não é relevante passá-lo  pelo contexto
            "title": topic.title,
            "description": topic.description,
            "author": topic.author.username,
            "comments": topic_comments
        }
        return HttpResponse(template.render(context, request))

@csrf_exempt
def edit_topic(request, topic_id):
    # get e post
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    else:
        if request.method == 'GET':
            # formulario para editar topico
            template = loader.get_template("topics/edit_topic.html")
            try:
                context = {
                    "title": topic.title,
                    "description": topic.description
                }
            except:
                context = {}
            return HttpResponse(template.render(context, request))
        if request.method == 'POST':
            # acao de edicao de topico
            title = request.POST.get('title')
            description = request.POST.get('description')
            # se for enviada uma string vazia usar o valor anterior
            if not title:
                title = topic.title
            if not description :
                description = topic.description
            try:
                Topic.objects.filter(id=topic_id).update(
                    title=title,
                    description=description
                )
            except:
                return redirect(".")
            sr_template = loader.get_template("topics/sm.html")
            return HttpResponse(sr_template.render({
                "message": gen_sm('Tópico', 'editado')
            }, request))

@csrf_exempt
def delete_topic(request, topic_id):
    # get e post
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    else:
        if request.method == 'GET':
            # formulario para confirmar intencao de delete do topico
            template = loader.get_template("topics/delete_topic.html")
            try:
                context = {
                    "title": topic.title,
                    "description": topic.description
                }
            except:
                context = {}
            return HttpResponse(template.render(context, request))
        if request.method == 'POST':
            # acao de delete do topico
            try:
                Topic.objects.filter(id=topic_id).delete()
            except:
                return redirect(".")
            sr_template = loader.get_template("topics/sm.html")
            return HttpResponse(sr_template.render({
                "message": gen_sm('Tópico', 'eliminado')
            }, request))

'''
@csrf_exempt
def new_comment(request, topic_id):
    # get e post
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    if request.method == 'GET':
        # formulario para novo comment
        template = loader.get_template("topics/new_comment.html")
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        # acao de criacao de novo comment
        text = request.POST.get('text')
        author = request.POST.get('author')
        if not text or not author:
            template = loader.get_template("topics/new_comment.html")
            return HttpResponse(template.render({
                "message": "Não podem ficar campos vazios!"
            }, request))
        try:
            Comment.objects.create(
                text=text,
                author=User.objects.create(username=author),
                topic=topic
            )
        except:
            return redirect(".")
        sr_template = loader.get_template("topics/sm.html")
        return HttpResponse(sr_template.render({
            "message": gen_sm('Comentário', 'criado')
        }, request))
'''

@csrf_exempt
def new_comment(request, topic_id):
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))

    if request.method == 'GET':
        form = CommentForm()
        template = loader.get_template("topics/new_comment.html")
        return HttpResponse(template.render({'form': form}, request))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            author_name = form.cleaned_data['author']
            try:
                author = User.objects.create(username=author_name)
                Comment.objects.create(text=text, author=author, topic=topic)
                sr_template = loader.get_template("topics/sm.html")
                return HttpResponse(sr_template.render({
                    "message": gen_sm('Comentário', 'criado')
                }, request))
            except:
                return redirect(".")
        else:
            template = loader.get_template("topics/new_comment.html")
            return HttpResponse(template.render({
                'form': form,
                'message': "Não podem ficar campos vazios!"
            }, request))

@csrf_exempt
def edit_comment(request, topic_id, comment_id):
    # get e post
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    comment = get_comment(comment_id)
    if comment is None:
        return HttpResponse(gen_ne('comentário'))
    if comment.topic.id is not topic.id:
        # é suposto manter a logica de ser um comentario do topico
        return HttpResponse(gen_ne('comentário'))
    else:
        if request.method == 'GET':
            template = loader.get_template("topics/edit_comment.html")
            try:
                context = {
                    "text": comment.text
                }
            except:
                context = {}
            return HttpResponse(template.render(context, request))
        if request.method == 'POST':
            text = request.POST.get('text')
            if not text:
                text = comment.text
            try:
                Comment.objects.filter(id=comment_id).update(
                    text=text
                )
            except:
                return redirect(".")
            sr_template = loader.get_template("topics/sm.html")
            return HttpResponse(sr_template.render({
                "message": gen_sm('Comentário', 'editado')
            }, request))

@csrf_exempt
def delete_comment(request, topic_id, comment_id):
    # get e post
    topic = get_topic(topic_id)
    if topic is None:
        return HttpResponse(gen_ne('tópico'))
    comment = get_comment(comment_id)
    if comment is None:
        return HttpResponse(gen_ne('comentário'))
    if comment.topic.id is not topic.id:
        return HttpResponse(gen_ne('comentário'))
    else:
        if request.method == 'GET':
            template = loader.get_template("topics/delete_comment.html")
            try:
                context = {
                    "text": comment.text
                }
            except:
                context = {}
            return HttpResponse(template.render(context, request))
        if request.method == 'POST':
            try:
                Comment.objects.filter(id=comment_id).delete()
            except:
                return redirect(".")
            sr_template = loader.get_template("topics/sm.html")
            return HttpResponse(sr_template.render({
                "message": gen_sm('Comentário', 'eliminado')
            }, request))