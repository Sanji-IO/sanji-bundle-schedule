#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt
from schedule import Schedule

logger = logging.getLogger()


class Index(Sanji):
    '''Schedule bundle RESTful API endpoints'''

    def init(self, *args, **kwargs):
        self.schedule = Schedule()

    @Route(methods="get", resource="/system/schedule")
    def get_all_schedule(self, message, response):
        return response(data=self.schedule.get())

    @Route(methods="get", resource="/system/schedule/:id")
    def get_one_schedule(self, message, response):
        return response(data=self.schedule.get(id=message.param["id"]))

    @Route(methods="put", resource="/system/schedule/:id")
    def update_one_schedule(self, message, response):
        data = dict({"id": int(message.param["id"])}.items() +
                    message.data.items())
        upadte = self.schedule.update(data)

        return response(data=upadte)

    @Route(methods="put", resource="/system/schedule")
    def update_multi_schedule(self, message, response):
        update = []
        for job in message.data:
            update.append(self.schedule.update(job))

        return response(data=update)


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Schedule")
    schedule = Index(connection=Mqtt())
    schedule.start()
