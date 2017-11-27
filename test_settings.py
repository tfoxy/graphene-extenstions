SECRET_KEY = True
DEBUG = True

INSTALLED_APPS = [
    'graphene_extensions',

    # demo apps
    'examples',
    'examples.restaurants',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

ROOT_URLCONF = 'examples.urls'
