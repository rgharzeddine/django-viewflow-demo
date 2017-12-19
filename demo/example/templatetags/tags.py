from django import template
register = template.Library()


@register.simple_tag
def get_task_url(task):
    application = 'example'
    label = task.process.flow_class.flow_label

    if task.status.lower() == 'done':
        return '/{}/{}/{}/{}/{}/detail'.format(
            application,
            label,
            task.process_id,
            str(task.flow_task).lower(),
            task.id,
        )

    if not task.owner:
        return '/{}/{}/{}/{}/{}/assign'.format(
            application,
            label,
            task.process_id,
            str(task.flow_task).lower(),
            task.id,
        )

    return '/{}/{}/{}/{}/{}'.format(
        application,
        label,
        task.process_id,
        str(task.flow_task).lower(),
        task.id,
    )
