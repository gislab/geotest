import csv
import os
from django.conf import settings
from django.core.management.base import CommandError
from django.utils.html import strip_tags
from django_tqdm import BaseCommand
from coordmanager.models import Coordinate
from coordmanager.forms import ImportCoordinate

class Command(BaseCommand):
    """
        import x,y point from CSV file into "coordinate" models:
        usage:

        ./manage.py import_coordinates <file_name>
    """

    help = "import x,y point from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV filename')

    def handle(self, *args, **options):
        updated_count = 0
        created_count = 0
        error_count = 0

        if getattr(settings, 'CSV_IMPORT_DIR', None) is not None:
            os.chdir(settings.CSV_IMPORT_DIR)

        if not os.path.isfile(options['csv_file']):
            raise CommandError("%s is not a file" % options['csv_file'])

        with open(options['csv_file']) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            row_count = sum(1 for row in csv_file) - 1
            csv_file.seek(0)

            if row_count == 0:
                self.stdout.write(self.style.WARNING('file %s is empty!' % options['csv_file']))
                exit()

            self.stdout.write(self.style.SUCCESS(
                'Successfully open file "%s", load %s coordinates' % (options['csv_file'], row_count)
            ))

            progress_bar = self.tqdm(total=int(row_count))

            for row_id, data in enumerate(csv_reader):
                import_form = ImportCoordinate(data)
                progress_bar.update(1)

                if not import_form.is_valid():
                    self.stderr.write('error on import data row number %s:' % row_id)
                    for error in import_form.errors.items():
                        self.stderr.write('field %s: %s' % (error[0], strip_tags(error[1])))
                    for error in import_form.non_field_errors():
                        self.stderr.write('non field error: %s' % strip_tags(error))
                    error_count += 1
                    continue

                _, created = Coordinate.objects.update_or_create(
                    id=import_form.cleaned_data['id'],
                    defaults={
                        'x': import_form.cleaned_data['x'],
                        'y': import_form.cleaned_data['y']
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            if created_count == 0 and updated_count == 0:
                self.stdout.write(self.style.WARNING('no point are imported'))
            else:
                self.stdout.write(self.style.SUCCESS('Successfully insert %s points' % created_count))
                self.stdout.write(self.style.SUCCESS('Successfully update %s points' % updated_count))
            if error_count > 0:
                self.stdout.write(self.style.ERROR('%s points are not imported' % error_count))
