from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.curriculum.models import Module, Topic, CodeExample, Problem
from apps.assignments.models import ProblemAccess

User = get_user_model()

RAW_MODULES = [
    {
        'level': 'beginner',
        'name': 'Django Fundamentals',
        'topics': [
            {
                'id': 'intro-setup',
                'title': 'Django Intro & Setup',
                'explain': [
                    'Django nu solradhu Python la eluthapatta oru web framework. Framework nu solra mudhala vera edhu illa — website build pannradhuku venum irukura basic structure ellam already ready ah iruku, nee business logic mattum eludhinaa podhum.',
                    'Django "batteries included" nu solradhu enna nu na explain panren — login system, admin panel, database handling, security ellam already built-in ah irukum. So nee ratha vera scratch la eludha vendam.',
                    'Setup panradhuku mudhalla virtual environment create pannanum. Virtual environment nu solradhu — oru thani box, adhukulla unga project ku venum ana packages mattum install aagum, system wide ah vera projects oda mix aagadhu.'
                ],
                'examples': [
                    {
                        'label': 'terminal — install & setup',
                        'code': '# virtual environment create pannurom\npython -m venv myenv\n\n# activate pannurom (windows)\nmyenv\\Scripts\\activate\n\n# activate pannurom (mac/linux)\nsource myenv/bin/activate\n\n# django install\npip install django\n\n# version check\ndjango-admin --version'
                    }
                ],
                'labs': [
                    'Unga system la Python version enna nu terminal la check pannunga (python --version).',
                    'Oru virtual environment create panni, adhula django install pannunga.',
                    '"django-admin --version" run panni output screenshot eduthu vachukonga.'
                ]
            },
            {
                'id': 'project-structure',
                'title': 'Project Structure',
                'explain': [
                    'django-admin startproject nu command kudutha, Django unga ku oru full project structure create panni tharum. Idhula erukura mukkiyamana files na — manage.py, settings.py, urls.py.',
                    'manage.py — idhu unga command center. Server run pannradhu, migration pannradhu, ellame idha vachu than.',
                    'settings.py — unga project oda ella configuration um (database, installed apps, security) idhula irukum.',
                    'urls.py — user oru URL type pannumbodhu, adha eppadi handle panradhu nu decide panra file idhu than — "traffic police" mari nu nenachikonga.'
                ],
                'examples': [
                    {
                        'label': 'terminal',
                        'code': 'django-admin startproject myproject\ncd myproject\npython manage.py runserver'
                    },
                    {
                        'label': 'folder structure',
                        'code': 'myproject/\n    manage.py\n    myproject/\n        __init__.py\n        settings.py\n        urls.py\n        asgi.py\n        wsgi.py'
                    }
                ],
                'labs': [
                    '"myportfolio" nu peru vacha oru new project create pannunga.',
                    'runserver run panni browser la http://127.0.0.1:8000 open pannunga — rocket page varuma nu check pannunga.',
                    'settings.py file open panni, INSTALLED_APPS list la enna enna already irukku nu note pannunga.'
                ]
            },
            {
                'id': 'apps',
                'title': 'Django Apps',
                'explain': [
                    'Django la project vera, app vera. Project nu solradhu unga full website (example: unga online store). App nu solradhu adhukulla oru specific feature (example: products app, cart app, users app).',
                    'Ipadi chinna chinna apps ah pirichu eludhradhaala, code reusable ah irukum, and confusion illama vera vera team members vera vera apps la velai pannalam.',
                    'Oru app create pannadhum, adha settings.py oda INSTALLED_APPS list la add pannanum — illana Django adha recognize pannadhu.'
                ],
                'examples': [
                    {
                        'label': 'terminal',
                        'code': 'python manage.py startapp blog'
                    },
                    {
                        'label': 'settings.py',
                        'code': 'INSTALLED_APPS = [\n    \'django.contrib.admin\',\n    \'django.contrib.auth\',\n    \'django.contrib.contenttypes\',\n    \'django.contrib.sessions\',\n    \'django.contrib.messages\',\n    \'django.contrib.staticfiles\',\n    \'blog\',   # <-- namma app add pannanum\n]'
                    }
                ],
                'labs': [
                    '"blog" nu peru vacha oru app create pannunga.',
                    'Adha INSTALLED_APPS la add pannunga.',
                    'blog app folder inside enna enna files auto ah create aagi irukku nu list pannunga (models.py, views.py, admin.py...).'
                ]
            }
        ]
    },
    {
        'level': 'beginner',
        'name': 'Routing & Views',
        'topics': [
            {
                'id': 'urls',
                'title': 'URLs & Routing',
                'explain': [
                    'User browser la oru address type pannumbodhu (example: /about/), adha Django eppadi handle pannum nu solradhu urls.py than.',
                    'path() function use panni, oru URL pattern ku edho oru view function ah link pannuvom. path() ku 3 mukkiyamana arguments — route (URL text), view (edha call pannanum), name (identify panna oru peru).',
                    'Project la irukura main urls.py, individual apps oda urls.py file kooda include() vachu link pannalam — ipadi pannina, project neat ah irukum, and ovvoru app um thani thaniya routes maintain pannikalam.'
                ],
                'examples': [
                    {
                        'label': 'blog/urls.py',
                        'code': 'from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path(\'\', views.home, name=\'home\'),\n    path(\'about/\', views.about, name=\'about\'),\n    path(\'post/<int:id>/\', views.post_detail, name=\'post_detail\'),\n]'
                    },
                    {
                        'label': 'myproject/urls.py',
                        'code': 'from django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    path(\'admin/\', admin.site.urls),\n    path(\'blog/\', include(\'blog.urls\')),\n]'
                    }
                ],
                'labs': [
                    '/about/ nu oru URL create panni, adha "about" nu peru vachi kudunga.',
                    '<int:id> mari dynamic URL oru create pannunga — /post/5/ type panna adhukana view trigger aaganum.',
                    'Project level urls.py la include() use panni blog app oda urls.py link pannunga.'
                ]
            },
            {
                'id': 'views',
                'title': 'Views (Function Based)',
                'explain': [
                    'View nu solradhu oru simple Python function (or class) — idhu request eduthukittu, response return pannum. "Logic" ellam idha vachu than nadakkum.',
                    'Function based view eppovum request nu oru parameter eduthukum. Adhula user pathina data (GET, POST) ellam irukum.',
                    'HttpResponse use panni direct ah text/html return pannalam, illana render() use panni oru template file ku data kudukalam — real project la render() thaan romba use pannuvom.'
                ],
                'examples': [
                    {
                        'label': 'blog/views.py',
                        'code': 'from django.http import HttpResponse\nfrom django.shortcuts import render\n\ndef home(request):\n    return HttpResponse("Welcome to my blog!")\n\ndef about(request):\n    context = {\'team_size\': 5, \'year\': 2026}\n    return render(request, \'blog/about.html\', context)\n\ndef post_detail(request, id):\n    return HttpResponse(f"Post number {id} details here")'
                    }
                ],
                'labs': [
                    'HttpResponse use panni "Hello Django" nu return panra oru view eludhunga.',
                    'URL la irundhu oru number eduthukura view eludhi, adha response la show pannunga (example: post_detail).',
                    'render() use panni oru simple template ku "team_size" nu oru value pass pannunga.'
                ]
            }
        ]
    },
    {
        'level': 'beginner',
        'name': 'Templates & Static',
        'topics': [
            {
                'id': 'templates',
                'title': 'Templates & DTL',
                'explain': [
                    'Django Template Language (DTL) na — HTML file kulla Python madhiri chinna logic eludhradhuku use pannum syntax. Idhula 2 mukkiyamana things — variables ({{ }}) matrum tags ({% %}).',
                    '{{ variable }} use panni namma view la irundhu anupina data ah HTML la show pannalam. {% if %}, {% for %} mari tags use panni conditions and loops podalam.',
                    'Template Inheritance na — oru base.html file eludhi, adhula common structure (header, footer) vachikittu, veru veru pages andha base.html file extend pannikalam. Ipadi pannina, ovvoru page layout ah repeat pannanum nu theva illa.'
                ],
                'examples': [
                    {
                        'label': 'templates/base.html',
                        'code': '<!DOCTYPE html>\n<html>\n<head><title>{% block title %}My Site{% endblock %}</title></head>\n<body>\n  <header>My Blog</header>\n  {% block content %}{% endblock %}\n  <footer>&copy; 2026</footer>\n</body>\n</html>'
                    },
                    {
                        'label': 'templates/blog/about.html',
                        'code': '{% extends \'base.html\' %}\n{% block title %}About Us{% endblock %}\n{% block content %}\n  <h1>Team size: {{ team_size }}</h1>\n  <ul>\n  {% for i in "12345" %}\n    <li>Member {{ forloop.counter }}</li>\n  {% endfor %}\n  </ul>\n{% endblock %}'
                    }
                ],
                'labs': [
                    'base.html oru file create panni, adhula {% block content %} vachukonga.',
                    'Vera oru template la extends use panni base.html inherit pannunga.',
                    '{% for %} loop use panni, view la irundhu anupina list ah HTML la display pannunga.'
                ]
            },
            {
                'id': 'static-media',
                'title': 'Static Files & Media',
                'explain': [
                    'CSS, JavaScript, images mari maaraadha files ah static files nu solvom. User upload panra files (profile photo mari) ah media files nu solvom.',
                    'settings.py la STATIC_URL define pannanum, and template la {% load static %} podanum. Apparam {% static \'path/to/file.css\' %} vachu link pannalam.',
                    'Media files ku MEDIA_URL and MEDIA_ROOT settings venum, and development la idha serve panna urls.py la oru chinna extra line venum.'
                ],
                'examples': [
                    {
                        'label': 'settings.py',
                        'code': 'STATIC_URL = \'static/\'\nSTATICFILES_DIRS = [BASE_DIR / "static"]\n\nMEDIA_URL = \'media/\'\nMEDIA_ROOT = BASE_DIR / "media"'
                    },
                    {
                        'label': 'template.html',
                        'code': '{% load static %}\n<link rel="stylesheet" href="{% static \'css/style.css\' %}">\n<img src="{% static \'images/logo.png\' %}" alt="logo">'
                    }
                ],
                'labs': [
                    'static folder create panni, adhula oru style.css podunga.',
                    'Andha CSS file ah oru template la {% static %} vachi link pannunga.',
                    'MEDIA_URL and MEDIA_ROOT settings.py la add pannunga.'
                ]
            }
        ]
    },
    {
        'level': 'beginner',
        'name': 'Data & Admin',
        'topics': [
            {
                'id': 'models',
                'title': 'Models & Migrations',
                'explain': [
                    'Model nu solradhu — unga database table ah Python class ah represent panradhu. Ovvoru class attribute um, table la oru column ah maarum. Idhu than Django ORM oda magic.',
                    'Model eludhina odhane database la table create aagadhu — mudhalla makemigrations run pannanum (idhu oru plan file create pannum), apparam migrate run pannanum (idhu andha plan ah actual ah database la apply pannum).',
                    'CharField, IntegerField, TextField, ForeignKey mari palavidhamana field types Django kudukum, ovvondrukum vera vera use case.'
                ],
                'examples': [
                    {
                        'label': 'blog/models.py',
                        'code': 'from django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()\n    published_on = models.DateTimeField(auto_now_add=True)\n    is_published = models.BooleanField(default=False)\n\n    def __str__(self):\n        return self.title'
                    },
                    {
                        'label': 'terminal',
                        'code': 'python manage.py makemigrations\npython manage.py migrate'
                    }
                ],
                'labs': [
                    'title, content, published_on fields vacha oru "Post" model eludhunga.',
                    'makemigrations and migrate run panni, database la table create pannunga.',
                    'python manage.py shell open panni, oru Post object create panni save pannunga.'
                ]
            },
            {
                'id': 'admin',
                'title': 'Django Admin',
                'explain': [
                    'Django oda romba periya sirappu enna na — free ah oru ready-made admin panel tharum. Idhu vachu database la data ah easy ah add/edit/delete pannalam, extra UI eludhama.',
                    'Superuser account create panradhukum, admin panel access panradhukum mudhalla createsuperuser command run pannanum.',
                    'Namma model ah admin panel la kaatanumna, admin.py file la register pannanum. list_display, search_fields mari options vachu, admin panel ah customize kooda pannalam.'
                ],
                'examples': [
                    {
                        'label': 'terminal',
                        'code': 'python manage.py createsuperuser'
                    },
                    {
                        'label': 'blog/admin.py',
                        'code': 'from django.contrib import admin\nfrom .models import Post\n\n@admin.register(Post)\nclass PostAdmin(admin.ModelAdmin):\n    list_display = (\'title\', \'is_published\', \'published_on\')\n    search_fields = (\'title\',)\n    list_filter = (\'is_published\',)'
                    }
                ],
                'labs': [
                    'Oru superuser account create pannunga.',
                    '/admin/ open panni login pannunga.',
                    'Post model ah admin.py la register panni, list_display use panni columns show pannunga.'
                ]
            }
        ]
    },
    {
        'level': 'intermediate',
        'name': 'ORM & Forms',
        'topics': [
            {
                'id': 'queryset',
                'title': 'QuerySets & ORM',
                'explain': [
                    'QuerySet nu solradhu — database la irundhu data eduthukura oru Python way. SQL query direct ah eludhama, Python methods use panni data fetch pannalam.',
                    '.all() ella records um eduthukum, .filter() condition match aana records mattum eduthukum, .get() single record eduthukum (illana error tharum), .exclude() opposite ah filter pannum.',
                    'QuerySets lazy — nee actual ah data ah use panra varaikkum (loop pannradhu, print pannradhu), database ku query pogadhu. Idhu performance ku romba nallathu.'
                ],
                'examples': [
                    {
                        'label': 'shell / views.py',
                        'code': 'from blog.models import Post\n\n# ella posts um\nPost.objects.all()\n\n# published posts mattum\nPost.objects.filter(is_published=True)\n\n# oru single post\nPost.objects.get(id=1)\n\n# title la \'django\' irukura posts\nPost.objects.filter(title__icontains=\'django\')\n\n# order pannradhu\nPost.objects.order_by(\'-published_on\')'
                    }
                ],
                'labs': [
                    'Ella published posts ah um fetch pannra query eludhunga.',
                    'title la specific keyword irukura posts ah filter pannunga.',
                    'published_on based ah latest post mudhalla varura madhiri order_by use pannunga.'
                ]
            },
            {
                'id': 'forms',
                'title': 'Forms & ModelForms',
                'explain': [
                    'Forms nu solradhu user input ah safe ah handle panna Django kudukura tool. Manually HTML form eludhi, validation eludhradhuku bathila, Django Form class use pannalam.',
                    'ModelForm na, unga model ah base ah vachi automatic ah oru form create aagum — fields ellam automatic ah varum, validation um automatic ah nadakkum.',
                    'Form submit aana odhane, form.is_valid() check pannanum. Valid ah irundha, form.save() vachu database la direct ah save pannalam.'
                ],
                'examples': [
                    {
                        'label': 'blog/forms.py',
                        'code': 'from django import forms\nfrom .models import Post\n\nclass PostForm(forms.ModelForm):\n    class Meta:\n        model = Post\n        fields = [\'title\', \'content\', \'is_published\']'
                    },
                    {
                        'label': 'blog/views.py',
                        'code': 'def create_post(request):\n    if request.method == \'POST\':\n        form = PostForm(request.POST)\n        if form.is_valid():\n            form.save()\n            return redirect(\'home\')\n    else:\n        form = PostForm()\n    return render(request, \'blog/create_post.html\', {\'form\': form})'
                    }
                ],
                'labs': [
                    'Post model ku oru ModelForm create pannunga.',
                    'GET request la empty form kaatti, POST request la save panra view eludhunga.',
                    'Template la {{ form.as_p }} use panni form ah render pannunga.'
                ]
            }
        ]
    },
    {
        'level': 'intermediate',
        'name': 'Users & Views',
        'topics': [
            {
                'id': 'auth',
                'title': 'Authentication',
                'explain': [
                    'Django kitta already ready ah built-in authentication system irukku — login, logout, password handling ellam idhula irukum, namma scratch la eludha vendam.',
                    'authenticate() function username/password check pannum, login() function session create pannum. logout() session ah clear pannidum.',
                    '@login_required decorator vacha, login pannama andha page ah access panna mudiyadhu — automatic ah login page ku redirect aagum.'
                ],
                'examples': [
                    {
                        'label': 'blog/views.py',
                        'code': 'from django.contrib.auth import authenticate, login, logout\nfrom django.contrib.auth.decorators import login_required\n\ndef login_view(request):\n    if request.method == \'POST\':\n        username = request.POST[\'username\']\n        password = request.POST[\'password\']\n        user = authenticate(request, username=username, password=password)\n        if user is not None:\n            login(request, user)\n            return redirect(\'home\')\n    return render(request, \'blog/login.html\')\n\n@login_required\ndef dashboard(request):\n    return render(request, \'blog/dashboard.html\')'
                    }
                ],
                'labs': [
                    'Oru simple login view eludhunga (form la irundhu username/password eduthukum).',
                    '@login_required use panni oru protected page create pannunga.',
                    'Logout button add panni, click pannumbodhu logout() call aagum madhiri pannunga.'
                ]
            },
            {
                'id': 'cbv',
                'title': 'Class-Based Views',
                'explain': [
                    'Function based views nallathu, aana same pattern (list kaatradhu, detail kaatradhu, create pannradhu) repeat ah eludha vendaam nu Django Class-Based Views (CBV) kudukudhu.',
                    'ListView automatic ah ella objects ah um kaatum, DetailView single object kaatum, CreateView/UpdateView/DeleteView form handling ah automatic ah pannikum.',
                    'CBV use panradhaala code romba kuraiyum, aana idhu eppadi work aagudhu nu internally puriyanumna, mudhalla function based views la nalla practice pannanum.'
                ],
                'examples': [
                    {
                        'label': 'blog/views.py',
                        'code': 'from django.views.generic import ListView, DetailView, CreateView\nfrom .models import Post\n\nclass PostListView(ListView):\n    model = Post\n    template_name = \'blog/post_list.html\'\n    context_object_name = \'posts\'\n\nclass PostDetailView(DetailView):\n    model = Post\n    template_name = \'blog/post_detail.html\'\n\nclass PostCreateView(CreateView):\n    model = Post\n    fields = [\'title\', \'content\', \'is_published\']\n    template_name = \'blog/post_form.html\'\n    success_url = \'/\''
                    },
                    {
                        'label': 'blog/urls.py',
                        'code': 'from .views import PostListView, PostDetailView\n\nurlpatterns = [\n    path(\'\', PostListView.as_view(), name=\'home\'),\n    path(\'post/<int:pk>/\', PostDetailView.as_view(), name=\'post_detail\'),\n]'
                    }
                ],
                'labs': [
                    'Post model ku ListView create panni, ella posts um kaattunga.',
                    'Adhe model ku DetailView create panni, single post kaattunga.',
                    'CreateView use panni, form illama new post add panna oru page pannunga.'
                ]
            }
        ]
    },
    {
        'level': 'advanced',
        'name': 'API & Beyond',
        'topics': [
            {
                'id': 'drf',
                'title': 'Django REST Framework',
                'explain': [
                    'Namma app oda data ah, vera app (mobile app, React frontend) kooda share pannanumna, HTML bathila JSON format la data kudukanum. Idhukku thaan Django REST Framework (DRF) use pannuvom.',
                    'Serializer na — model data ah JSON ah convert pannradhu (and JSON ah thirumba model data ah convert pannradhu). Model Form mari than, aana API ku.',
                    'APIView class use panni, GET/POST/PUT/DELETE ku vera vera logic eludhalam — idhu than REST API oda base.'
                ],
                'examples': [
                    {
                        'label': 'terminal',
                        'code': 'pip install djangorestframework'
                    },
                    {
                        'label': 'blog/serializers.py',
                        'code': 'from rest_framework import serializers\nfrom .models import Post\n\nclass PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = [\'id\', \'title\', \'content\', \'is_published\']'
                    },
                    {
                        'label': 'blog/views.py',
                        'code': 'from rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom .models import Post\nfrom .serializers import PostSerializer\n\nclass PostListAPI(APIView):\n    def get(self, request):\n        posts = Post.objects.all()\n        serializer = PostSerializer(posts, many=True)\n        return Response(serializer.data)'
                    }
                ],
                'labs': [
                    'djangorestframework install pannunga.',
                    'Post model ku oru serializer create pannunga.',
                    'GET request ku ella posts ah um JSON ah return panra APIView eludhunga.'
                ]
            },
            {
                'id': 'signals',
                'title': 'Signals',
                'explain': [
                    'Signals na — oru event nadakkumbodhu (example: model save aagumbodhu), automatic ah vera oru function trigger aaganumna use pannuvom.',
                    'post_save signal na — object save aana odhane trigger aagum. pre_save na, save aagara mudhalla trigger aagum.',
                    'Example: user register aana odhane automatic ah oru Profile object create panna, post_save signal use pannalam — views.py la extra code eludha vendam.'
                ],
                'examples': [
                    {
                        'label': 'blog/signals.py',
                        'code': 'from django.db.models.signals import post_save\nfrom django.dispatch import receiver\nfrom django.contrib.auth.models import User\nfrom .models import Profile\n\n@receiver(post_save, sender=User)\ndef create_profile(sender, instance, created, **kwargs):\n    if created:\n        Profile.objects.create(user=instance)'
                    },
                    {
                        'label': 'blog/apps.py',
                        'code': 'from django.apps import AppConfig\n\nclass BlogConfig(AppConfig):\n    name = \'blog\'\n    def ready(self):\n        import blog.signals'
                    }
                ],
                'labs': [
                    'User model ku oru Profile model create pannunga (OneToOneField vachu).',
                    'post_save signal use panni, User create aana odhane Profile automatic ah create aagura madhiri pannunga.',
                    'apps.py la ready() method use panni signal ah register pannunga.'
                ]
            },
            {
                'id': 'deployment',
                'title': 'Deployment Basics',
                'explain': [
                    'Development la DEBUG = True vachi velai pannuvom, aana live server la DEBUG = False pannanum — illana security risk.',
                    'ALLOWED_HOSTS la unga domain name add pannanum, illana Django request ah reject pannidum.',
                    'Live server la static files ah serve panna collectstatic command run pannanum, and Django\'s default server ku bathila gunicorn mari production server use pannanum.'
                ],
                'examples': [
                    {
                        'label': 'settings.py (production)',
                        'code': 'DEBUG = False\nALLOWED_HOSTS = [\'yourdomain.com\', \'www.yourdomain.com\']\n\nSTATIC_ROOT = BASE_DIR / \'staticfiles\''
                    },
                    {
                        'label': 'terminal',
                        'code': 'pip install gunicorn\npython manage.py collectstatic\ngunicorn myproject.wsgi:application'
                    }
                ],
                'labs': [
                    'settings.py la DEBUG = False panni, ALLOWED_HOSTS add pannunga.',
                    'collectstatic command run panni, staticfiles folder eppadi create aagudhu nu paarunga.',
                    'gunicorn install panni, adha vachi server start pannunga.'
                ]
            }
        ]
    }
]


