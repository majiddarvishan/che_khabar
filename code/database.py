import pymysql

# https://itnext.io/sqlalchemy-orm-connecting-to-postgresql-from-scratch-create-fetch-update-and-delete-a86bc81333dc
# https://www.tutorialspoint.com/python3/python_database_access.htm

class Database():
    def __init__(self):
        self._connection = None

        self._connection_config_dict = {
            'user': 'root',
            'password': '123456',
            'host': '127.0.0.1',
            'database': 'che_khabar',
            'autocommit': True
            }

        self._conn(self._connection_config_dict)

    def __del__(self):
        # print('Database destructor called.')
        if(self._connection.open):
            self._connection.close()

    def _conn(self, config_dict: dict):
        # Open database connection
        try:
            self._connection = pymysql.connect(**self._connection_config_dict)
            print("Database Instance created")
        except Exception as e:
            print("Error while connecting to MySQL", e)

        # return self._connection.cursor()

    def _db_read_exe(self,query):
        try:
            # prepare a cursor object using cursor() method
            cur = self._connection.cursor()

            if cur.connection:
                # execute SQL query using execute() method.
                cur.execute(query)

                # column headers
                # desc = cursor.description
                # print(f'{desc[0][0]:<8} {desc[1][0]:<15} {desc[2][0]:>10}')

                # affected rows
                # print(f'The query affected {cur.rowcount} rows')

                return True, cur.fetchall()
            else:
                print("trying to reconnect")
                # cur=conn()
        except Exception as e:
            return False, str(e)
        finally:
            if(self._connection.open):
                cur.close()

    def _db_write_exe(self, query):
        try:
            # prepare a cursor object using cursor() method
            cur = self._connection.cursor()

            if cur.connection:
                # execute SQL query using execute() method.
                cur.execute(query)

                self._connection.commit()

                # Get the primary key value of the last inserted row
                print("Primary key id of the last inserted row:")
                print(cur.lastrowid)

                return True, "OK"
            else:
                print("trying to reconnect")
                # cur=conn()
        except Exception as e:
            return False, str(e)
        finally:
            if(self._connection.open):
                cur.close()

    def read_user_info(self, user_profile, user_id):
        sql = f"SELECT * FROM user_profile WHERE id = {user_id}"
        results, users = self._db_read_exe(sql)

        if(results):
            for row in users:
                user_profile.user_id = row[0]
                user_profile.user_name = row[1]
                user_profile.user_last_name = row[2]
                user_profile.user_mobile = row[3]
                user_profile.user_email = row[4]
                user_profile.distance = row[5]
                user_profile.tags = row[6]

    def save_user_data(self, user_profile):
        sql = f"""INSERT INTO user_profile(name, last_name, mobile, email, distance, tags) VALUES(
                '{user_profile.user_name}', 
                '{user_profile.user_last_name}',
                '{user_profile.user_mobile}', 
                '{user_profile.user_email}', 
                '{user_profile.distance}', 
                '{user_profile.tags}')"""

        return self._db_write_exe(sql)

    def read_advertise_info(self, advertisement, advertise_id):
        sql = f"SELECT * FROM advertisements WHERE id = {advertise_id}"
        results, advertises = self._db_read_exe(sql)

        if(results):
            for row in advertises:
                advertisement.id = row[0]
                advertisement.user_id = row[1]
                advertisement.body = row[2]
                advertisement.latitude = row[3]
                advertisement.longitude = row[4]
                advertisement.start_date = row[5]
                advertisement.end_date = row[6]
                advertisement.tags = row[7]

    def save_advertise_data(self, advertisement):
        sql = f"""INSERT INTO advertisements(user_id, body, latitude, longitude, start_date, end_date, tags) VALUES(
                '{advertisement.user_id}', 
                '{advertisement.body}',
                '{advertisement.latitude}', 
                '{advertisement.longitude}',
                '{advertisement.start_date}', 
                '{advertisement.end_date}',
                '{advertisement.tags}')"""

        return self._db_write_exe(sql)

    # https://gis.stackexchange.com/questions/31628/find-points-within-a-distance-using-mysql
    # https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    # https://www.geodatasource.com/distance-calculator
    # https://www.movable-type.co.uk/scripts/latlong-db.html
    # https://sweetcode.io/flask-python-3-mysql/
    # https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73
    def find_nearest_points(self, lat, lng, distance):
        results = []
        # 6371 : earth's mean radius, km
        # 3959 : earth's mean radius, miles
        sql = f"""
                SELECT
                    body,
                    latitude,
                    longitude,
                    tags,
                    Convert((6371 *
                    acos(
                        cos (radians({lat})) * cos(radians(latitude)) * cos(radians(longitude) - radians({lng})) +
                        sin (radians({lat})) * sin(radians(latitude))
                        )
                    * 100
                    ), UNSIGNED ) AS distance
                FROM advertisements
                HAVING distance < {distance} AND latitude != {lat} AND longitude != {lng}
                ORDER BY distance
                LIMIT 0 , 20;
                """
        res, results = self._db_read_exe(sql)

        return results