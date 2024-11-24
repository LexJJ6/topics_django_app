# este ficheiro só existe para ter funcoes utilizadas multiplas vezes nas views

from .models import Topic, Comment

def gen_sm(type, action):
    # generate success message
    # funcao reutilizavel para gerar a mensagem que vai nos http response de sucesso
    if type not in ['Tópico','Comentário'] or action not in ['criado','editado','eliminado']:
        return 'Ocorreu um erro inesperado.' # ver argumentos passados se aparecer isto
    else:
        return f"{type} {action} com sucesso."
    
def gen_ne(type):
    # generate non existent message
    # funcao reutilizavel para gerar a mensagem que vai nos http response de nao existente
    if type not in ['tópico','comentário']:
        return 'Ocorreu um erro inesperado.'
    else:
        return f"Não existe tal {type}."

def get_topic(topic_id):
    # para retornar um objeto Topic ou None
    try:
        return Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return None
    
def get_comment(comment_id):
    try:
        return Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return None