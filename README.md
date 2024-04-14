# Wagtail DrawIO - A Wagtail plugin to embed DrawIO diagrams in Wagtail pages

## Overview

This plugin allows you to embed a DrawIO diagram straight into a page, just like you would with an image.

- In view mode, the diagram is shown as a PNG (not embedding the draw IO code)
- In edit mode, the diagram can be editted directly in place

## Build

For convenience a Makefile is included to build the python package

```
   make dist
```

## Testing it Out

```
    cd webroot
    ./manage runserver
```

## Installing Into a Project

Add the `wagtail_drawio` into your application in settings:

```python
    INSTALLED_APPS = [
        ...
        'wagtail_drawio',
    ]
```

Upgrade your database:

```shell
    ./manage.py migrate wagtail_drawio
```

Add the `DrawioBlock` into a `Page` or directly into a `StreamField/StreamBlock`, eg.:

```python
    from wagtail_drawio.blocks import DrawIOImageBlock

    class HomePage(Page):
        """Home page model"""

        body = fields.StreamField(
            [
                # ...
                ("drawio_diagram", DrawIOImageBlock()),
                # ...
            ],
            null=True,
            blank=True,
        )

```

Optionally, you can configure the DrawIO URL by adding the following to your `settings.py`

```python
    WAGTAIL_DRAWIO_URL = "https://embed.diagrams.net"
    WAGTAIL_DRAWIO_QUERY_STRING = "ui=atlas&spin=1"
```

(adjust as needed)

## Usage

### Creating a Diagram

Diagrams are managed directly from the main menu, check the 'Drawio` menu. Create a new Drawio model instance directly from there.

To Edit the diagram, directly double click on the image to bring the diagram editor.

### Using a diagram

Add a block to your page, and select the diagram from there.

### Using the Js Code

if you are only looking for a quick JS fix, have a look at `wagtail_drawio/static/js/drawio_widget.js`. This simple js class
can either be used with or without jQuery to transform an `&lt;img/&gt;` tag into an editor directly. Please check the
javascript code directly, the top section provides full usage guidelines.


## Project Status

While still green, this project is already usable as is, some
This project is at a very early stage, and will move along as I use it internally. Features to come:

* Filter diagrams by tags
* Better diagram chooser
* Edit diagram in place from the Block (t.b.d.)
