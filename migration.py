# Migration in Databases
import argparse
import mysql.connector
from config import mysql_config

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=mysql_config['host'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            database=mysql_config['database']
        )
        if connection.is_connected():
            print("Berhasil terhubung ke MySQL Database")
            return connection
    except mysql.connector.Error as e:
        print(f"Gagal terhubung ke MySQL Database: {e}")
        return None

def drop_all_tables(connection):  # sourcery skip: extract-method, last-if-guard
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"Tabel {table_name} berhasil dihapus")
                
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            connection.commit()
            print("Penghapusan tabel selesai")
        except mysql.connector.Error as e:
            print(f"Terjadi kesalahan saat menghapus tabel: {e}")
            
def migrate_data(connection):  # sourcery skip: extract-method, last-if-guard
    if connection:
        try:
            cursor = connection.cursor()

            # Migrasi tabel hobi
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hobi (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255)
                )
            """)
            print("Migrasi data tabel 'hobi' selesai")
            hobi_list = [
                'Sepak Bola', 'Basket', 'Renang', 'Bersepeda', 'Bulu Tangkis',
                'Futsal', 'Panjat Tebing', 'Jogging', 'Badminton', 'Tenis',
                'Memancing', 'Memanah', 'Golf', 'Mengecat', 'Mendaki',
                'Belajar', 'Menulis', 'Membaca', 'Memasak', 'Berkebun'
            ]
            for hobi in hobi_list:
                cursor.execute("INSERT INTO hobi (nama) VALUES (%s)", (hobi,))
                
            connection.commit()
            print("Tambah hobi ke tabel 'hobi' selesai")

            # Migrasi tabel anggota
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS anggota (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama VARCHAR(255),
                    usia INT,
                    email VARCHAR(255),
                    deskripsi TEXT,
                    tanggal_lahir DATE,
                    gender ENUM('Laki-laki', 'Perempuan'),
                    status ENUM('Menikah', 'Belum Menikah')
                )
            """)
            print("Migrasi data tabel 'anggota' selesai")

            # Menambahkan contoh data ke tabel 'anggota'
            anggota_data = [
                ('John Doe', 30, 'john@example.com', 'Seorang programmer', '1990-01-01', 'Laki-laki', 'Menikah'),
                ('Jane Doe', 25, 'jane@example.com', 'Seorang desainer', '1995-05-05', 'Perempuan', 'Belum Menikah'),
                ('Michael Smith', 35, 'michael@example.com', 'Seorang pengusaha', '1985-10-10', 'Laki-laki', 'Belum Menikah')
            ]

            for data in anggota_data:
                cursor.execute("""
                    INSERT INTO anggota (nama, usia, email, deskripsi, tanggal_lahir, gender, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, data)

            # Migrasi tabel pivot untuk hobi_anggota
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hobi_anggota (
                    anggota_id INT,
                    hobi_id INT,
                    PRIMARY KEY (anggota_id, hobi_id),
                    FOREIGN KEY (anggota_id) REFERENCES anggota(id) ON DELETE CASCADE,
                    FOREIGN KEY (hobi_id) REFERENCES hobi(id) ON DELETE CASCADE
                )
            """)
            print("Migrasi data tabel 'hobi_anggota' selesai")

            # Menambahkan contoh data ke tabel 'hobi_anggota'
            hobi_anggota_data = [
                (1, 1),  # Anggota 1 memiliki hobi 1
                (1, 2),  # Anggota 1 memiliki hobi 2
                (1, 3),  # Anggota 1 memiliki hobi 3
                (1, 4),  # Anggota 1 memiliki hobi 4
                (1, 5),  # Anggota 1 memiliki hobi 5
                (2, 2),  # Anggota 2 memiliki hobi 2
                (2, 3),  # Anggota 2 memiliki hobi 3
                (2, 4),  # Anggota 2 memiliki hobi 4
                (2, 5),  # Anggota 2 memiliki hobi 5
                (3, 3),  # Anggota 3 memiliki hobi 3
                (3, 4),  # Anggota 3 memiliki hobi 4
                (3, 5),  # Anggota 3 memiliki hobi 5
            ]

            for data in hobi_anggota_data:
                cursor.execute("""
                    INSERT INTO hobi_anggota (anggota_id, hobi_id) 
                    VALUES (%s, %s)
                """, data)
            print("Migrasi data tabel 'hobi_anggota' selesai")

            connection.commit()
            print("Migrasi data selesai")
        except mysql.connector.Error as e:
            print(f"Terjadi kesalahan saat migrasi data: {e}")

# sourcery skip: use-named-expression
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Migrasi Database')
    parser.add_argument('--fresh', action='store_true', help='Menghapus semua database sebelum migrasi')
    args = parser.parse_args()
    if args.fresh:
        try:
            connection = connect_to_mysql()
            drop_all_tables(connection)
        except mysql.connector.Error as e:
            print(f"Terjadi kesalahan saat menghapus database: {e}")
        finally:
            if connection:
                connection.close()
    # Jalankan migrasi
    connection = connect_to_mysql()
    if connection:
        migrate_data(connection)
        connection.close()
        print("Koneksi ke MySQL Database ditutup")