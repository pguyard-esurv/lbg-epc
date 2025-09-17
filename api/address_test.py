from esurv_db_manager import SH_DB

from logging_config import configure_root_logger, get_logger

configure_root_logger()
logger = get_logger(__name__)

al_db = SH_DB()
al_conn = al_db.connect()
al_db.disconnect()
logger.info("address_test_success")
