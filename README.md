# Aplicação de Gestão de Tópicos de Discussão

## Descrição do Projeto
Esta aplicação web foi desenvolvida com o Django Web Framework e permite gerir tópicos de discussão de forma simples e intuitiva. Os utilizadores podem criar tópicos, comentar em discussões existentes, e editar ou eliminar conteúdos que tenham criado.

## Funcionalidades
- Operações **CRUD (Create, Read, Update, Delete)** para tópicos e comentários.
- Listagem organizada de tópicos e respetivos detalhes.
- Integração da biblioteca externa 'django-crispy-forms' para melhorar a usabilidade.
- Interface administrativa para gestão de utilizadores e conteúdos.

## Requisitos
- Python 3.8 ou superior
- Django 4.0 ou superior
- Biblioteca 'django-crispy-forms'

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/LexJJ6/topics_django_app.git
   cd topics_django_app
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # Para Linux/MacOS
   env\Scripts\activate     # Para Windows
   ```
3. Configure a base de dados:
   ```bash
   python manage.py migrate
   ```
4. Crie um superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Utilização
1. Aceda à aplicação no seu navegador em [http://127.0.0.1:8000](http://127.0.0.1:8000).
2. Para gerir os conteúdos ou utilizadores, aceda ao painel administrativo em [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e autentique-se com as credenciais do superuser.

## Testes
Para executar os testes unitários e garantir que as funcionalidades principais estão a funcionar corretamente:
```bash
python manage.py test
```
