from esurv_db_manager import SH_DB

al_db = SH_DB()
al_conn = al_db.connect()
al_db.disconnect()
print('success')