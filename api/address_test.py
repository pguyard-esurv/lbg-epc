from esurv_db_manager import AL_DB

al_db = AL_DB()
al_conn = al_db.connect()
al_db.disconnect()