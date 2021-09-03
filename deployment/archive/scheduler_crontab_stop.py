### https://stackabuse.com/scheduling-jobs-with-python-crontab/
from gauntlet_template import * 
from crontab import CronTab

# Set up Logging
logger = set_up_logger(__file__)

# Remove all crontab jobs
cron = CronTab(user=True)
for job in cron:
    logger.info("disabling " + str(job))
    job.enable(False)
    cron.remove(job)
# cron.remove_all()
cron.write()



