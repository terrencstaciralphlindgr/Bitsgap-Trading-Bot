import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as md
import winsound
import pandas as pd
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import HourLocator, MinuteLocator, SecondLocator
# from playsound import playsound
from openpyxl import load_workbook, Workbook
from datetime import datetime
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QObject, Qt
from PyQt6.QtGui import QDoubleValidator
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep

def alarm():
    duration = 500
    freq = 750

    for _ in range(3):
        winsound.Beep(freq, duration)

try:
    wb = load_workbook('Closed Trades.xlsx')
    ws = wb.worksheets[0]
except FileNotFoundError:
    headers_row = ["Pair", "Category", "Date", "Time", "Change % on closure", "Close Condition", "TP", "SL", "Collective"]
    wb = Workbook()
    ws = wb.active
    ws.append(headers_row)

track = {
    'MT': [],
    'ST': []
}

bot_start_date = datetime.today()
chart_dir = 'charts'

if not os.path.exists(chart_dir):
    os.mkdir(chart_dir)

class ExtractingBot(QObject):
    progress = pyqtSignal(list, list, bool)
    finished = pyqtSignal()
    is_mt_closing = False
    is_st_closing = False
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
            try:
                if not self.is_mt_closing and not self.is_st_closing:
                    self.progress.emit(['Extracting change...'], [0], False)

                    self.extract(driver)
                    sleep(10)
                else:
                    self.progress.emit(["Closing pairs..."], [0], False)

                    self.closePair(driver)

                    if self.is_mt_closing:
                        self.is_mt_closing = False
                    elif self.is_st_closing:
                        self.is_st_closing = False
            except:
                pass

    def setClose(self, pairs, is_mt):
        if is_mt:
            self.is_mt_closing = True
        else:
            self.is_st_closing = True

        self.close_list = pairs

    def closePair(self, driver):
        while True:
            is_closed = False

            try:
                pairs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'MuiTableRow-root')))[1:]
            except TimeoutException:
                pairs = []
                
            for pair in pairs:
                is_closed = False
                cells = pair.find_elements(By.CLASS_NAME, 'MuiTableCell-root')

                name = cells[1].find_element(By.CLASS_NAME, 'two-row-cell').find_element(By.TAG_NAME, 'div').text.replace(' / ', '/')

                for pair_name in self.close_list:
                    if name == pair_name:
                        try:
                            driver.execute_script("arguments[0].click();", cells[-1].find_elements(By.TAG_NAME, 'button')[-1])
                            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//button[@class="aQXLoSia4k1esjIDAFwW zhVSsYrxjm8vd8ihxSUs MuiButton-root MuiButton-text MuiButton-textPrimary MuiButton-sizeMedium MuiButton-textSizeMedium MuiButtonBase-root  css-pev4aq"]'))
                            driver.execute_script("arguments[0].click();", driver.find_elements(By.XPATH, '//li[@class="yh3uTjDDJTvbuAZD9i_M jj5mPys2QhRB6omDdQP4 MuiMenuItem-root MuiMenuItem-gutters MuiButtonBase-root css-17cm1p2"]')[1])
                            confirm = driver.find_element(By.XPATH, '//button[@data-test="bot-preview-confirm-button"]')
                            driver.execute_script("arguments[0].click();", confirm)
                        except:
                            pass

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
        pairs = driver.find_elements(By.CLASS_NAME, 'MuiTableRow-root')[1:]

        if len(pairs) > 0:
            pair_list = []
            change_list = []

            for pair in pairs:
                cells = pair.find_elements(By.CLASS_NAME, 'MuiTableCell-root')

                name = cells[1].find_element(By.CLASS_NAME, 'two-row-cell').find_element(By.TAG_NAME, 'div').text.replace(' / ', '/')
                change = float(cells[3].text[:-1])

                pair_list.append(name)
                change_list.append(change)

            self.progress.emit(pair_list, change_list, True)
        else:
            self.progress.emit([], [], True)
            self.progress.emit(["No pairs"], [0], False)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.mt_profit.setValidator(QDoubleValidator())
        self.mt_stoploss.setValidator(QDoubleValidator())
        self.mt_viewchart.clicked.connect(self.viewMTChart)
        self.mt_clearchart.clicked.connect(self.clearMTChart)

        # self.initMT()
        # self.initSL()

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

    def keyPressEvent(self, event):
        widget = QtWidgets.QApplication.focusWidget()
        
        if widget.objectName() == 'auto_restart_table' or widget.objectName() == 'mt_table' or widget.objectName() == 'st_table':
            if event.key() == Qt.Key.Key_V:
                try:
                    clipboard = pd.read_clipboard(sep=r'\s+', header=None)
                except:
                    clipboard = pd.DataFrame()
                clipboard.fillna('0', inplace=True)

                clip_rows = len(clipboard)
                clip_cols = len(clipboard.columns)

                for row_index in range(clip_rows):
                    for col_index in range(clip_cols):
                        try:
                            widget.setItem(widget.selectedIndexes()[0].row()+row_index, widget.selectedIndexes()[0].column()+col_index, QtWidgets.QTableWidgetItem(str(clipboard.iat[row_index, col_index])))
                        except:
                            pass
            elif event.key() == Qt.Key.Key_Delete:
                for index in widget.selectedIndexes():
                    widget.setItem(index.row(), index.column(), QtWidgets.QTableWidgetItem(''))

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

            if not self.extracting_bot_worker.is_mt_closing:
                self.updateST(message, value)

    def clearMTChart(self):
        global track
        track['MT'] = []

    def viewMTChart(self, is_export=False):
        graphs = {}
        tp = []
        sl = []
        timestamps = []

        if len(track['MT']) > 0:
            for key in track['MT'][-1].keys():
                if key != "Exist" and key != 'timestamp':
                    graphs[key] = []

            for index in range(len(track['MT'])):
                if track['MT'][index]['Exist']:
                    timestamps.append(track['MT'][index]['timestamp'])
                    tp.append(float(self.mt_profit.text()))
                    sl.append(float(self.mt_stoploss.text()))
                    for key in graphs.keys():
                        try:
                            graphs[key].append(track['MT'][index][key])
                        except:
                            graphs[key].append(0)

            plt.figure('Multiple chart')

            datenums = md.date2num(timestamps)

            ax = plt.gca()
            xfmt = md.DateFormatter('%m-%d %H:%M:%S')
            # plt.xlim(datetime(bot_start_date.year, bot_start_date.month, bot_start_date.day, 0, 0, 0), datetime(datetime.today().year, datetime.today().month, datetime.today().day, 23, 59, 59))
            ax.xaxis.set_major_formatter(xfmt)
            # ax.xaxis.set_major_locator(SecondLocator(bysecond=range(60), interval=10, tz=None))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            
            plt.xticks(rotation=25)

            for key in graphs.keys():
                if key != "collective":
                    plt.plot(datenums, graphs[key], label=key)

            plt.plot(datenums, graphs['collective'], label='collective', linewidth=4)
            plt.plot(datenums, tp, label='TP', linewidth=4)
            plt.plot(datenums, sl, label='SL', linewidth=4)

            plt.legend(loc='lower right')
            plt.grid()

            if is_export:
                fname = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png'
                plt.savefig(os.path.join(chart_dir, fname))
            else:
                plt.show()
            
    def viewSTChart(self, is_export=False, r_index=0):
        graph = []
        tp = []
        sl = []
        timestamps = []

        if not is_export:
            button = QtWidgets.QApplication.focusWidget()
            index = self.st_table.indexAt(button.pos())

            if index.isValid():
                row_index = index.row()
        else:
            row_index = r_index

        pair = self.st_table.item(row_index, 0).text()

        for index in range(len(track['ST'])):
            if pair in track['ST'][index].keys():
                try:
                    tp.append(float(self.st_table.item(row_index, 2).text()))
                except:
                    tp.append(0)

                try:
                    sl.append(float(self.st_table.item(row_index, 3).text()))
                except:
                    sl.append(0)

                timestamps.append(track['ST'][index]['timestamp'])
                graph.append(track['ST'][index][pair])

        if len(graph) > 0:
            plt.figure(pair)

            datenums = md.date2num(timestamps)

            ax = plt.gca()
            xfmt = md.DateFormatter('%m-%d %H:%M:%S')
            ax.xaxis.set_major_formatter(xfmt)
            # plt.xlim(datetime(bot_start_date.year, bot_start_date.month, bot_start_date.day, 0, 0, 0), datetime(datetime.today().year, datetime.today().month, datetime.today().day, 23, 59, 59))
            # ax.xaxis.set_major_locator(SecondLocator(bysecond=range(60), interval=10, tz=None))
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

            plt.xticks(rotation=25)

            plt.plot(datenums, graph, label=pair)
            plt.plot(datenums, tp, label='TP', linewidth=4)
            plt.plot(datenums, sl, label='SL', linewidth=4)
            plt.legend(loc='lower right')
            plt.grid()

            if is_export:
                fname = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png'
                plt.savefig(os.path.join(chart_dir, fname))
            else:
                plt.show()

    def clearSTChart(self, is_export=False, r_index=0):
        if not is_export:
            button = QtWidgets.QApplication.focusWidget()
            index = self.st_table.indexAt(button.pos())

            if index.isValid():
                row_index = index.row()
        else:
            row_index = r_index

        pair = self.st_table.item(row_index, 0).text()

        for step in track['ST']:
            if pair in step.keys():
                step.pop(pair, None)

    def updateMT(self, pairs, changes):
        row_count = self.mt_table.rowCount()
        existing_changes = []
        existing_pairs = []
        collective = 0
        global track
        data = {
            'Exist': False
        }
        
        for row_index in range(row_count):
            item = self.mt_table.item(row_index, 0)
            
            if item:
                if item.text() != "" and item.text() in pairs:
                    self.mt_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(changes[pairs.index(item.text())])))
                    data[item.text()] = changes[pairs.index(item.text())]
                    data['Exist'] = True
                    existing_pairs.append(item.text())
                    existing_changes.append(changes[pairs.index(item.text())])
                else:
                    self.mt_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(''))

        if len(existing_changes) > 0:
            collective = sum(existing_changes) / len(existing_changes)

        self.mt_collective.setText("{:.2f}".format(collective))
        data['collective'] = collective
        data['timestamp'] = datetime.now()

        track['MT'].append(data)

        if self.mt_stoploss.text() != "" and self.mt_profit.text() != "" and self.mt_stoploss.text() != "." and self.mt_profit.text() != ".":
            sl = float(self.mt_stoploss.text())
            tp = float(self.mt_profit.text())

            if collective <= sl:
                alarm()
                for pair in existing_pairs:
                    for row_index in range(self.mt_table.rowCount()):
                        if self.mt_table.item(row_index, 0):
                            if self.mt_table.item(row_index, 0).text() == pair:
                                self.viewMTChart(is_export=True)
                                log_data = [pair, "multiple"]

                                current_datetime = datetime.now()

                                current_date = current_datetime.strftime('%Y-%m-%d')
                                current_time = current_datetime.strftime('%H:%M:%S')

                                log_data.append(current_date)
                                log_data.append(current_time)
                                log_data.append(float(self.mt_table.item(row_index, 1).text()))
                                log_data.append("Hit SL")
                                log_data.append(tp)
                                log_data.append(sl)
                                log_data.append(collective)

                                ws.append(log_data)
                                wb.save('Closed Trades.xlsx')

                                for col_index in range(2):
                                    self.mt_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(''))

                self.extracting_bot_worker.setClose(existing_pairs, True)
            elif collective >= tp:
                alarm()
                for pair in existing_pairs:
                    for row_index in range(self.mt_table.rowCount()):
                        if self.mt_table.item(row_index, 0):
                            if self.mt_table.item(row_index, 0).text() == pair:
                                self.viewMTChart(is_export=True)
                                log_data = [pair, "multiple"]

                                current_datetime = datetime.now()

                                current_date = current_datetime.strftime('%Y-%m-%d')
                                current_time = current_datetime.strftime('%H:%M:%S')

                                log_data.append(current_date)
                                log_data.append(current_time)
                                log_data.append(float(self.mt_table.item(row_index, 1).text()))
                                log_data.append("Hit TP")
                                log_data.append(tp)
                                log_data.append(sl)
                                log_data.append(collective)

                                ws.append(log_data)
                                wb.save('Closed Trades.xlsx')

                                for col_index in range(2):
                                    self.mt_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(''))

                self.extracting_bot_worker.setClose(existing_pairs, True)

    def updateST(self, pairs, changes):
        row_count = self.st_table.rowCount()
        delete_pairs = []
        global track
        data = {
            'Exist': False
        }
        
        for row_index in range(row_count):
            item = self.st_table.item(row_index, 0)
            
            if item:
                if item.text() != "" and item.text() in pairs:
                    chart_btn = QtWidgets.QPushButton("Show")
                    chart_btn.clicked.connect(self.viewSTChart)

                    clear_btn = QtWidgets.QPushButton("Clear")
                    clear_btn.clicked.connect(self.clearSTChart)

                    self.st_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(changes[pairs.index(item.text())])))
                    self.st_table.setCellWidget(row_index, 4, chart_btn)
                    self.st_table.setCellWidget(row_index, 5, clear_btn)

                    data[item.text()] = changes[pairs.index(item.text())]
                    data['Exist'] = True
                    change = changes[pairs.index(item.text())]
                    tp = self.st_table.item(row_index, 2)
                    sl = self.st_table.item(row_index, 3)

                    if tp and sl:
                        if tp.text() != "" and tp.text() != "." and sl.text() != "" and sl.text() != ".":
                            if change >= float(tp.text()) or change <= float(sl.text()):
                                alarm()
                                delete_pairs.append(item.text())
                else:
                    for col_index in range(1, 4):
                        self.st_table.setItem(row_index, col_index, None)
                    
                    self.st_table.setCellWidget(row_index, 4, None)
                    self.st_table.setCellWidget(row_index, 5, None)

        data['timestamp'] = datetime.now()
        track['ST'].append(data)

        if len(delete_pairs) > 0:
            for pair in delete_pairs:
                for row_index in range(self.st_table.rowCount()):
                    if self.st_table.item(row_index, 0):
                        if self.st_table.item(row_index, 0).text() == pair:
                            self.viewSTChart(is_export=True, r_index=row_index)
                            log_data = [pair, "single"]

                            current_datetime = datetime.now()

                            current_date = current_datetime.strftime('%Y-%m-%d')
                            current_time = current_datetime.strftime('%H:%M:%S')

                            log_data.append(current_date)
                            log_data.append(current_time)

                            change = float(self.st_table.item(row_index, 1).text())
                            tp = float(self.st_table.item(row_index, 2).text())
                            sl = float(self.st_table.item(row_index, 3).text())

                            log_data.append(change)

                            if change >= tp:
                                log_data.append("Hit TP")
                                log_data.append(tp)
                                log_data.append(sl)
                            elif change <= sl:
                                log_data.append("Hit SL")
                                log_data.append(tp)
                                log_data.append(sl)

                            ws.append(log_data)
                            wb.save('Closed Trades.xlsx')

                            for col_index in range(4):
                                self.st_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(''))

                            self.st_table.setCellWidget(row_index, 4, None)
                            self.st_table.setCellWidget(row_index, 5, None)

            self.extracting_bot_worker.setClose(delete_pairs, False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec()

    wb.close()
