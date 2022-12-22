#!/usr/bin/python3

'''MIT License

Copyright (c) 2022 Collen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from bs4 import BeautifulSoup
from time import sleep 
import requests
import os 
from colorama import Fore, Style
import re 

def banner():
	os.system("clear")
	print(Style.BRIGHT + """  
    ____                           __  ______          
   /  _/___  _________  ___  _____/ /_/ ____/___ ______
   / // __ \/ ___/ __ \/ _ \/ ___/ __/ /   / __ `/ ___/
 _/ // / / (__  ) /_/ /  __/ /__/ /_/ /___/ /_/ / /    
/___/_/ /_/____/ .___/\___/\___/\__/\____/\__,_/_/     
              /_/\n""")
	sleep(0.5)


def main():

	placa = ""
	while placa == "":
		banner()
		placa = input("[-] INSIRA A PLACA: ").strip().upper()

	headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
	}
	url = f"https://www.keplaca.com/placa/{placa}"
	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		site = BeautifulSoup(response.content, "html.parser")
		check = site.find("h2")
		if "outra" in check.text:
			banner()
			print("[-] A PLACA " + Fore.RED + placa + Fore.RESET + " ESTÁ EM UM FORMATO INVÁLIDO OU NÃO EXISTE!")
			sleep(3)
			main()
		else:
			banner()
			print("[-] BUSCANDO POR " + Fore.GREEN + placa + Fore.RESET + ".")
			sleep(2)
			banner()
			tabela = site.find("table", class_="fipeTablePriceDetail")
			tag_tr = tabela.find_all("tr")
			tag_p = site.find_all("p")
			file = open(placa + ".txt", "tw")
			for x in range(len(tag_tr)):
				x = re.sub(":",": ", tag_tr[x].text.upper())
				sleep(0.5)
				print("[-] " + x)
				file.write("[-] " + x + "\n")

			sleep(0.5)
			print("[-] " + tag_p[0].text.upper())
			file.write("[-] " + tag_p[0].text.upper() + "\n")

			for i in range(len(tag_p)):
				if "sistema" in tag_p[i].text:
					sleep(0.5)
					print("[-] " + tag_p[i].text.upper())
					file.write("[-] " + tag_p[i].text.upper())
					file.close()
				else:
					pass

			def busca():
				nova_busca = input("\n[-] DESEJA FAZER UMA NOVA BUSCA? (Y/N) ").upper().strip()
				if nova_busca == "Y":
					main()
				elif nova_busca == "N":
					banner()
					print("[-] ENCERRANDO... SUAS PESQUISAM FORAM SALVAS EM UM ARQUIVO DE TEXTO NA PASTA DO PROGRAMA!")
					sleep(5)
					os.system("clear")
				else:
					print("\nRESPOSTA INVÁLIDA!")
					busca()

			busca()

	else:
		banner()
		print("[-] VOCÊ FOI BANIDO TEMPORARIAMENTE DO SERVIÇO! USE UMA VPN OU AGUARDE PARA USAR NOVAMENTE.")
		sleep(5)
		os.system("clear")

main()