class Command(BaseCommand):
    help = 'Seeds complete Django curriculum, modules, topics, examples, and practice labs from syllabus'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding default Staff and Student users..."))

        # 1. Staff / Super Admin User
        staff_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@skillstack.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'role': 'STAFF',
                'is_staff': True,
                'is_superuser': True,
                'is_admin_role': True
            }
        )
        staff_user.set_password('0912')
        staff_user.email = 'admin@skillstack.com'
        staff_user.role = 'STAFF'
        staff_user.is_staff = True
        staff_user.is_superuser = True
        staff_user.is_admin_role = True
        staff_user.save()
        self.stdout.write(self.style.SUCCESS(f"Super Admin User: {staff_user.username} / {staff_user.email} (Password: 0912)"))

        # Also update staff legacy user if existing
        legacy_staff = User.objects.filter(username='staff').first()
        if legacy_staff:
            legacy_staff.set_password('0912')
            legacy_staff.email = 'admin@skillstack.com'
            legacy_staff.save()

        # 2. Student User
        student_user, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@djangokalari.com',
                'first_name': 'Tamil',
                'last_name': 'Learner',
                'role': 'STUDENT',
                'batch_name': 'Batch Alpha',
            }
        )
        student_user.set_password('Student@12345')
        student_user.role = 'STUDENT'
        student_user.save()
        self.stdout.write(self.style.SUCCESS(f"Student User: {student_user.username} (Password: Student@12345)"))

        # 3. Curriculum Data
        self.stdout.write(self.style.NOTICE("Seeding modules, topics, and problem labs..."))

        now = timezone.now()
        unlocked_first_n = 3  # Unlock first 3 labs for immediate active testing!

        total_problems = 0
        for mod_idx, m_data in enumerate(RAW_MODULES, start=1):
            module, _ = Module.objects.get_or_create(
                name=m_data['name'],
                defaults={
                    'level': m_data['level'],
                    'order': mod_idx
                }
            )

            for top_idx, t_data in enumerate(m_data['topics'], start=1):
                topic, _ = Topic.objects.get_or_create(
                    topic_id=t_data['id'],
                    defaults={
                        'module': module,
                        'title': t_data['title'],
                        'explain': t_data['explain'],
                        'order': top_idx
                    }
                )

                # Examples
                for ex_idx, ex in enumerate(t_data['examples'], start=1):
                    CodeExample.objects.get_or_create(
                        topic=topic,
                        label=ex['label'],
                        defaults={
                            'code': ex['code'],
                            'order': ex_idx
                        }
                    )

                # Labs / Problems
                for lab_idx, lab_text in enumerate(t_data['labs'], start=1):
                    total_problems += 1
                    problem, _ = Problem.objects.get_or_create(
                        topic=topic,
                        order=lab_idx,
                        defaults={
                            'title': f"Task #{lab_idx}: {t_data['title']}",
                            'description': lab_text,
                            'points': 10,
                            'expected_output_hint': "Enter your terminal command output or code implementation."
                        }
                    )

                    # Problem Access
                    access, _ = ProblemAccess.objects.get_or_create(problem=problem)
                    if total_problems <= unlocked_first_n:
                        # Unlock first 3 labs with a 24-hour deadline for live testing
                        access.is_unlocked = True
                        access.unlocked_at = now
                        access.deadline = now + timedelta(hours=24)
                        access.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded curriculum with {total_problems} problems across {len(RAW_MODULES)} modules!"))
