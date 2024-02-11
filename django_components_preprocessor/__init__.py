"""A preprocessor for Django templates that replaces custom HTML tags with component tags."""

__version__ = "0.1.0"


def with_components_preprocessor(*loaders):
    return [
        ("django_components_preprocessor.loader.Loader", loader) for loader in loaders
    ]
