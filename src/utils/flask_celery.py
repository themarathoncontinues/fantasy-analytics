from celery import Celery


def make_celery(app):
    """
    Instantiate celery.Celery async broker
    Args:
        app: (Flask) - app to broker messages for

    Returns:
         celery: (Celery)
    """
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """establish Flask application context (for call within Flask)"""

        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
