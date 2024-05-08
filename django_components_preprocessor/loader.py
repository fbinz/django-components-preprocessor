import re

from django.template.loaders.base import Loader as BaseLoader
from django_components.component_registry import registry


class Loader(BaseLoader):
    """A template loader that preprocesses element tags to component tags."""

    def __init__(self, engine, loader):
        self.loader = engine.find_template_loader(loader)

        # Monkey-patch the loader to replace component tags with template tags
        self.loader_get_contents = self.loader.get_contents
        self.loader.get_contents = self.get_contents

        # Prepare regular expressions for replacing tags
        self.component_names = "|".join(registry.all().keys())
        self.self_closing_tag_re = re.compile(f"<({self.component_names})([^>]*)/>")
        self.opening_tag_re = re.compile(f"<({self.component_names})([^>]*)>")
        self.closing_tag_re = re.compile(f"</({self.component_names})\s*>")

        super().__init__(engine)

    @staticmethod
    def replace_self_closing_tag(match):
        tag = match.group(1)
        args = match.group(2).replace("\n", " ")
        return f'{{% component "{tag}"{args} %}}{{% endcomponent %}}'

    @staticmethod
    def replace_opening_tag(match):
        tag = match.group(1)
        args = match.group(2).replace("\n", " ")
        return f'{{% component "{tag}"{args} %}}'

    @staticmethod
    def replace_closing_tag(match):
        return "{% endcomponent %}"

    def get_contents(self, origin):
        contents = self.loader_get_contents(origin)

        contents = self.self_closing_tag_re.sub(self.replace_self_closing_tag, contents)
        contents = self.opening_tag_re.sub(self.replace_opening_tag, contents)
        contents = self.closing_tag_re.sub(self.replace_closing_tag, contents)

        return contents

    # Forward all other methods to the original loader
    def get_template(self, template_name, skip=None):
        template = self.loader.get_template(template_name, skip)
        return template

    def get_template_sources(self, template_name):
        return self.loader.get_template_sources(template_name)

    def reset(self):
        return self.loader.reset()
