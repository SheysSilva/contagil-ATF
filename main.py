# Generated by Selenium IDE
# -*- coding: UTF-8 -*- 

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

nfces = open('NFCE.txt','r')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/snap/bin/chromium.chromedriver')

lines = nfces.readlines()

def addKeys():
	i = 1
	while i < len(lines):
		print(i)
		nfce = lines[i].split('|')[0]
		try:
			driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(nfce)
		except NoSuchElementException:
			i-=i
			print('err')
		driver.find_element(By.NAME, "btnAdicionar").click()
		i+=1
		

def addKey(ini, fin):
	print(ini, fin)
	for i in range(ini, fin):
		print(i)
		nfce = lines[i].split('|')[0]
		driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(nfce)
		driver.find_element(By.NAME, "btnAdicionar").click()


def test():
	lines = nfces.readlines()
	driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(lines[1].split('|')[0])
	driver.find_element(By.NAME, "btnAdicionar").click()
	driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(lines[2].split('|')[0])
	driver.find_element(By.NAME, "btnAdicionar").click()
	driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(lines[3].split('|')[0])
	driver.find_element(By.NAME, "btnAdicionar").click()
	driver.find_element(By.NAME, "edtNrChaveAcesso").send_keys(lines[3].split('|')[0])
	driver.find_element(By.NAME, "btnAdicionar").click()


def message():
	time.sleep(2)
	driver.get('https://www4.receita.pb.gov.br/atf/seg/SEGf_MinhasMensagens.do')
	time.sleep(20)

	tr =  driver.find_elements_by_css_selector("tr")
	strg = 'FIS_1484 - Consulta de NFC-e por Emitente '
	i = 3
	if verify():
		while i < (len(tr)-2):
			td = tr[i]
			list = td.text.split()
			txt = ''
			if len(list) >= 7:
				for i in range(7):
					txt = txt + str(list[i]) + " "

				ID = driver.find_element_by_css_selector('a').get_attribute('href').encode("utf-8");
				if ID == "":
					i-=1;
				else:
					list = ID.split("'")
					link = 'https://www4.receita.pb.gov.br/atf/seg/SEGf_MinhasMensagens.do?hidsqMensagem='+list[1]

					if strg == txt:
						driver.get(link)
						break	
			i+=1

def archive():
	tr =  driver.find_elements_by_css_selector("tr")
	tr[5].click()

def verify():
	imgs = driver.find_elements_by_css_selector('img')
	count = 0
	for img in imgs:
		img = img.get_attribute('src').encode("utf-8");
		if img == 'https://www4.receita.pb.gov.br/atf/imagens/clips.gif' and count == 1:
			return True
		count+=1
	return False

def main(ini, fin):
	driver.get("https://www4.receita.pb.gov.br/atf/")
	driver.set_window_size(1296, 704)
	driver.switch_to.frame(1)
	driver.find_element(By.ID, "login").send_keys('fra13582')
	driver.find_element(By.NAME, "edtDsSenha").click()
	driver.find_element(By.NAME, "edtDsSenha").send_keys('fiscal3336*')

	time.sleep(2)

	driver.find_element(By.NAME, "btnAvancar").click()
	time.sleep(5)

	nfce = 'https://www4.receita.pb.gov.br/atf/fis/FISf_ConsultaGenericaEmitenteNFCe.do?limparSessao=true'
	driver.get(nfce)


	addKey(ini, fin)
	#test()

	select = Select(driver.find_element_by_name('cmbTpExibicao'))
	select.select_by_visible_text("TXT (produtos)")

	driver.find_element(By.NAME, 'btnConsultar').click() 

	message()
	archive()

	driver.find_element(By.TAG_NAME, 'a').click();
	print('FINISH')


count = len(lines)%64
summ = 0
ini = 1
for i in range(64, len(lines), 64):
	now = datetime.now()
	fin = i
	print(now)
	err = True
	while err:
		try:
			main(ini, fin)
			err = False
		except NoSuchElementException:
			err = True
			print('err')
	now = datetime.now()
	print(now)
	ini = fin

now = datetime.now()
print(now)
fin = fin+count
main(ini, fin)
now = datetime.now()
print(now)

