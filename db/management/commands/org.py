from django.core.management.base import BaseCommand
from db.models import Org
from db.rawmodel import RawModel


class Command(BaseCommand):
    help = 'Organization manipulation'

    def add_arguments(self, parser):
        parser.add_argument('command', action="store", nargs='*', help='Use [ list | info | update ]')
        parser.add_argument('--verbose',action='store_true', dest='verbose', default=False, help='Set verbosity level for books collection scan.')
        parser.add_argument('--nogenres',action='store_true', dest='nogenres', default=False, help='Not install genres fom fixtures.')

    def handle(self, *args, **options):
        action = options['command'][0]

        if action=='list':
            self.list()
        elif action == 'create':
            org_id = options['command'][1] if len(options['command'])>1 else None
            self.create_tables(org_id)

    def list(self):
        self.stdout.write('List Organizations registered with ID.')
        print('{:<30} {:>6}'.format('Name', 'ID'))
        for o in Org.objects.all():
            print('{:<30} {:>6}'.format(o.name, o.id))

    def create_tables(self, org_id):
        self.stdout.write('Create organization database.')
        if org_id:
            org=Org.objects.get(id=org_id)
            self.stdout.write('Create database for "{}".'.format(org.name))