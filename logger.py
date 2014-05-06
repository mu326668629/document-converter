from logentries import LogentriesHandler
import logging
from config import LOGENTRIES_KEY

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
log.addHandler(LogentriesHandler(LOGENTRIES_KEY))
