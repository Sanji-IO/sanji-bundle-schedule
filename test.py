from crontab import CronTab

cron = CronTab(user=True)

# for job in cron:
#     job.setall("1,2 1,2 * * *")
#     job.set_comment("")

for job in cron.find_comment("New ID or comment here"):
    print job

print cron.write()
