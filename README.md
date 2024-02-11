# django-components-preprocessor

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This project allows you to use regular HTML tags for your django-component components.

### Before

```
{% component_block "calendar" attr="value" %}
  {% component_block "header" %}
    Custom header
  {% endcomponent_block %}
{% encomponent_block %}
```

### After

```
<calendar attr="value">
  <header>
    Custom header
  </header>
</calendar>
```

## Installation

- Install the package using pip:

```bash
pip install django-components-preprocessor
```

- Import the `with_components_preprocessor` function and use it to wrap the `loaders` option in your `TEMPLATES` setting:

```python
# settings.py
from django_components_preprocessor import with_components_preprocessor
...

# Example TEMPLATES setting
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": with_components_preprocessor(
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django_components.template_loader.Loader",
            ),
            "builtins": [
                "django_components.templatetags.component_tags",
            ],
        },
    },
]
```

## How it works

Your templates will be preprocessed before being passed to the regular django template engine.
The preprocessor will replace custom tags (i.e. `<calendar />`) with the regular django-component tags
(i.e. `{% component "calendar" }`).
The tags are matched by name and are case-sensitive.

Currently, custom tags are found using regular expressions, which is obviously a bit whacky.
It does however work for most cases, and is a lot more readable than the regular django-component tags.
A more robust solution would be to use a proper HTML parser, but that's a bit overkill at this point in time.

If, due to the limitations of the regular expressions, you find that the preprocessor doesn't work for your use case,
you can always use the regular django-component tags as you normally would.

## License

This project is licensed under the [MIT License](LICENSE).
