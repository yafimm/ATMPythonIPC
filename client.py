# import xmlrpc bagian client saja
import xmlrpc.client
import os
import math
import socket
from pprint import pprint

#menentukan alamat server
server_address = ('localhost', 4999)
 
#ukuran buffer ketika menerima pesan
SIZE = 1024
 
#membuat objek socket (proses pertama)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#koneksi server (proses kedua)
s.connect(server_address)

z = True
os.system("cls")
print("LOGIN")
i=input("NAME : ")
p=input("PIN : ")
login = s.login(i, p)
if login :
	while (z==True):
		os.system("cls")
		account = s.update_account(login)
		print(s.tampilan_menu())
		t=input("Masukan Pilihan : ")
		os.system('cls')
		if (t=='1'):
			ammount = input("JUMLAH Deposit : ")
			#print(s.deposit(account, ammount))
			#mengirim pesan ke server (proses ketiga)
                        s.send(t.encode("utf-8"))
                        s.send(account.encode("utf-8"))
                        s.send(ammount.encode("utf-8"))
                        
		elif (t=='2'):
			ammount = input("JUMLAH Withdraw : ")
			#print(s.withdraw(account, ammount))
			s.send(t.encode("utf-8"))
                        s.send(account.encode("utf-8"))
                        s.send(ammount.encode("utf-8"))
		elif (t=='3'):
			#print(s.balance_check(account))
			s.send(t.encode("utf-8"))  
                        s.send(account.encode("utf-8"))
                elif (t=='4'):
			nama_penerima = input("Nama Pengirim : ")
			ammount = input("JUMLAH Transfer : ")
			#print(s.transfer(account, nama_penerima, ammount))
                        s.send(t.encode("utf-8"))
                        s.send(account.encode("utf-8"))
                        s.send(ammount.encode("utf-8"))
                        s.send(namapenerima.encode("utf-8"))
		elif (t=='5'):
			z == False

		#menerima pesan dari server
                message = s.recv(SIZE)

else:
	print("maaf password salah")
  
s.close()

