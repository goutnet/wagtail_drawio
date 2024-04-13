# Wagtail DrawIO - A Wagtail plugin to embed DrawIO diagrams in Wagtail pages

# Overview

This plugin allows you to embed a DrawIO diagram straight into a page, just like you would with an image.

- In view mode, the diagram is shown as a PNG (not embedding the draw IO code)
- In edit mode, the diagram can be editted directly in place

# Build

For convenience a Makefile is included to build the python package

```
   make dist
```

# Testing it Out

```
    cd webroot
    ./manage runserver
```

# Installing Into a Project

Add the `wagtail_drawio` into your application in settings:

```
    INSTALLED_APPS = [
        ...
        'wagtail_drawio',
    ]
```

Upgrade your database:

```
    ./manage.py migrate wagtail_drawio
```

Add the `DrawIOBlock` into a `Page` or directly into a `StreamBlock`
