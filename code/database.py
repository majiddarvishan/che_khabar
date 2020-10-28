import pymysql

# https://itnext.io/sqlalchemy-orm-connecting-to-postgresql-from-scratch-create-fetch-update-and-delete-a86bc81333dc

class Database():
    def __init__(self):
        # Open database connection
        self.connection = pymysql.connect("localhost","root","123456","che_khabar" )
        print("Database Instance created")

    def __del__(self): 
        print('Database destructor called.') 
        self.connection.close()


    def read(self, user_profile, user_id):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.connection.cursor()

            sql = f"SELECT * FROM user_profile WHERE id = {user_id}"
                
            # execute SQL query using execute() method.
            cursor.execute(sql)

            results = cursor.fetchall()
            for row in results:
                user_profile.user_id = row[0]
                user_profile.user_name = row[1]
                user_profile.user_last_name = row[2]
                user_profile.user_mobile = row[3]
                user_profile.distance = row[4]
                user_profile.tags = row[5]
                
            # disconnect from server
            
        except Exception as e:
            print(str(e))

    def save_user_data(self, user_profile):
        try:
            # prepare a cursor object using cursor() method
            cursor = self.connection.cursor()

            sql = f"""INSERT INTO user_profile(name, last_name, mobile_no, distance, tags) VALUES(
                    '{user_profile.user_name}', '{user_profile.user_last_name}', 
                    '{user_profile.user_mobile}', '{user_profile.distance}', '{user_profile.tags}')"""
            
            cursor.execute(sql)

            self.connection.commit()

            # Get the primary key value of the last inserted row
            print("Primary key id of the last inserted row:")
            print(cursor.lastrowid)

        except Exception as e:
            print(str(e))
        
    def save_advertise_data(self, advertisement):
        try:
            db = pymysql.connect("localhost","root","123456","che_khabar" )

                # prepare a cursor object using cursor() method
            cursor = self.connection.cursor()

            sql = f"""INSERT INTO advertisements(user_id, body, latitude, longitude, start_date, end_date, tags) VALUES(
                    '{advertisement.user_id}', '{advertisement.body}', 
                    '{advertisement.latitude}', '{advertisement.longitude}', 
                    '{advertisement.start_date}', '{advertisement.end_date}', 
                    '{advertisement.tags}')"""
            
            cursor.execute(sql)

            self.connection.commit()

            # Get the primary key value of the last inserted row
            print("Primary key id of the last inserted row:")
            print(cursor.lastrowid)

        except Exception as e:
            print(str(e))
            
        
    # https://gis.stackexchange.com/questions/31628/find-points-within-a-distance-using-mysql
    # https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    # https://www.geodatasource.com/distance-calculator
    # https://www.movable-type.co.uk/scripts/latlong-db.html
    # https://sweetcode.io/flask-python-3-mysql/
    # https://www.codementor.io/@adityamalviya/python-flask-mysql-connection-rxblpje73
    def find_nearest_points(self, lat, lng, distance):
        results = []
        try:
            db = pymysql.connect("localhost","root","123456","che_khabar" )

                # prepare a cursor object using cursor() method
            cursor = self.connection.cursor()

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
            cursor.execute(sql)

            results = cursor.fetchall()

        except Exception as e:
            print(str(e))
            

        return results