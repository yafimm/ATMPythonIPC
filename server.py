# import library socket karena akan menggunakan IPC socket
import socket
import json
import threading    
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

#menentukan alamat server
server_address = ('localhost',4999)
 
#ukuran buffer ketika menerima pesan
SIZE = 1024
 
#membuat objek socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#bind ke alamat server
s.bind(server_address)
 
#mendengarkan koneksi dari client
s.listen(5)


lock = threading.Lock()
    
#login rekening
def login(name, pin):
    lock.acquire()
    account = {}
    data = readData()
    login = -1
    for x in data:
        if(x['name'] == name) and (x['pin'] == pin):
            login = 1
            account = get_account(data, name)
    lock.release()
    if(login == -1):
        return False
    else:
        return account['name']

#Fungsi untuk mengambil akun sesuai dengan name yang tentunya didapatkan dari login
def get_account(data, name):
    for d in data:
        if(d['name'] == name):
            return d
    return None

#Fungsi untuk membaca json ke array
def readData():
    try:
        with open('rekening.json') as json_file:  
            data = json.load(json_file)
            data = data['rekening']
    except IOError:
        print("unable to open {}".format(ACCOUNT_FILE))
    return data 

#Fungsi untuk update data rekening / data jsonnya
def update_rekening(account):
    all_data = readData()
    index = 0;
    lock.acquire()
    for i in all_data:
        if(i['name'] == account['name']):
            all_data[index] = account
        index += 1
    data = {}
    data['rekening'] = []
    data['rekening'] = all_data
    lock.release()
    with open('rekening.json', 'w') as outfile:   
        json.dump(data, outfile)
    return True

#Fungsi untuk update akun setelah melakukan aksi
def update_account(name):
    data = readData()
    return get_account(data, name)

#Fungsi untuk cek saldo
def balance_check(account):
    data = readData()
    account = get_account(data, account['name'])
    print("akun " + account['name'] + " sedang cek Saldo")
    return "Message : Saldo anda Rp." + str(account['balance']) + "\n"

#Fungsi untuk nabung          
def deposit(account, ammount):
    try:
      ammount = int(ammount)
      if(ammount > 0)   :
        if(ammount <= 100000000):
            change_value(account, ammount)
            account = update_account(account['name'])
            print('Akun '+ account['name'] +' Berhasil deposit sebesar Rp.'+ str(ammount))
            return "Message : Deposit berhasil sebesar Rp."+ str(ammount) +" ammount \n"        
        else:
            print('Akun '+ account['name'] +' gagal karena melebihi nominal')
            return "Message : Jumlah deposit melebihi nominal direkening \n"
      else:
         return "Message : Jumlah harus positif \n"
            
    except OverflowError as err:
        return "Message : Jumlah tidak bisa melebihi batas integer \n"
    except ValueError as verr:
        return "Message : Hanya dapat diisi dengan nilai angka \n"

#Fungsi untuk narik
def withdraw(account, ammount):
    try:
        ammount = int(ammount)
        if(ammount > 0):
            if(ammount <= account['balance'] and ammount <= 100000000):
                change_value(account, -(ammount))
                account = update_account(account['name'])
                print('Akun '+ account['name'] +' Berhasil withdraw sebesar Rp.' +str(ammount))
                return "Message : Withdraw berhasil sebesar Rp."+ str(ammount) +" ammount \n"
            else:
                print('Akun '+ account['name'] +' Gagal withdraw sebesar Rp.' +str(ammount)+' Karena melebihi batas atau diatas Rp.100.000.000 \n')
                return "Message : Withdraw gagal, saldo direkening tidak mencukupi \n"
        else:
            return "Message : Gagal, nilai negatif \n"
    except OverflowError as err:
        return "Message : Jumlah tidak bisa melebihi batas integer \n"
    except ValueError as verr:
        return "Message : Hanya dapat diisi dengan nilai angka \n"                               


#Fungsi untuk merubah nilai rekening
def change_value(account, ammount):
    account['balance'] += ammount
    update_rekening(account)

#Fungsi untuk menampilkan menu
def tampilan_menu():
    tampilan = "---- Selamat Datang ---- \n 1. Deposit \n 2. Withdraw \n 3. Check your ballance \n 4. Transfer \n 5. Exit"
    return tampilan

def transfer(account1, nama_penerima, ammount):
    try:
        ammount = int(ammount)
        data = readData()
        account2 = get_account(data, nama_penerima)
        if(account1['name'] == account2['name']):
            print('Akun '+ account1['name'] +' Gagal transfer ke diri sendiri \n')
            return "Message : Tidak bisa transfer ke diri sendiri \n"
        elif(account2):
            change_value(account1, -(ammount))
            change_value(account2, (ammount))
            print('Akun '+ account1['name'] +' Transfer sebesar Rp.' +str(ammount)+' ke rekening '+account2['name']+'\n')
            return "Message : Berhasil, Transfer sebesar Rp."+ str(ammount)+" ke rekening "+account2['name']+"\n" 
        else:
            return "Message : Nama Pengirim Tidak ditemukan \n"
    except OverflowError as err:
        return "Message : Jumlah tidak bisa melebihi batas integer \n"
    except ValueError as verr:
        return "Message : Hanya dapat diisi dengan nilai angka \n"


def main():
    
    #siap menerima pesan terus-menerus dari client
    while 1 :
     print ("Waiting for connection")
     
     #menerima koneksi dari client
     client, client_address = s.accept()
     
     print ("Connected from : ", client_address)
     
     while 1 :
         #menerima pesan dari client
         message = client.recv(SIZE)
         account = client.recv(SIZE)
         ammount = client.recv(SIZE)
         message = message.decode('UTF-8')
         print(message)
         type(message)
         if(message == "1"):
             balik = deposit(account.decode("utf-8"),ammount.decode("utf-8"))
         elif(message == "2"):
             balik = withdraw(account.decode("utf-8"),ammount.decode("utf-8"))
         elif(message == "3"):
             balik = balance(account.decode("utf-8")
         elif(message == "4"):
             balik = transfer(account.decode("utf-8"), nama_penerima("utf-8"), ammount.decode("utf-8"))
         else :
             balik = "Inputan Salah"
         
         #jika tidak ada pesan, keluar dari while
         if not message:
             break
             print (message)
     
     balik = bytes(balik, "utf-8")

     #mengirimkan kembali pesan ke client
     client.send(balik)
     
     #menutup client
     client.close()
     
     #menutup socket
     s.close()


main()
