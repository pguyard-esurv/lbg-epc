import os

import psycopg2
import pyodbc
from dotenv import load_dotenv


class DatabaseBase(object):
    """
    Base class for all database utility classes to inherit from.
    """

    def __init__(self):
        self.env = self.get_enviroment_vars()

    def get_enviroment_vars(self):
        """
        Return a dict with the enviroment settings variables.
        """
        env_path = '.env.database'

        # Check file exists.e
        if not os.path.isfile(env_path):
            raise Exception('.env.database file does not exist in esurv_db_manager directory.')

        # Get PROD variable.
        load_dotenv(env_path)

        return os.environ

    @property
    def prod(self):
        """
        Return the PROD enviroment variable value, making sure it exists.
        """
        try:
            DB_PROD = int(os.environ['DB_PROD'])
            PROD = DB_PROD == 1
        except KeyError:
            raise Exception('DB_PROD variable does not exists in .env.database file.')
        except ValueError:
            raise Exception('PROD variable must be 0 or 1.')
        return PROD


class PG_DB(DatabaseBase):
    """
    Class to handle connection to postgres database.
    """

    def __init__(self):
        super().__init__()
        self.pg_conn = None

    def _connect_prod(self):
        self.pg_conn = psycopg2.connect(
            host="prd-rpa-01",
            dbname='rpalive01',
            user='postgres',
            password=self.env['PG_DB_PROD_PASSWORD'],
        )

    def _connect_dev(self):
        self.pg_conn = psycopg2.connect(
            host="prd-rpa-01",
            dbname='rpadev01',
            user='postgres',
            password=self.env['PG_DB_DEV_PASSWORD'],
        )

    def connect(self):
        if self.prod:
            self._connect_prod()
        else:
            self._connect_dev()

        return self.pg_conn

    def disconnect(self):
        self.pg_conn.close()


class SH_DB(DatabaseBase):
    """
    Class to handle connection to SurveyHub database.
    """

    def __init__(self, user=1):
        super().__init__()
        self.sh_conn = None
        self.user = user

    def _connect_prod(self):
        driver = self.env[f'SH_DB_DRIVER']
        server = '192.168.52.55'
        database = 'sh_esurv'

        username = self.env[f'SH_DB_UNAME{self.user}']
        password = self.env[f'SH_DB_PASSWORD{self.user}']

        driver = f'{driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
        self.sh_conn = pyodbc.connect(DRIVER=driver)

    def _connect_dev(self):
        server = '192.168.52.55'
        database = 'sh_esurv'
        username = self.env[f'SH_DB_UNAME{self.user}']
        password = self.env[f'SH_DB_PASSWORD{self.user}']

        driver = f'{{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.sh_conn = pyodbc.connect(DRIVER=driver)

    def connect(self):
        if self.prod:
            self._connect_prod()
        else:
            self._connect_dev()

        return self.sh_conn

    def disconnect(self):
        self.sh_conn.close()


class ES_DB(DatabaseBase):
    """
    Class to handle connection to Esurv MI database.
    """

    def __init__(self):
        super().__init__()
        self.es_conn = None

    def connect(self):
        server = 'ES-HBO-03'
        database = 'Dashboard_Views'
        username = 'RPAPROCESS'
        password = self.env['ES_DB_PROD_PASSWORD']
        driver = f'{{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.es_conn = pyodbc.connect(DRIVER=driver)

        return self.es_conn

    def disconnect(self):
        self.es_conn.close()


class LS_DB(DatabaseBase):
    """
    Class to handle connection to ___ database.
    """

    def __init__(self):
        super().__init__()
        self.lh_conn = None

    def _connect_prod(self):
        server = 'ES-HBO-03'
        database = 'LandRegistry'
        username = self.env['LS_DB_DEV_USERNAME']
        password = self.env['LS_DB_DEV_PASSWORD']

        driver = f'{{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.lh_conn = pyodbc.connect(DRIVER=driver)

    def _connect_dev(self):
        server = 'ES-HBO-03'
        database = 'LandRegistry'
        username = self.env['LS_DB_DEV_USERNAME']
        password = self.env['LS_DB_DEV_PASSWORD']

        driver = f'{{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.lh_conn = pyodbc.connect(DRIVER=driver)

    def connect(self):
        if self.prod:
            self._connect_prod()
        else:
            self._connect_dev()

        return self.lh_conn

    def disconnect(self):
        self.lh_conn.close()


class JBA_DB(DatabaseBase):
    """
    Class to handle connection to Esurv JBA database.
    """

    def __init__(self):
        super().__init__()
        self.jba_conn = None

    def connect(self):
        server = 'ES-HBO-03'
        database = 'JBA'
        username = 'RPAPROCESS'
        password = self.env['ES_DB_PROD_PASSWORD']
        driver = f'{{ODBC Driver 13 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.jba_conn = pyodbc.connect(DRIVER=driver)

        return self.jba_conn

    def disconnect(self):
        self.jba_conn.close()
        
class EPC_DB(DatabaseBase):
    """
    Class to handle connection to Esurv JBA database.
    """

    def __init__(self):
        super().__init__()
        self.epc_conn = None

    def connect(self):
        # server = 'ES-HBO-03'
        server = "psql-lbgepc-prd-uks-01.postgres.database.azure.com"
        database = "postgres"
        username = "psqladmin"
        password = os.getenv('DB_PASSWORD')
        driver_version = "PostgreSQL UNICODE(x64)"
        driver = f"{driver_version};SERVER={server};DATABASE={database};UID={username};PWD={password};SSLmode=allow"
        #driver_version = self.env[f"SH_DB_DRIVER"]
        #driver = f"{driver_version};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;sslverify=0"
        self.jba_conn = pyodbc.connect(DRIVER=driver)

        return self.epc_conn

    def disconnect(self):
        self.epc_conn.close()
