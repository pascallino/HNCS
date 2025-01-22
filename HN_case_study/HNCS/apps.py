from django.apps import AppConfig
from mongoengine import connect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .job import Store_News_every_five_minutes
from datetime import datetime

class HncsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HNCS'
    def ready(self):
        #from .scheduler import start
        #start()
         # Initialize the scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            Store_News_every_five_minutes, 
            trigger=IntervalTrigger(seconds=10),
            id=str(datetime.now),  # Unique ID for the job
            replace_existing=True  # Replace if the job ID already exists
        )

        # Start the scheduler
        #scheduler.start()
        connect(
            db='HNCS',
            host='localhost',
            port=27017,
         )
