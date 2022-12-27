import mysql.connector
import sys
from datetime import datetime

def user_list(host = "127.0.0.1", port=8000 ,user="root" ,password="1234"):
    print(sys._getframe().f_code.co_name , str(datetime.now()))
    
    try:
        connection = mysql.connector.connect(host = host,
                                             port = port,
                                             user = user,
                                             password = password)
        cursor = connection.cursor()
        sql = "SELECT userID, name FROM user.user;"

        cursor.execute(sql, )
        record = cursor.fetchall()
        row = []
        with open(r".\Python\DB\User_List.txt", "w") as f:
            for i in range(0, len(record)):
                f.write(str(record[i][0]) + "\n")
                f.write(str(record[i][1]) + "\n")
        if (connection.is_connected()):
            cursor.close()
            connection.close()        
                
    except mysql.connector.Error as error:
        print(sys._getframe().f_code.co_name, "Except mysql.connector.Error: ", error)

    except UnboundLocalError as e:
        print(sys._getframe().f_code.co_name, "Except UnboundLocalError: ", e)