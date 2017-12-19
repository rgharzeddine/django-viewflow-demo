from django.core.management.base import BaseCommand

from viewflow import flow

from demo.example.flows import VacationApprovalFlow

TEMPLATE = """\
digraph {{


    label="{label}"
    
    {definition}


    {routes}

}}
"""


class Command(BaseCommand):
    help = 'Visualise a viewflow process'		

    def handle(self, *args, **options):

        mapping = []
        routes = []
        definition = set()

        fields = { id(v): k for k, v in VacationApprovalFlow.__dict__.items() }

        for name, value in VacationApprovalFlow.__dict__.items():

            if isinstance(value, flow.Split):
                for task in value._activate_next:
                    mapping.append((name, 'diamond', fields[id(task[0])]))

            if isinstance(value, flow.Join):
                mapping.append((name, 'circle', fields[id(value._next)]))

            if isinstance(value, flow.Start):
                mapping.append((name, 'circle', fields[id(value._next)]))
                # mapping.append(('first', 'box', 

            if isinstance(value, flow.View):
                mapping.append((name, 'box', fields[id(value._next)]))

            if isinstance(value, flow.If):
                mapping.append((name, 'diamond', fields[id(value._on_true)]))
                mapping.append((name, 'diamond', fields[id(value._on_false)]))

            if isinstance(value, flow.End):
                mapping.append((name, 'circle', None))

        for src, _type, dst in mapping:
            definition.add(f'{src} [shape = {_type}];')

            if dst is not None:
                routes.append(f'{src} -> {dst};')


        self.stdout.write(TEMPLATE.format(
            label=VacationApprovalFlow.process_description, 
            definition='\n'.join(definition),
            routes='\n'.join(routes)
        ))
