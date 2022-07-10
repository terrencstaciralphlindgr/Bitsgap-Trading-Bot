import csv
import sys
from datetime import datetime
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtGui import QDoubleValidator
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

class ExtractingBot(QObject):
    progress = pyqtSignal(list, list, bool)
    finished = pyqtSignal()
    is_closing = False
    close_list = []

    def run(self):
        login_file = open('login.txt', 'r')
        info = login_file.read()
        email = info.split(':')[0].strip()
        password = info.split(':')[1].strip()
        login_file.close()

        login_url = 'https://bitsgap.com/sign-in?d=app'

        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        driver.get(login_url)

        # Login
        self.progress.emit(['Signing to Bitsgap...'], [0], False)
        while True:
            try:
                email_input = driver.find_element(By.ID, 'email')
                password_input = driver.find_element(By.ID, 'password')

                email_input.clear()
                password_input.clear()

                ac = ActionChains(driver)
                ac.move_to_element(email_input)
                sleep(0.5)
                ac.click()
                sleep(0.5)
                ac.send_keys(email)
                sleep(2)
                ac.move_to_element(password_input)
                sleep(0.5)
                ac.click()
                sleep(0.5)
                ac.send_keys(password)
                sleep(2)
                ac.perform()
                password_input.submit()
            except StaleElementReferenceException:
                continue
            
            break
        self.progress.emit([f'Signed as {email}'], [0], False)

        # Switch to demo
        self.progress.emit(['Switching to demo...'], [0], False)
        sleep(5)
        driver.get('https://app.bitsgap.com/my-exchanges')
        driver.find_elements(By.CLASS_NAME, 'RX0wjSyh4wgkc8ZhpkRW')[-1].click()

        # Extract table
        sleep(3)

        self.progress.emit(['Switched to demo'], [0], False)

        driver.get('https://app.bitsgap.com/bot')

        self.progress.emit(['Loading finished!'], [0], False)

        while True:
            if not self.is_closing:
                self.progress.emit(['Extracting change...'], [0], False)

                self.extract(driver)
                sleep(10)
            else:
                self.progress.emit(["Closing pairs..."], [0], False)

                self.closePair(driver)

                self.is_closing = False

    def setClose(self, pairs):
        self.is_closing = True
        self.close_list = pairs

    def closePair(self, driver):
        while True:
            is_closed = False
            pairs = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'MuiTableRow-root')))[1:]

            for pair in pairs:
                is_closed = False
                cells = pair.find_elements(By.CLASS_NAME, 'MuiTableCell-root')

                name = cells[1].find_element(By.CLASS_NAME, 'two-row-cell').find_element(By.TAG_NAME, 'div').text.replace(' / ', '')

                for pair_name in self.close_list:
                    if name == pair_name:
                        driver.execute_script("arguments[0].click();", cells[-1].find_elements(By.TAG_NAME, 'button')[-1])
                        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//button[@class="aQXLoSia4k1esjIDAFwW zhVSsYrxjm8vd8ihxSUs MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButtonBase-root  css-pev4aq"]'))
                        driver.execute_script("arguments[0].click();", driver.find_elements(By.XPATH, '//li[@class="yh3uTjDDJTvbuAZD9i_M jj5mPys2QhRB6omDdQP4 MuiMenuItem-root MuiMenuItem-gutters MuiButtonBase-root css-17cm1p2"]')[1])
                        confirm = driver.find_element(By.XPATH, '//button[@data-test="bot-preview-confirm-button"]')
                        driver.execute_script("arguments[0].click();", confirm)

                        is_closed = True
                        
                        sleep(5)

                        break

                if is_closed:
                    break

            if is_closed:
                continue
            else:
                break

    def extract(self, driver):
        try:
            pairs = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'MuiTableRow-root')))[1:]
        except:
            self.progress.emit(["No pairs"], [0], False)
            return

        pair_list = []
        change_list = []

        for pair in pairs:
            cells = pair.find_elements(By.CLASS_NAME, 'MuiTableCell-root')

            name = cells[1].find_element(By.CLASS_NAME, 'two-row-cell').find_element(By.TAG_NAME, 'div').text.replace(' / ', '')
            change = float(cells[3].text[:-1])

            pair_list.append(name)
            change_list.append(change)

        self.progress.emit(pair_list, change_list, True)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.mt_profit.setValidator(QDoubleValidator())
        self.mt_stoploss.setValidator(QDoubleValidator())

        # self.initMT()
        # self.initST()

        self.statusBar.showMessage('Loading...')

        self.extracting_bot_thread = QThread(self)
        self.extracting_bot_worker = ExtractingBot()
        self.extracting_bot_worker.moveToThread(self.extracting_bot_thread)
        self.extracting_bot_thread.started.connect(self.extracting_bot_worker.run)
        self.extracting_bot_worker.progress.connect(self.updateStatus)
        self.extracting_bot_worker.finished.connect(self.extracting_bot_thread.quit)
        self.extracting_bot_worker.finished.connect(self.extracting_bot_worker.deleteLater)
        self.extracting_bot_thread.finished.connect(self.extracting_bot_thread.deleteLater)
        self.extracting_bot_thread.start()

        self.show()

    def updateStatus(self, message, value, state):
        if not state:
            self.statusBar.showMessage(''.join(message))

            if ''.join(message) == 'Loading finished!':
                self.setEnabled(True)
        else:
            status = []
            
            for index in range(len(message)):
                status.append(f'{message[index]}:{value[index]}')

            self.statusBar.showMessage(' '.join(status))

            self.updateMT(message, value)

            if not self.extracting_bot_worker.is_closing:
                self.updateST(message, value)

    def initMT(self):
        mt_pair_file = open('multiple.txt', 'r')
        mt_pairs = mt_pair_file.readlines()
        
        for index in range(len(mt_pairs)):
            self.mt_table.setItem(index, 0, QtWidgets.QTableWidgetItem(mt_pairs[index].strip()))
        
        mt_pair_file.close()

    def initST(self):
        st_pair_file = open('single.txt', 'r')
        st_pairs = st_pair_file.readlines()
        
        for index in range(len(st_pairs)):
            self.st_table.setItem(index, 0, QtWidgets.QTableWidgetItem(st_pairs[index].strip()))
        
        st_pair_file.close()

    def updateMT(self, pairs, changes):
        row_count = self.mt_table.rowCount()
        existing_changes = []
        existing_pairs = []
        collective = 0
        
        for row_index in range(row_count):
            item = self.mt_table.item(row_index, 0)
            
            if item:
                if item.text() in pairs:
                    self.mt_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(changes[pairs.index(item.text())])))
                    existing_pairs.append(item.text())
                    existing_changes.append(changes[pairs.index(item.text())])
                else:
                    self.mt_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('0.00'))

        if len(existing_changes) > 0:
            collective = sum(existing_changes) / len(existing_changes)
            self.mt_collective.setText("{:.2f}".format(collective))

        st = float(self.mt_stoploss.text())
        tp = float(self.mt_profit.text())

        if collective <= st:
            self.extracting_bot_worker.setClose(existing_pairs)

        if collective >= tp:
            self.extracting_bot_worker.setClose(existing_pairs)

    def updateST(self, pairs, changes):
        row_count = self.st_table.rowCount()
        delete_pairs = []
        
        for row_index in range(row_count):
            item = self.st_table.item(row_index, 0)
            
            if item:
                if item.text() in pairs:
                    self.st_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(changes[pairs.index(item.text())])))

                    change = changes[pairs.index(item.text())]
                    tp = self.st_table.item(row_index, 2)
                    sl = self.st_table.item(row_index, 3)

                    if tp and sl:
                        if change >= float(tp.text()) or change <= float(sl.text()):
                            delete_pairs.append(item.text())
                else:
                    self.st_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('0.00'))

        self.extracting_bot_worker.setClose(delete_pairs)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec()
