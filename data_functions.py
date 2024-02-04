from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def dodavanje_to_csv(folder, klub, url):
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--ignore-ssl-errors')
  driver = webdriver.Chrome(options)

  driver.get(url)

  print(driver.title)

  table = driver.find_element(By.CLASS_NAME, 'stats_table')

  rows = table.find_elements(By.TAG_NAME, 'tr')

  data=[]
  dodavanja_index=[7,8,10,25,29]
  

  for row in (rows[7:]):


      cells = row.find_elements(By.TAG_NAME, "td")
        
      row_data = []

      for index, cell in enumerate(cells):
        if index in dodavanja_index:
          cell_data=cell.text
          row_data.append(cell_data)
      
      data.append(row_data)

  with open(folder+"\dodavanja.csv", "a") as fajl:
    
    #fajl.write("naziv_kluba,naziv_protivnika,broj_dodavanja,procenat_preciznosti_dodavanja,kljucna_dodavanja,progresivna_dodavanja\n")
    for row_data in data:
      if row_data==data[-1]:
        break
      fajl.write(klub+",")
      for item in row_data:
        if item!=row_data[-1]:
          fajl.write(item+",")
        else:
          fajl.write(item)
      fajl.write("\n")


  driver.quit()

def sutevi_to_csv(folder, klub, url):
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--ignore-ssl-errors')
  driver = webdriver.Chrome(options)

  driver.get(url)

  print(driver.title)

  table = driver.find_element(By.CLASS_NAME, 'stats_table')

  rows = table.find_elements(By.TAG_NAME, 'tr')

  data=[]
  sutevi_index=[5,6,7,9,10,16,18]
  

  for row in (rows[7:]):


      cells = row.find_elements(By.TAG_NAME, "td")
        
      row_data = []

      for index, cell in enumerate(cells):
        if index in sutevi_index:
          cell_data=cell.text
          row_data.append(cell_data)
      
      data.append(row_data)

  with open(folder+"\sutevi.csv", "a") as fajl:
    
    #fajl.write("naziv_kluba,postignuti_golovi,primljeni_golovi,naziv_protivnika,sutevi_na_gol,sutevi_u_okvir_gola,broj_penala,ocekivani_broj_golova\n")
    for row_data in data:
      if row_data==data[-1]:
        break
      fajl.write(klub+",")
      for item in row_data:
        if item!=row_data[-1]:
          fajl.write(item+",")
        else:
          fajl.write(item)
      fajl.write("\n")


  driver.quit()

def statistika_to_csv(folder, klub, url):
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--ignore-ssl-errors')
  driver = webdriver.Chrome(options)

  driver.get(url)

  print(driver.title)

  table = driver.find_element(By.CLASS_NAME, 'stats_table')

  rows = table.find_elements(By.TAG_NAME, 'tr')

  data=[]
  statistika_index=[3,4,7,8]
  broj_meceva=0
  broj_pobeda=0
  broj_remija=0
  broj_poraza=0

  for row in (rows[7:]):

      broj_meceva+=1
      cells = row.find_elements(By.TAG_NAME, "td")
        
      row_data = []

      for index, cell in enumerate(cells):
        if index in statistika_index:
          cell_data=cell.text
          if cell_data=="Home":
            cell_data="1"
          if cell_data=="Away":
            cell_data="0" 
          if cell_data=="W":
            broj_pobeda+=1
            continue
          if cell_data=="D":
            broj_remija+=1
            continue
          if cell_data=="L":
            broj_poraza+=1
            continue
          row_data.append(cell_data)

      row_data.append(str(round(broj_pobeda/broj_meceva*100,2)))  
      row_data.append(str(round(broj_remija/broj_meceva*100,2)))
      row_data.append(str(round(broj_poraza/broj_meceva*100,2)))   
      data.append(row_data)
      


  with open(folder+"\statistika.csv", "a") as fajl:
    
    #fajl.write("naziv_kluba,domaci_teren,naziv_protivnika,posed_lopte,procenat_pobeda,procenat_remija,procenat_poraza\n")
    for row_data in data:
      if row_data==data[-1]:
        break
      fajl.write(klub+",")
      for item in row_data:
        if item!=row_data[-1]:
          fajl.write(item+",")
        else:
          fajl.write(item)
      fajl.write("\n")


  driver.quit()
  
  
def predikcije_to_csv(folder, klub, url):

  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--ignore-ssl-errors')
  driver = webdriver.Chrome(options)

  driver.get(url)

  wait = WebDriverWait(driver, 10)
  odds = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "oddsValueInner")))  
  clubs = driver.find_elements(By.CLASS_NAME, 'participant__participantName')
  index=0
  teams=[]
    
  for club in clubs:
    index+=1
    if index%2==1:
      clubs.remove(club)
      
  for club in clubs:
    teams.append(club.text)
    
  if teams[0]!=klub:
    teams[0], teams[1] = teams[1], teams[0]
    odds[0], odds[2] = odds[2], odds[0]
  
  line=""
  line+=teams[0]+","+teams[1]+","
  for odd in odds:
    if odd==odds[-1]:
      line+=odd.text+"\n"
    else:
      line+=odd.text+","
  
  with open(folder+"\predikcije.csv", "a") as fajl:
    fajl.write(line)
  

  







