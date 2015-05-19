#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt
from schedule import Schedule

from voluptuous import Schema
from voluptuous import Required
from voluptuous import REMOVE_EXTRA
from voluptuous import Range
from voluptuous import All
from voluptuous import Length


_logger = logging.getLogger("sanji.schedule")


class Index(Sanji):
    '''Schedule bundle RESTful API endpoints'''
    SCHEMA = Schema({
        Required("id"): All(int, Range(min=1, max=65535)),
        "enable": All(int, Range(min=0, max=1)),
        "alias": All(str, Length(1, 255)),
        "command": All(str, Length(1, 255)),
        "schedule": All(str, Length(1, 255)),
        "executer": All(str, Length(1, 255)),
    }, extra=REMOVE_EXTRA)

    SCHEMA_ARR = Schema([SCHEMA])

    def init(self, *args, **kwargs):
        self.schedule = Schedule()

    @Route(methods="get", resource="/system/schedule")
    def get_all_schedule(self, message, response):
        return response(data=self.schedule.get())

    @Route(methods="get", resource="/system/schedule/:id")
    def get_one_schedule(self, message, response):
        return response(data=self.schedule.get(id=message.param["id"]))

    @Route(methods="put", resource="/system/schedule/:id", schema=SCHEMA)
    def update_one_schedule(self, message, response):
        data = dict({"id": int(message.param["id"])}.items() +
                    message.data.items())
        upadte = self.schedule.update(data)

        return response(data=upadte)

    @Route(methods="put", resource="/system/schedule", schema=SCHEMA_ARR)
    def update_multi_schedule(self, message, response):
        update = []
        for job in message.data:
            update.append(self.schedule.update(job))

        return response(data=update)


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    _logger = logging.getLogger("sanji.schedule")
    schedule = Index(connection=Mqtt())
    schedule.start()
