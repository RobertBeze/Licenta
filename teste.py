from selenium import webdriver
import unittest
import random
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

url = "http://127.0.0.1:8000/"

def randletter(x, y):
    return chr(random.randint(ord(x), ord(y)))

def plate_generator():
    plate = ""
    judete = ["AB" ,"AG", "AR", "B", "BC", "BH", "BN", "BR", "BT", "BV", "BZ", "CJ", "CL", "CS", "CT", "CV", "DB", "DJ", "GJ", "GL", "GR", "HD",
              "HR", "IF", "IL", "IS", "MH", "MM", "MS", "NT", "OT", "PH", "SB", "SJ", "SM", "SV", "TL", "TM", "TR", "VL", "VN", "VS"]
    k = len(judete)-1
    i = random.randint(0, k)
    judet = judete[i]

    if len(judet) == 1:
        nr = random.randint(1,999)
        if nr < 10:
            sir = "00" + str(nr)
        elif nr >= 10 and nr <100:
            sir = "0" + str(nr)
        else:
            sir = str(nr)
    else:
        nr = random.randint(1,99)
        if nr<10:
            sir = "0" + str(nr)
        else:
            sir = str(nr)
    A = randletter('A', 'Z')
    B = randletter('A','Z')
    C = randletter('A','Z')
    plate = plate + judet + sir + A + B + C
    return plate


class RDFleetTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_login_method1(self):
        driver = self.driver
        driver.get(url)
        loginbtn = driver.find_element(By.ID,"loginbtn")
        loginbtn.click()

        username = driver.find_element(By.ID,"id_username")
        passwd = driver.find_element(By.ID,"id_password")
        loginsubmit = driver.find_element(By.ID, "loginsubmit")

        username.send_keys("robert")
        passwd.send_keys("18280814")
        loginsubmit.click()

        title = driver.title
        self.assertIn(title,"Home-User Home-Admin")

    def test_login_method2(self):
        driver = self.driver
        driver.get(url)
        loginbtn = driver.find_element(By.ID, "loginbtn")
        loginbtn.click()

        username = driver.find_element(By.ID, "id_username")
        passwd = driver.find_element(By.ID, "id_password")
        loginsubmit = driver.find_element(By.ID, "loginsubmit")

        username.send_keys("daniel")
        passwd.send_keys("18280814")
        loginsubmit.click()

        title = driver.title
        self.assertIn(title,"Home-User Home-Admin")

    def test_login_method3_fail(self):
        driver = self.driver
        driver.get(url)
        loginbtn = driver.find_element(By.ID, "loginbtn")
        loginbtn.click()

        username = driver.find_element(By.ID, "id_username")
        passwd = driver.find_element(By.ID, "id_password")
        loginsubmit = driver.find_element(By.ID, "loginsubmit")

        username.send_keys("robert")
        passwd.send_keys("fail")
        loginsubmit.click()

        #erori = driver.find_element(By.CLASS_NAME, "errorlist nonfield")
        li = driver.find_elements(By.TAG_NAME, "li")
        lista = []
        for k in li:
            lista.append(k.text)
        self.assertIsNot(len(lista), 0, "Eroare la autentificare {}".format(lista))
        print(lista)

    def test_add_vehicle_method1(self):
        driver = self.driver
        driver.get(url)
        loginbtn = driver.find_element(By.ID, "loginbtn")
        loginbtn.click()

        username = driver.find_element(By.ID, "id_username")
        passwd = driver.find_element(By.ID, "id_password")
        loginsubmit = driver.find_element(By.ID,"loginsubmit")

        username.send_keys("robert")
        passwd.send_keys("18280814")
        loginsubmit.click()

        title = driver.title
        self.assertIn(title,"Home-Admin", "Credentiale incorecte sau utilizator normal! Necesita drepturi de admin!")

        driver.find_element(By.ID, "vehiculebtn").click()
        title = driver.title
        self.assertIn(title,"Listă Vehicule","Eroare! Titlul paginii este incorect")

        driver.find_element(By.ID,"adaugavehiculbtn").click()
        title = driver.title
        self.assertIn(title,"Adaugă Vehicul", "Eroare! Titlul paginii trebuia sa fie Aduaga Vehicul")


        plate = driver.find_element(By.ID, "id_vehicle_plate")
        nr = plate_generator()
        plate.send_keys(nr)
        odometer = driver.find_element(By.ID, "id_vehicle_odometer")
        km = random.randint(1500, 300000)
        odometer.send_keys(km)

        itp = driver.find_element(By.ID, "id_vehicle_itp")
        itp.send_keys("23")
        itp.send_keys("10")
        itp.send_keys(Keys.ARROW_RIGHT)
        itp.send_keys("2023")

        rca = driver.find_element(By.ID, "id_vehicle_rca")
        rca.send_keys("23")
        rca.send_keys("10")
        rca.send_keys(Keys.ARROW_RIGHT)
        rca.send_keys("2023")

        service = driver.find_element(By.ID, "id_vehicle_last_service")
        km = km - 1000
        service.send_keys(km)



        buton = driver.find_element(By.ID, "salveaza")
        buton.click()

        title = driver.title
        self.assertIn(title,nr,"Eroare la submiterea formularului!")

    def test_add_vehicle_method2(self):
        driver = self.driver
        driver.get(url)
        loginbtn = driver.find_element(By.ID, "loginbtn")
        loginbtn.click()

        username = driver.find_element(By.ID, "id_username")
        passwd = driver.find_element(By.ID, "id_password")
        loginsubmit = driver.find_element(By.ID, "loginsubmit")

        username.send_keys("robert")
        passwd.send_keys("18280814")
        loginsubmit.click()

        title = driver.title
        self.assertIn(title, "Home-Admin", "Credentiale incorecte sau utilizator normal! Necesita drepturi de admin!")

        driver.find_element_by_id("vehiculebtn").click()
        title = driver.title
        self.assertIn(title, "Listă Vehicule", "Eroare! Titlul paginii este incorect")

        driver.find_element(By.ID, "adaugavehiculbtn").click()
        title = driver.title
        self.assertIn(title, "Adaugă Vehicul", "Eroare! Titlul paginii trebuia sa fie Aduaga Vehicul")

        plate = driver.find_element(By.ID, "id_vehicle_plate")
        nr = "MH23RXR"
        plate.send_keys(nr)
        odometer = driver.find_element(By.ID, "id_vehicle_odometer")
        km = random.randint(1500, 300000)
        odometer.send_keys(km)

        itp = driver.find_element(By.ID, "id_vehicle_itp")
        itp.send_keys("23")
        itp.send_keys("10")
        itp.send_keys(Keys.ARROW_RIGHT)
        itp.send_keys("2023")

        rca = driver.find_element(By.ID, "id_vehicle_rca")
        rca.send_keys("23")
        rca.send_keys("10")
        rca.send_keys(Keys.ARROW_RIGHT)
        rca.send_keys("2023")

        service = driver.find_element(By.ID, "id_vehicle_last_service")
        km = km + 1000
        service.send_keys(km)

        buton = driver.find_element(By.ID, "salveaza")
        buton.click()

        lista_erori = driver.find_elements(By.CLASS_NAME, "errorlist")
        lista = []
        for x in lista_erori:
            items = x.find_elements(By.TAG_NAME, "li")
            for k in items:
                lista.append(k.text)

        self.assertIsNot(len(lista), 0, "Erori la submiterea formularului: {}".format(lista))
        print(lista)


    def tearDown(self):
        self.driver.close()



if __name__=="__main__":
    unittest.main()
