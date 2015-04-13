#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import logging
import subprocess

from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt
from sanji.model_initiator import ModelInitiator


logger = logging.getLogger()


class Index(Sanji):
    '''Schedule bundle RESTful API endpoints'''

    def init(self, *args, **kwargs):
        pass

    @Route(methods="get", resource="/system/schedule")
    def get_all_schedule(self, message, response):
        pass

    @Route(methods="post", resource="/system/schedule")
    def post_schedule(self, message, response):
        pass

    @Route(methods="get", resource="/system/schedule/:id")
    def get_one_schedule(self, message, response):
        pass

    @Route(methods="put", resource="/system/schedule/:id")
    def update_one_schedule(self, message, response):
        pass

    @Route(methods="delete", resource="/system/schedule/:id")
    def delete_one_schedule(self, message, response):
        pass

    def reboot(self):
        pass


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Schedule")

    schedule = Index(connection=Mqtt())
    schedule.start()
