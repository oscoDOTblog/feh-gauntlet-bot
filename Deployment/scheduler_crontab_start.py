from crontab import CronTab
from current_vg import *
from gauntlet_template import *
import os 

# Set up Logging
logger = set_up_logger(__file__)

# Set up Cron Jobs (https://stackabuse.com/scheduling-jobs-with-python-crontab/)
cron = CronTab(user=True)
abs_path = os.path.abspath("")
for bot_module in crontab_bots:
    cron_command = 'python3 -m' + 
    job = cron.new(command='python3 -m Rebecca_Bot.rebecca_discord_client')
    # job.minute.on(5) # Set to 5 * * * *
    job.enable()
    cron.write()

# Check Cron Jobs
# crontab -l

