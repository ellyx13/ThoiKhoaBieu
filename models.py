import pandas as pd
import json
from os import path, stat
from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtGui

class Data:
    def __init__(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Thông báo lỗi")
        self.msg.setIcon(QMessageBox.Icon.Critical)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.msg.setFont(font)
    def format_Hoc_Phan(self, data):
        danhSachHocPhan = []
        hocPhan = {}
        maLHP = ''
        for index, row in data.iterrows():
            mon = row["Subject"]
            lop = row["Class"]
            thu = row["Day"]
            tietBatDau = row["Start_Period"]
            tietKetThuc = row["End_Period"]
            ngayBatDau = row["Begin_Day"]
            ngayKetThuc = row["End_Day"]
            phong = row["Room"]
            giaoVien = row["Teacher"]
            maLHP = row["ID_LHP"]
            thongTinHocPhan = {
                        'Mon': mon,
                        'Lop': lop,
                        'Thu': thu,
                        'TietBatDau': tietBatDau,
                        'TietKetThuc': tietKetThuc,
                        'NgayBatDau': ngayBatDau,
                        'NgayKetThuc': ngayKetThuc,
                        'Phong': phong,
                        'GV': giaoVien
                    }
            danhSachHocPhan.append(thongTinHocPhan)
        hocPhan = {
            int(maLHP): danhSachHocPhan
        }
        return hocPhan
    def format_Excel(self):
        excel_File = 'data.xlsx'
        file_Format = 'Data_Formated.xlsx'
        if not self.isExist_FileData():
            return
        df = pd.read_excel(excel_File)
        df = df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        df.columns = ["STT", "ID_LHP", "Subject", "STC", "Class", "Day", "Start_Period", "End_Period", "Type_Class", "Begin_Day", "End_Day", "Room", "Teacher"]
        df.reset_index(drop=True, inplace=True)
        df.to_excel(file_Format, index = False)
    def isExist_FileData(self):
        excel_File = 'data.xlsx'
        isExistData = path.exists(excel_File)
        file_Format = 'Data_Formated.xlsx'
        isExistDataFormat = path.exists(file_Format)
        if not isExistDataFormat: 
            if not isExistData:
                self.msg.setText("Không có file data.xlsx. Vui lòng đổi tên file excel thành data.xlsx và đăng cùng thư mục với chương trình")
                self.msg.exec()
                return False
        return True
    def isExist_FileExcelFormat(self):
        file_Excel = 'Data_Formated'
        isExist = path.exists(file_Excel)
        if isExist:
            return True
        else:
            return False
    def danh_Sach_Hoc_Phan(self, maLHP):
        if not self.isExist_FileExcelFormat: 
            self.format_Excel()
        excel_File = 'Data_Formated.xlsx'
        df = pd.read_excel(excel_File)
        data = df.loc[df['ID_LHP'] == maLHP]
        lhp = self.format_Hoc_Phan(data)
        return lhp
    def ghi_LHP(self, danhSachHocPhan):
        with open('data.json', 'w', encoding='utf8') as json_file:
            data = json.dumps(danhSachHocPhan, indent=4, ensure_ascii=False)
            json_file.write(data)
            json_file.close()
    def doc_LHP(self):
        file_LHP = 'data.json'
        isExist = path.exists(file_LHP)
        isEmpty = 10
        if isExist:
            if stat(file_LHP).st_size <= isEmpty:
                print('File rong')
            else:
                with open(file_LHP, 'r', encoding="utf8") as file:
                    data_Json = json.load(file)
                    file.close()
                    return data_Json
        else:
            print("Khong co file data.json")
        return list()



