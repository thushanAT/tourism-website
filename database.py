# D.V.Punchihewa  24IT0506 (1 - 50)
import mysql.connector

def _getdb_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="travelmate_db"
    )
    return conn

def it_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS travelmate_db")
        cursor.execute("USE travelmate_db")
        
        # 1. Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                nationality VARCHAR(100)
            )
        ''')
    
        cursor.execute("DROP TABLE IF EXISTS drivers")
        
        # 2. Drivers Table 
        cursor.execute('''
            CREATE TABLE drivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                vehicle_type VARCHAR(100),
                rate_per_km DECIMAL(10, 2),
                document_pdf VARCHAR(255) NULL,
                is_verified TINYINT(1) DEFAULT 0
            )                       
        ''')
        # A.V.P.A.N.Sandunika  24IT0518  (51 - 98)
        cursor.execute("DROP TABLE IF EXISTS reviews")
        
        # 3. Reviews Table
        cursor.execute('''
            CREATE TABLE reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                reviewer_name VARCHAR(100) NOT NULL,
                rating INT NOT NULL,
                comment TEXT NOT NULL,
                date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        #4. Admins Table 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL
            )
        ''')
        
        #  default admin
        cursor.execute("SELECT * FROM admins WHERE email = 'admin@travelmate.lk'")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO admins (email, password, name) 
                VALUES ('admin@travelmate.lk', 'admin123', 'System Admin')
            """)
           

        conn.commit()
        cursor.close()
        conn.close()
        print("====================================================")
        print("Database Updated Successfully with Admin Support! 🎉")
        print("====================================================")
       
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == '__main__':
    init_db()