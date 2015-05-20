#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import logging
import unittest
from crontab import CronTab
from mock import patch

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from schedule import Schedule
except ImportError as e:
    print os.path.dirname(os.path.realpath(__file__)) + "/../"
    print sys.path
    print e
    print "Please check the python PATH for import test module. (%s)" \
        % __file__
    exit(1)

dirpath = os.path.dirname(os.path.realpath(__file__))


class TestScheduleClass(unittest.TestCase):

    @patch("schedule.ModelInitiator")
    def setUp(self, model):
        model.return_value.db = []
        self.schedule = Schedule()
        self.schedule.insert({
            "enable": 1,
            "alias": "reboot",
            "command": "uptime && reboot",
            "schedule": "0 0 * * *",
            "executer": True
        })
        # self.reboot = Reboot(connection=Mockup())

    def tearDown(self):
        self.schedule = None
        cron = CronTab(user=True)
        cron.remove_all()
        cron.write()

    def test_insert(self):
        '''Insert a job, It should insert a job and return it with id'''
        result = self.schedule.insert({
            "enable": 1,
            "alias": "reboot",
            "command": "uptime && test_insert",
            "schedule": "0 0 * * *",
            "executer": True
        })

        self.assertDictEqual({
            "id": 2,  # by default we have two factory entry (.json.factory)
            "enable": 1,
            "alias": "reboot",
            "command": "uptime && test_insert",
            "schedule": "0 0 * * *",
            "executer": True,
            "comment": "sanji_schedule_2"
        }, result)

        jobs = []
        cron = CronTab(user=True)
        for job in cron.find_comment("sanji_schedule_2"):
            jobs.append(job)
        self.assertEqual(len(jobs), 1)

    def test_update(self):
        '''Update a job, It should update a job and return it'''
        added = self.schedule.get()[0]

        result = self.schedule.update({
            "id": added["id"],
            "enable": 1,
            "alias": "upgrade-firmware",
            "command": "/usr/bin/upgrade-firmware",
            "schedule": "1 1 1 * *",
            "executer": True
        })

        self.assertNotEqual(result, None)

        self.assertDictEqual({
            "id": added["id"],
            "enable": 1,
            "alias": "upgrade-firmware",
            "command": "/usr/bin/upgrade-firmware",
            "schedule": "1 1 1 * *",
            "executer": True,
            "comment": added["comment"]
        }, result)

        jobs = []
        cron = CronTab(user=True)
        for job in cron.find_comment(result["comment"]):
            jobs.append(job)
            self.assertEqual(job.slices, result["schedule"])
            self.assertEqual(job.command, result["command"])
        self.assertEqual(len(jobs), 1)

    def test_delete(self):
        '''Delete a job,
        It should delete a job by id and return effected count'''
        added = self.schedule.get()[0]
        result = self.schedule.delete(added["id"])
        self.assertEqual(result, 1)
        result = self.schedule.get()
        self.assertEqual(len(result), 0)

    def test_get_all(self):
        '''Get all jobs,
        It should return all jobs'''
        self.schedule.insert({
            "enable": 1,
            "alias": "1",
            "command": "uptime && test_get_all",
            "schedule": "0 0 * * *",
            "executer": True
        })
        self.schedule.insert({
            "enable": 1,
            "alias": "1",
            "command": "uptime && test_get_all",
            "schedule": "0 0 * * *",
            "executer": True
        })
        result = self.schedule.get()
        self.assertEqual(len(result), 3)

    def test_get_by_id(self):
        '''Get a job by id, It should return a job with correct id'''
        result = self.schedule.get(1)
        self.assertEqual(result["id"], 1)


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=20, format=FORMAT)
    logger = logging.getLogger("Schedule Test")
    unittest.main()
