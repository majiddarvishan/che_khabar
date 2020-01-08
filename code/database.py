import pymysql

# https://itnext.io/sqlalchemy-orm-connecting-to-postgresql-from-scratch-create-fetch-update-and-delete-a86bc81333dc

def read(user_profile, user_id):
    try:
        # Open database connection
        db = pymysql.connect("localhost","darvishan","darvishan","che_khabar" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = f"SELECT * FROM user_profile WHERE user_id = {user_id}"
               
        # execute SQL query using execute() method.
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            user_profile.user_id = row[0]
            user_profile.user_name = row[1]
            user_profile.user_password = row[2]
            user_profile.user_mobile = row[3]
            user_profile.distance = row[4]
            user_profile.tags = row[5]
            
        # disconnect from server
        db.close()
    except Exception as e:
        print(str(e))

def save_user_data(user_profile):
    try:
        db = pymysql.connect("localhost","darvishan","darvishan","che_khabar" )

            # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = f"""INSERT INTO user_profile(user_name, user_password, user_mobile, distance, tags) VALUES(
                '{user_profile.user_name}', '{user_profile.user_password}', 
                '{user_profile.user_mobile}', '{user_profile.distance}', '{user_profile.tags}')"""
        
        cursor.execute(sql)

        db.commit()

        # Get the primary key value of the last inserted row
        print("Primary key id of the last inserted row:")
        print(cursor.lastrowid)

    except Exception as e:
        print(str(e))
        
    finally:
        db.close()
    
def save_advertise_data(advertisement):
    try:
        db = pymysql.connect("localhost","darvishan","darvishan","che_khabar" )

            # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = f"""INSERT INTO advertisements(advertiser_id, body, latitude, longitude, start_date, end_date, tags) VALUES(
                '{advertisement.advertiser_id}', '{advertisement.body}', 
                '{advertisement.latitude}', '{advertisement.longitude}', 
                '{advertisement.start_date}', '{advertisement.end_date}', 
                '{advertisement.tags}')"""
        
        cursor.execute(sql)

        db.commit()

        # Get the primary key value of the last inserted row
        print("Primary key id of the last inserted row:")
        print(cursor.lastrowid)

    except Exception as e:
        print(str(e))
        
    finally:
        db.close()
    
# https://gis.stackexchange.com/questions/31628/find-points-within-a-distance-using-mysql
# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
# https://www.geodatasource.com/distance-calculator
def find_nearest_points(lat, lng, distance):
    try:
        db = pymysql.connect("localhost","darvishan","darvishan","che_khabar" )

            # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # 6371 : earth's mean radius, km
        # 3959 : earth's mean radius, miles
        sql = f"""
                SELECT
                    id, 
                    latitude,
                    longitude,
                    (6371 * 
                    acos(
                         cos (radians({lat})) * cos(radians(latitude)) * cos(radians(longitude) - radians({lng})) +
                         sin (radians({lat})) * sin(radians(latitude))
                        )
                    ) AS distance
                FROM advertisements
                HAVING distance < {distance} AND latitude != {lat} AND longitude != {lng}
                ORDER BY distance
                LIMIT 0 , 20;
                """
           
        cursor.execute(sql)

        results = cursor.fetchall()
        for row in results:
            print(row)

    except Exception as e:
        print(str(e))
        
    finally:
        db.close()