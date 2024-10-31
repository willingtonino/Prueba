from django.core.management.base import BaseCommand
from django.urls import get_resolver


class Command(BaseCommand):
    help = 'Prints all valid Django URLs'

    def handle(self, *args, **options):
        resolver = get_resolver()
        self.print_urls(resolver)

    def print_urls(self, resolver, prefix=''):
        if hasattr(resolver, 'url_patterns'):
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    self.print_urls(pattern, prefix + str(pattern.pattern))
                else:
                    self.stdout.write(prefix + str(pattern.pattern))
