import time
from django.core.management.base import BaseCommand
from db.models import Org, Org_log, DB_RECREATE, DB_READY, DB_VERSION
from db.rawmodel import RawModel


class Command(BaseCommand):
    help = 'Organization manipulation'

    def add_arguments(self, parser):
        parser.add_argument('command', action="store", nargs='*', help='Use [ list | create | updateall ]')
        parser.add_argument('--verbose',action='store_true', dest='verbose', default=False, help='Set verbosity level for books collection scan.')
        parser.add_argument('--nogenres',action='store_true', dest='nogenres', default=False, help='Not install genres fom fixtures.')

    def handle(self, *args, **options):
        action = options['command'][0]

        if action=='list':
            self.stdout.write('List Organizations registered with ID.')
            self.list()
        elif action == 'create':
            self.stdout.write('Create organization database.')
            org_id = options['command'][1] if len(options['command'])>1 else None
            self.create_tables(org_id)
        elif action == 'updateall':
            self.stdout.write('Recreate all organization database.')
            self.updateAll()

    def list(self):
        print('{:<30} {:>6}'.format('Name', 'ID'))
        for o in Org.objects.all():
            print('{:<30} {:>6}'.format(o.name, o.id))

    def create_tables(self, org_id):
        if not org_id:
            return
        org=Org.objects.get(id=org_id)

        if org.sync_status != DB_READY:
            msg = 'Start recreate impossible (DB not READY) for "{}".'.format(org.name)
            Org_log.objects.create(org_id=org_id,description=msg)
            self.stdout.write(msg)
            return

        org.sync_flag = False
        org.save()
        self.stdout.write('ReCreate database for "{}".'.format(org.name))
        Org_log.objects.create(org_id=org_id, description='{}. Start DB Recreating'.format(org.name))
        startTime = time.time()
        self.stdout.write('Drop all tables...')
        RawModel('drop_org.sql').filter(org_id=org.id).exec().close()
        self.stdout.write('Create org_CACHE_{} table...'.format(org.id))
        RawModel('create_org.sql').filter(org_id=org.id).exec().close()
        self.stdout.write('Create org_DOSAGE_{} table...'.format(org.id))
        RawModel('create_dosage.sql').filter(org_id=org.id).exec().close()
        self.stdout.write('Create org_FORM_{} table...'.format(org.id))
        RawModel('create_form.sql').filter(org_id=org.id, db_version = DB_VERSION).exec().close()
        totalTime = int(time.time() - startTime)
        self.stdout.write("Elapsed time: {:0=2}:{:0=2}".format(totalTime//60, totalTime%60))
        Org_log.objects.create(org_id=org_id, description='{}. Finish DB Recreating. Elapsed time: {:0=2}:{:0=2}'.format(org.name, totalTime//60, totalTime%60))

    def updateAll(self):
        for org in Org.objects.filter(sync_flag=True):
            self.create_tables(org.id)