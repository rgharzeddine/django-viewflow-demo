import inspect
import os

from django.core.management.base import BaseCommand

from viewflow import flow
from viewflow.base import Flow

from demo.example import flows
from flowutils import activities


TEMPLATE = """\
digraph {{


    label="{label}"

    {definition}


    {routes}

}}
"""


class Command(BaseCommand):
    help = 'Visualise a viewflow process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            dest='show_list',
            help='List available Workflows',
        )

        parser.add_argument('process', type=str, nargs='?', default=None)

    def show_list(self, *args, **options):
        for key, value in inspect.getmembers(flows):
            if (value is not Flow
                    and inspect.isclass(value)
                    and Flow in value.__mro__):
                self.stdout.write(f'{key}: {value.process_description}')

    def handle(self, *args, **options):
        klass = None
        process = options['process']

        if options['show_list']:
            self.show_list(*args, **options)
            return

        try:
            klass = getattr(flows, process)
        except (AttributeError, TypeError):
            self.stdout.write(f'please specify a valid workflow class') 
            return

        mapping = []
        routes = []
        definition = set()

        fields = {id(v): k for k, v in klass.__dict__.items()}

        for name, value in klass.__dict__.items():

            if isinstance(value, flow.Split):
                for task in value._activate_next:
                    mapping.append((name, 'diamond', fields[id(task[0])]))
            elif isinstance(value, flow.Join):
                mapping.append((name, 'circle', fields[id(value._next)]))
            elif isinstance(value, flow.Start):
                mapping.append((name, 'circle', fields[id(value._next)]))
            elif isinstance(value, flow.View):
                mapping.append((name, 'box', fields[id(value._next)]))
            elif isinstance(value, activities.Job):
                mapping.append((name, 'box', fields[id(value._next)]))
            elif isinstance(value, flow.If):
                mapping.append((name, 'diamond', fields[id(value._on_true)]))
                mapping.append((name, 'diamond', fields[id(value._on_false)]))
            elif isinstance(value, flow.End):
                mapping.append((name, 'circle', None))
            else:
                self.stdout.write(f'> Unhandled: {value}')

        for src, _type, dst in mapping:
            definition.add(f'{src} [shape = {_type}];')

            if dst is not None:
                routes.append(f'{src} -> {dst};')

        digraph = TEMPLATE.format(
            label=klass.process_description, 
            definition='\n'.join(definition),
            routes='\n'.join(routes))

        with open(f'{process}.dot', 'w') as dotfile:
            dotfile.write(digraph)

        os.system(f'dot -Tsvg -o {process}.svg {process}.dot')
