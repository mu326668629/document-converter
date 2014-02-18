from time import sleep
from models import db, Conversion, STATUS
from tasks import document_converter
from utils import PidManager

def request_fetcher(pm = PidManager('proc/rf.pid')):
    pm.register()
    while True:
        # Get conversions by priority
        conversions = Conversion.get_requests_by_priority(limit = 1)

        # Forward request ids to document converter
        conversion_ids = map(lambda conversion: conversion.id, conversions)
        if conversion_ids:
            document_converter.delay(conversion_ids)

            # Mark Queued
            for conversion in conversions:
                conversion.status = STATUS.queued
                db.session.commit()

        # Iter after sleep
        sleep(0.15)

if __name__ == '__main__':
    rf = PidManager('proc/rf.pid')
    
    if not rf.is_running():
        request_fetcher(rf)