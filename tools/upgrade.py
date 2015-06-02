#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from sanji.core import Sanji
from sanji.connection.mqtt import Mqtt


class View(Sanji):

    # This function will be executed after registered.
    def run(self):

        # Normal CRUD Operation
        #   self.publish.[get, put, delete, post](...)
        # One-to-One Messaging
        #   self.publish.direct.[get, put, delete, post](...)
        #   (if block=True return Message, else return mqtt mid number)
        # Agruments
        #   (resource[, data=None, block=True, timeout=60])

        # get if upgrade required
        resource = "/system/firmware/check"
        res = self.publish.get(resource)
        if res.code != 200:
            print res.to_json()
            _logger.debug(res.to_json())
            return self.stop()
        elif 1 == res.data["isLatest"]:
            print "MXcloud is up to date."
            _logger.info("MXcloud is up to date.")
            return self.stop()

        # upgrade
        resource = "/system/firmware"
        res = self.publish.put(resource, data={"upgrade": 1})
        if res.code != 200:
            print res.to_json()
            _logger.debug(res.to_json())
        else:
            print "Upgrading success."
            _logger.debug("Upgrading success.")

        # stop the test view
        self.stop()


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    _logger = logging.getLogger("sanji.schedule.upgrade")

    view = View(connection=Mqtt())
    view.start()
