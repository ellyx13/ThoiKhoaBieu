import tkinter as tk
from datetime import datetime, timedelta
from PyQt6 import QtCore
from PyQt6.QtWidgets import QLabel
    
class Scheduler:
    def __init__(self, app):
        self.week_Dict = {
                    'Thu 2': 0,
                    'Thu 3': 1,
                    'Thu 4': 2,
                    'Thu 5': 3,
                    'Thu 6': 4,
                    'Thu 7': 5,
                    'Chu nhat': 6
                }
        self.lbNgayThu2 = app.findChild(QLabel, 'lbNgayThu2')
        self.lbNgayThu3 = app.findChild(QLabel, 'lbNgayThu3')
        self.lbNgayThu4 = app.findChild(QLabel, 'lbNgayThu4')
        self.lbNgayThu5 = app.findChild(QLabel, 'lbNgayThu5')
        self.lbNgayThu6 = app.findChild(QLabel, 'lbNgayThu6')
        self.lbNgayThu7 = app.findChild(QLabel, 'lbNgayThu7')
        self.lbNgayChuNhat = app.findChild(QLabel, 'lbNgayChuNhat')
        self.lbCacNgayTrongTuan = [self.lbNgayThu2, self.lbNgayThu3, self.lbNgayThu4, self.lbNgayThu5, self.lbNgayThu6, self.lbNgayThu7, self.lbNgayChuNhat]
    def cac_Ngay_Trong_Tuan(self, noTuan):
        date = datetime.now().date()
        if noTuan != 0:
            date = date + timedelta(days = noTuan*7)        
        weekday =  int(date.weekday())
        self.list_Date = []
        for key, value in self.week_Dict.items():
            if weekday >= value:
                day = weekday - value
            else:
                day = weekday - value
            day = date - timedelta(days = day)
            self.list_Date.append(day.strftime('%d/%m/%Y'))
        return self.list_Date
    def thay_Doi_Tuan(self, noTuan = 0):
        weekDate = self.cac_Ngay_Trong_Tuan(noTuan)
        i = 0
        for lb in self.lbCacNgayTrongTuan:
            lb.setText(weekDate[i])
            i += 1
            lb.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    

