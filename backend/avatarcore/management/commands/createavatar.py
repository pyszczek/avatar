from django.core.management.base import BaseCommand, CommandError

from avatarauth import services


class Command(BaseCommand):
    help = 'Creates new avatars'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, default=1, help='Number of avatars to create')

    def handle(self, *args, **options):
        for i in range(options['number']):
            try:
                avatar = services.create_avatar()
            except Exception as err:
                raise CommandError(f'Something went wrong. Details: {err}')

            self.stdout.write(self.style.SUCCESS(f'[{avatar.id}] Avatar {avatar.uuid} successfully created'))
