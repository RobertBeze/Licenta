from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "http://127.0.0.1:8000/"
driver = webdriver.Chrome()


def login(usr, pwd):
    print("Starting login test")
    driver.find_element_by_id("loginbtn").click()
    username = driver.find_element_by_id("id_username")
    passwd = driver.find_element_by_id("id_password")
    username.send_keys(usr)
    passwd.send_keys(pwd)
    driver.find_element_by_id("loginsubmit").click()

    title = driver.title
    print(title)

    if title == "Home-Admin" or title == "Home-User":
        print("User is logged in")
    else:
        print("Eroare login! Incearca din nou!")
        driver.get(url)
        login()

def main():
    print("Test Started!")
    driver.maximize_window()
    driver.get(url)
    login("robert", "ceva")
    driver.close()



if __name__=="__main__":
    main()