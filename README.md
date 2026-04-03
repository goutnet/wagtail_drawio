# wagtail-drawio

A [Wagtail](https://wagtail.org/) plugin that brings [draw.io](https://www.drawio.com/) diagrams natively into your CMS — create, edit, and embed diagrams without leaving Wagtail.

## Features

- **Dedicated diagram library** — diagrams are first-class Wagtail snippets, managed from a dedicated *Drawio* menu in the admin sidebar. Create, rename, tag, and browse all your diagrams in one place.
- **In-place draw.io editor** — double-click the diagram thumbnail inside the admin edit form to open the full draw.io editor in an iframe. Save sends the updated PNG (with embedded XML) back to Wagtail without a page reload.
- **StreamField block** — `DrawIOImageChooserBlock` lets page authors pick any diagram from the library and embed it in any `StreamField`. Updating the diagram in the library automatically updates every page that references it.
- **Safe rendering** — diagrams are served as clean PNGs via a dedicated view (`/drawio/drawio-image/<pk>/`). The raw XML embedded in the PNG is stripped server-side before delivery, so diagram source is never exposed to end users.
- **Usage tracking** — when `WAGTAIL_USAGE_COUNT_ENABLED = True`, each diagram shows a *Used on* panel listing every page or object that references it, with direct links to their edit views.
- **Tagging** — diagrams support Wagtail's standard tagging via `django-taggit`.
- **Configurable draw.io URL** — point the editor at a self-hosted draw.io instance or customise the query string via Django settings.
- **Custom draw.io icon** — the draw.io logo is registered as a Wagtail icon and used throughout the admin interface.

## Requirements

- Python >= 3.10
- Django >= 5.1
- Wagtail >= 6.1
- `pypng`

## Installation

Install from PyPI:

```shell
pip install wagtail_drawio
```

Or directly from GitHub:

```shell
pip install git+https://github.com/goutnet/wagtail-drawio.git
```

Add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_drawio",
]
```

Run migrations:

```shell
./manage.py migrate wagtail_drawio
```

## Usage

### StreamField block

```python
from wagtail_drawio.blocks import DrawIOImageChooserBlock

class BlogPage(Page):
    body = StreamField(
        [
            # ...
            ("diagram", DrawIOImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )
```

### Managing diagrams

Diagrams are managed from the **Drawio** entry in the Wagtail sidebar. Create a new diagram there, then double-click the thumbnail to open the draw.io editor.

### Usage tracking

```python
# settings.py
WAGTAIL_USAGE_COUNT_ENABLED = True
```

On an existing project, backfill the reference index once:

```shell
./manage.py rebuild_references_index
```

### Custom draw.io server

```python
# settings.py
WAGTAIL_DRAWIO_URL = "https://embed.diagrams.net"   # default
WAGTAIL_DRAWIO_QUERY_STRING = "ui=atlas&spin=1"     # default
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Building locally

```shell
make dist
```

Output goes to `out/`. See `make help` for all available targets.

## License

This project is distributed under the [MIT License](LICENSE).

Copyright (C) 2023-2026 Florian Delizy

The draw.io logo (`wagtail_drawio/static/admin/media/drawio.svg`) is copyright JGraph Ltd and distributed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
