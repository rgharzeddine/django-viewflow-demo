from django.utils.timezone import now
from viewflow import flow
from viewflow.activation import AbstractJobActivation, STATUS


class CeleryJobActivation(AbstractJobActivation):

    # status = AbstractJobActivation.status

    # @status.transition(
    #     source=[STATUS.STARTED, STATUS.ASSIGNED], target=STATUS.DONE)
    def done(self):
        """Cancel existing task."""
        self.task.finished = now()
        self.task.status = STATUS.DONE
        self.task.save()
        self.activate_next()


def _dummy(*args, **kwargs):
    pass


class CeleryJob(flow.AbstractJob):
    activation_class = CeleryJobActivation

    def __init__(self, **kwargs):  # noqa D102
        super(CeleryJob, self).__init__(_dummy, **kwargs)

    @property
    def job(self):
        """Callable that should start the job in background."""
        raise
        # return self._job
