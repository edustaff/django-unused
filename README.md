# django-unused

[![Build Status](https://travis-ci.org/ticalcster/django-unused.svg?branch=master)](https://travis-ci.org/ticalcster/django-unused)

Lists all unused templates, views, or media in a Django project.

## Install / Setup ##
First install the package

    pip install django-unused

Add to Django `settings.py` file

```python
INSTALLED_APPS = (
    ...
    'django_unused',
    ...
)
```

## Usage ##

django-unused creates a management command `unused`.
The command has three basic sub commands: `templates`, `views`, and `media`

`unused templates`
: A semantic personal publishing platform


**templates**

    python manage.py unused templates

**views**

    python manage.py unused views

**media**

    python manage.py unused media

## Testing ##
Just run tox.

    tox

###### Upload to PyPI ######

Just to remind myself:

    python setup.py bdist_wheel --universal
    twine upload dist/*