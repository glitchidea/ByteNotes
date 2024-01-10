import os
import sqlite3
import datetime

# Default database file path
db_path = 'notlar.db'

# Create database connection
def create_connection(path=db_path):
    return sqlite3.connect(path)

# Create database table
def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS notlar
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             BASLIK TEXT NOT NULL,
             ICERIK TEXT NOT NULL,
             ETIKET TEXT,
             OLUSTURMA_TARIHI TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             GUNCELLEME_TARIHI TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')

# Main system menu
def ana_menu():
    # Open database connection
    conn = create_connection()

    # Create database table
    create_table(conn)

    while True:
        os.system("cls")
        print("\nAna sistem")
        print("----------------------")
        print("1-Yeni not")
        print("2-Tüm notlar")
        print("3-Not ara")
        print("4-Not sil")
        print("5-Not güncelle")
        print("6-Ayarlar")
        print("7-Çıkış")

        secim = input("Seçim yapınız: ")

        if secim == "1":
            yeni_not_ekle(conn)
            input("  ")
        elif secim == "2":
            tum_notlari_goster(conn)
            input("  ")
        elif secim == "3":
            not_ara(conn)
            input("  ")
        elif secim == "4":
            not_sil(conn)
            input("  ")
        elif secim == "5":
            not_guncelle(conn)
            input("  ")
        elif secim == "6":
            ayarlar_menu(conn)
            input("  ") 
        elif secim == "7":
            print("Program sonlandırıldı.")
            conn.close()
            break
        else:
            print("Hatalı giriş.")

# Function to add new note
def yeni_not_ekle(conn):
    os.system("cls")
    baslik = input("Not başlığı giriniz: ")
    icerik = input("Not içeriği giriniz: ")
    etiket = input("Etiket giriniz: ")
    tarih = datetime.datetime.now()

    conn.execute("INSERT INTO notlar (BASLIK, ICERIK, ETIKET, OLUSTURMA_TARIHI, GUNCELLEME_TARIHI) \
                  VALUES (?, ?, ?, ?, ?)", (baslik, icerik, etiket, tarih, tarih))

    conn.commit()
    print("Not başarıyla eklendi.")

# Function to display all notes
def tum_notlari_goster(conn):
    os.system("cls")
    secim = input("Tüm notlar için (1)\nEtikete göre filtrelemek için (2)\nSeçim yapınız: ")
    
    if secim == "1":
        cursor = conn.execute("SELECT * FROM notlar")
    elif secim == "2":
        etiket = input("Etiket giriniz: ")
        cursor = conn.execute("SELECT * FROM notlar WHERE ETIKET=?", (etiket,))
    else:
        print("Hatalı giriş.")
        return

    for row in cursor:
        print("\nID: ", row[0])
        print("Başlık: ", row[1])
        print("İçerik: ", row[2])
        print("Etiket: ", row[3])
        print("Oluşturulma tarihi: ", row[4])
        print("Güncelleme tarihi: ", row[5])

#Function to search notes by keyword
def not_ara(conn):
    os.system("cls")
    anahtar_kelime = input("Aranacak kelimeyi giriniz: ")
    cursor = conn.execute("SELECT * FROM notlar WHERE BASLIK LIKE ? OR ICERIK LIKE ?", ('%'+anahtar_kelime+'%', '%'+anahtar_kelime+'%'))
    for row in cursor:
        print("\nID: ", row[0])
        print("Başlık: ", row[1])
        print("İçerik: ", row[2])
        print("Etiket: ", row[3])
        print("Oluşturulma tarihi: ", row[4])
        print("Güncelleme tarihi: ", row[5])

#Function to delete a note by ID
def not_sil(conn):
    os.system("cls")
    id = input("Silinecek notun ID'sini giriniz: ")
    conn.execute("DELETE FROM notlar WHERE ID=?", (id,))
    conn.commit()
    print("Not başarıyla silindi.")

#Function to update a note by ID
def not_guncelle(conn):
    os.system("cls")
    id = input("Güncellenecek notun ID'sini giriniz: ")
    baslik = input("Not başlığı giriniz: ")
    icerik = input("Not içeriği giriniz: ")
    etiket = input("Etiket giriniz: ")
    tarih = datetime.datetime.now()

def ayarlar_menu(conn):
    while True:
        os.system("cls")
        print("\nAyarlar")
        print("----------------------")
        print("1- Veri tabanı yedekle")
        print("2- Veri tabanı konumu değiştir")
        print("3- Veri tabanı şuan ki konumu")
        print("4- Veritabanı geri yükle")
        print("5- Geri")

        secim = input("Seçim yapınız: ")

        if secim == "1":
            veritabani_yedekle(conn)
            input("\Başarılı")
        elif secim == "2":
            veritabani_konum_degistir()
            db_path = input("\nBaşarılı")
        elif secim == "3":
            veritabani_konum_goster()
            input("\Başarılı")
        elif secim == "4":
            veritabani_geri_yukle()
            input("\Başarılı")
        elif secim == "5":
            print("Ayarlar menüsünden çıkılıyor...")
            break
        else:
            print("Hatalı giriş.")
            input("  ")
            
# Function to backup the database
def veritabani_yedekle(conn):
    os.system("cls")
    backup_file = input("Lütfen yedek dosyasının adını giriniz: ")
    if backup_file:
        with open(backup_file, 'wb') as f:
            f.write(conn.backup())
        print("Veritabanı yedekleme işlemi başarılı.")

# Function to change database file path
def veritabani_konum_degistir():
    os.system("cls")
    global db_path
    db_path = input("Lütfen yeni veritabanı dosyasının yolunu giriniz: ")
    print("Veritabanı dosya yolu başarıyla değiştirildi.")

# Function to show current database file path
def veritabani_konum_goster():
    os.system("cls")
    print(f"Şu anki veritabanı dosya yolu: {db_path}")

# Function to restore the database from backup
def veritabani_geri_yukle(conn):
    os.system("cls")
    backup_file = input("Lütfen geri yüklenecek yedek dosyasının adını giriniz: ")
    if backup_file:
        with open(backup_file, 'rb') as f:
            conn.rollback()
            conn.restore(f.read())
        print("Veritabanı geri yükleme işlemi başarılı.")

ana_menu()
