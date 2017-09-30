# coding=utf-8
from __future__ import unicode_literals, absolute_import

from celery import Task

from clambda.worker import app
from clambda.model import LambdaFunction


class LambdaFunctionTask(Task):
    name = "clambda.LambdaFunctionTask"

    def run(self, task_id):
        obj = LambdaFunction.query().get(task_id)
        if obj is None:
            return
        # safety?
        exec(obj.code)
        # from execute
        execute()
        return true


app.register_task(LambdaFunctionTask())
