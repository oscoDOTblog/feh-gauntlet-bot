from crontab import CronTab
from current_vg import *
from gauntlet_template import *
import os 

# Set up Logging
logger = set_up_logger(__file__)

# Set up Cron Jobs (https://stackabuse.com/scheduling-jobs-with-python-crontab/)
cron = CronTab(user=True)
abs_path = os.path.abspath("")
# '/home/argo/Code/FEH-Gauntlet-Bot/Deployment'
for bot in crontab_bots:
    cron_command = f"python3 {abs_path}/{bot}"
    logger.info("adding to crontab -l >> " + cron_command)
    job = cron.new(command=cron_command)
    # job.minute.on(5) # Set to 5 * * * *
    cron.write()
    job.enable()

# Check Cron Jobs
# crontab -l

