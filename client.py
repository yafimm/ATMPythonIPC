# import xmlrpc bagian client saja
import xmlrpc.client
import os
import math

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://192.168.1.6:13000', allow_none = True)
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
			print(s.deposit(account, ammount))
		elif (t=='2'):
			ammount = input("JUMLAH Withdraw : ")
			print(s.withdraw(account, ammount))
		elif (t=='3'):
			print(s.balance_check(account))
		elif (t=='4'):
			nama_penerima = input("Nama Pengirim : ")
			ammount = input("JUMLAH Transfer : ")
			print(s.transfer(account, nama_penerima, ammount))
		elif (t=='5'):
			z == False
else:
	print("maaf password salah")
