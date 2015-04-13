from crontab import CronTab

"""
{
    "id":1,
    "enable": 0,
    "alias": "reboot",
    "command": "reboot",
    "schedule": "0 0 3 1,3,5,7,9,11 *",
    "executer": "root"
}
"""


class Schedule(object):
    '''Schedule bundle class'''
    def __init__(self, *args, **kwargs):
        self.db = []
        # path_root = os.path.abspath(os.path.dirname(__file__))
        # self.db = ModelInitiator("schedule", path_root)

    def update(self, data):
        '''Update job by input data'''
        for job in self.db:
            if job["id"] != data["id"]:
                continue
            #  update by merge two dict
            job = dict(job.items() + data.items())
            self.update_job(job)
            return job

        return None

    def update_job(self, job):
        '''Sync job to system'''
        cron = CronTab(user=job["executer"])
        cron.remove_all(comment=job["comment"])
        if job["enable"] != 1:
            cron.write()
            return
        item = cron.new(command=job["command"], comment=job["comment"])
        item.setall(job["schedule"])
        cron.write()

    def insert(self, data):
        '''Insert a job and return data with id'''
        insert_id = self._get_max_id() + 1
        data = dict({
            "enable": 0,
            "alias": "",
            "command": "",
            "schedule": "",
            "executer": True
        }.items() + data.items())  # default dict merge input data

        data["id"] = insert_id
        data["comment"] = "sanji_schedule_%s" % (insert_id)
        self.db.append(data)

        if data["enable"] == 1:
            self.insert_job(data)

        return data

    def insert_job(self, job):
        '''Sync to system crontab by assigned user'''
        cron = CronTab(user=job["executer"])
        item = cron.new(command=job["command"], comment=job["comment"])
        item.setall(job["schedule"])
        cron.write()

    def delete(self, id):
        '''Delete job by assigned id'''
        to_remove = [i for i, val in enumerate(self.db) if val["id"] == id]
        for index in reversed(to_remove):
            self.delete_job(self.db[index])
            del self.db[index]

        return len(to_remove)

    def delete_job(self, job):
        cron = CronTab(user=job["executer"])
        cron.remove_all(comment=job["comment"])
        cron.write()

    def get(self, id=None):
        '''Get a job by assigned id or all jobs'''
        if id is None:
            return self.db

        for job in self.db:
            if job["id"] == id:
                return job

        return None

    def _get_max_id(self):
        '''Get current max id'''
        maxid = 0
        for job in self.db:
            if job["id"] > maxid:
                maxid = job["id"]

        return maxid
