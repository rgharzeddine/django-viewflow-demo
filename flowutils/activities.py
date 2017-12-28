from django.utils.timezone import now
from viewflow import flow
from viewflow.activation import AbstractJobActivation, STATUS
from viewflow import signals
# from viewflow.decorators import flow_job
# from celery.decorators import task


class JobActivation(AbstractJobActivation):

    def run_async(self, *args, **kwargs):
        kw = self.get_kwargs()
        self.func.delay(**kw)
        self.done()

    def get_kwargs(self):
        path = '{}.{}'.format(
            self.flow_class.__module__, self.flow_class.__name__)
        app_label = '.'.join(path.split('.')[1:2])
        task_path = '.'.join(path.split('.')[2:]) + '.'
        task_path += str(self.flow_task).lower().replace(' ', '_')

        flow_task_strref = '{}/{}'.format(
            app_label,
            task_path,
        )
        print(flow_task_strref)
        return dict(
            flow_task_strref=flow_task_strref,
            process_pk=self.process.pk,
            task_pk=self.task.pk,
        )
    status = AbstractJobActivation.status

    @status.transition(source=STATUS.NEW, target=STATUS.DONE)
    def schedule(self):
        """Schedule task for execution."""
        # with self.exception_guard():
        self.run_async()
        self.task.finished = now()
        self.set_status(STATUS.DONE)
        self.task.save()
        signals.task_finished.send(
            sender=self.flow_class, process=self.process, task=self.task)
        self.activate_next()

    @status.transition(source=STATUS.DONE)
    def activate_next(self):
        super(JobActivation, self).activate_next()

    @classmethod
    def activate(cls, flow_task, prev_activation, token):
        """
        Activate and schedule for background job execution.

        It is safe to schedule job just now b/c the process instance is locked,
        and job will wait until this transaction completes.
        """
        flow_class, flow_task = flow_task.flow_class, flow_task
        process = prev_activation.process

        task = flow_class.task_class(
            process=process,
            flow_task=flow_task,
            token=token)

        task.save()
        task.previous.add(prev_activation.task)

        activation = cls()
        activation.initialize(flow_task, task)
        # activation.assign()
        activation.schedule()

        return activation

    def assign(self):
        pass

    def start(self):
        pass

    def restart(self):
        pass

    def done(self):
        pass

    def error(self, comments=""):
        pass

    def retry(self):
        pass

    def undo(self):
        pass

    def cancel(self):
        pass


class Job(flow.AbstractJob):
    activation_class = JobActivation

    def __init__(self, job, **kwargs):  # noqa D102
        super(Job, self).__init__(job)  # **kwargs)
        self.activation_class.func = job
        self._job = job

    @property
    def job(self):
        """Callable that should start the job in background."""
        return self._job
