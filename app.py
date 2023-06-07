from models import Data
from scheduler import Scheduler
from PyQt6 import QtGui, uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QPushButton, QFrame, QListWidget, QMessageBox
from frame import Draw
import sys
import json
from datetime import datetime
import os

class ClassData():
    def __init__(self, lop):
        self.lopRaw = lop
        self.Mon = lop["Mon"]
        self.Lop = lop["Lop"]
        self.TietBatDau = int(lop["TietBatDau"])
        self.TietKetThuc = int(lop["TietKetThuc"])
        self.NgayBatDay = lop["NgayBatDau"]
        self.NgayKetThuc = lop["NgayKetThuc"]
        self.thuCuaMon = lop["Thu"]
        self.Phong = lop["Phong"]
        self.GiaoVien = lop["GV"].split('-')[1]
    def __str__(self):
        data = json.dumps(self.lopRaw, indent=4, ensure_ascii=False)
        return data
    def thong_Tin_Lop(self):
        thongTinLop = "{mon}\n{tenLop}\nTiết: {tietBatDau} - {tietKetThuc}\nPhòng: {phong}\nGiáo viên: {gv}".format(mon=self.Mon, tenLop=self.Lop, tietBatDau = str(self.TietBatDau), tietKetThuc = str(self.TietKetThuc), phong=self.Phong, gv=self.GiaoVien)
        return thongTinLop
    def thoi_Gian_Tiet_Hoc(self):
        duration = self.TietKetThuc - self.TietBatDau + 1
        return duration
    def kiem_Tra_Ngay_Hoc(self, strNgayHienTai):
        ngayHienTai = datetime.strptime(strNgayHienTai, r'%d/%m/%Y')
        ngayBatDau = datetime.strptime(self.NgayBatDay, r'%d/%m/%Y')
        ngayKetThuc = datetime.strptime(self.NgayKetThuc, r'%d/%m/%Y')
        if ngayBatDau <= ngayHienTai <= ngayKetThuc:
            return True
        else:
            return False
    def kiem_Tra_Ca_Hoc(self):
        caSang = True
        caChieu = False
        tietCuoiCungBuoiSang = 6
        if self.TietBatDau <= tietCuoiCungBuoiSang:
            return caSang
        else:
            return caChieu
    def kiem_Tra_Thu_Hoc(self, thu):
        if self.thuCuaMon == thu + 2:
            return True
        else:
            return False
        
class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('design.ui', self)
        self.maLHP = self.findChild(QTextEdit, 'maLHP')
        self.btnDangKy = self.findChild(QPushButton, 'btnDangKy')
        self.btnTiep = self.findChild(QPushButton, 'btnTiep')
        self.btnTruoc = self.findChild(QPushButton, 'btnTruoc')
        self.btnXemTatCaMon = self.findChild(QPushButton, 'btnXemFullMon')

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Thông báo lỗi")
        self.msg.setIcon(QMessageBox.Icon.Critical)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.msg.setFont(font)

        self.sangThu2 = self.findChild(QFrame, 'sangThu2')
        self.sangThu3 = self.findChild(QFrame, 'sangThu3')
        self.sangThu4 = self.findChild(QFrame, 'sangThu4')
        self.sangThu5 = self.findChild(QFrame, 'sangThu5')
        self.sangThu6 = self.findChild(QFrame, 'sangThu6')
        self.sangThu7 = self.findChild(QFrame, 'sangThu7')
        self.sangChuNhat = self.findChild(QFrame, 'sangChuNhat')

        self.chieuThu2 = self.findChild(QFrame, 'chieuThu2')
        self.chieuThu3 = self.findChild(QFrame, 'chieuThu3')
        self.chieuThu4 = self.findChild(QFrame, 'chieuThu4')
        self.chieuThu5 = self.findChild(QFrame, 'chieuThu5')
        self.chieuThu6 = self.findChild(QFrame, 'chieuThu6')
        self.chieuThu7 = self.findChild(QFrame, 'chieuThu7')
        self.chieuChuNhat = self.findChild(QFrame, 'chieuChuNhat')
        
        self.WEEK = Scheduler(self)
        self.DATA = Data()
        self.DRAW = Draw()
        if not self.DATA.isExist_FileData():
            sys.exit()
        

        self.noTuan = 0
        self.danhSachLop = []
        self.danhSachHocPhan = []
        self.tuan_Hien_Tai()

        self.danhSachHocPhan = self.DATA.doc_LHP()
        self.btnDangKy.clicked.connect(self.dang_Ky_LHP)
        self.btnTiep.clicked.connect(self.tuan_Tiep_Theo)
        self.btnTruoc.clicked.connect(self.tuan_Truoc_Do)
        self.btnXemTatCaMon.clicked.connect(self.xem_Tat_Ca_Cac_Mon)
        self.show()
    def is_Empty_Danh_Sach_Hoc_Phan(self):
        if not bool(self.danhSachHocPhan):
            print("Danh sach hoc phan rong")
            return True
        else:
            return False
    def ghi_LHP(self):
        self.DATA.ghi_LHP(self.danhSachHocPhan)
    def dang_Ky_LHP(self):
        text = self.maLHP.toPlainText() 
        if str(text) == "":
            self.msg.setText("Lỗi đăng ký, vui lòng nhập lại mã học phần")
            self.msg.exec()
            return
        maLHP = int(text)
        print("Dang ky mon: ", str(maLHP))
        danhSachLop = self.DATA.danh_Sach_Hoc_Phan(maLHP)
        if self.is_Trung_Hoc_Phan(danhSachLop):
            self.msg.setText("Học phần đăng ký bị trùng lịch, nhập học phần khác")
            self.maLHP.clear()
            self.msg.exec()
            return
        self.danhSachHocPhan.append(danhSachLop)
        self.maLHP.clear()
        self.tuan_Hien_Tai()
    def is_Trung_Hoc_Phan(self, danhSachLop):
        for mahp in danhSachLop.values():
            for lop in mahp:
                lopDangKy = ClassData(lop)
                for maLHP in self.danhSachHocPhan:
                    for chiTietLop in maLHP.values():
                        for tungLop in chiTietLop:
                            lopHP = ClassData(tungLop)
                            if lopDangKy.thuCuaMon == lopHP.thuCuaMon:
                                if lopHP.TietBatDau <= lopDangKy.TietBatDau <= lopHP.TietKetThuc:
                                    if lopHP.TietBatDau <= lopDangKy.TietKetThuc <= lopHP.TietKetThuc:
                                        return True
        return False
    def tuan_Hien_Tai(self):
        self.WEEK.thay_Doi_Tuan()
        self.DRAW.xoa_Het_Lop_Hoc()
        self.lich_Hoc()
    def tuan_Tiep_Theo(self):
        self.noTuan += 1
        self.WEEK.thay_Doi_Tuan(self.noTuan)
        self.DRAW.xoa_Het_Lop_Hoc()
        self.lich_Hoc()
    def tuan_Truoc_Do(self):
        self.noTuan -= 1
        self.WEEK.thay_Doi_Tuan(self.noTuan)
        self.DRAW.xoa_Het_Lop_Hoc()
        self.lich_Hoc()
    
    def ca_Sang(self, thu, lop):
        thongTinLop = lop.thong_Tin_Lop()
        start = lop.TietBatDau
        end= lop.TietKetThuc
        match thu:
            case 0:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu2)
            case 1:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu3)
            case 2:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu4)
            case 3:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu5)
            case 4:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu6)
            case 5:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangThu7)
            case 6:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.sangChuNhat)
    def ca_Chieu(self, thu, lop):
        thongTinLop = lop.thong_Tin_Lop()
        start = lop.TietBatDau
        end= lop.TietKetThuc
        match thu:
            case 0:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuThu2)
            case 1:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuThu3)
            case 2:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuThu4)
            case 3:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuhu5)
            case 4:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuThu6)
            case 5:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuThu7)
            case 6:
                self.DRAW.ve_Lop_Hoc(thongTinLop, start, end, self.chieuChuNhat)   
    def lich_Hoc(self):
        self.cac_Ngay_Trong_Tuan = self.WEEK.cac_Ngay_Trong_Tuan(self.noTuan)
        for thu in range(0, len(self.cac_Ngay_Trong_Tuan)):
            strNgayHienTai = self.cac_Ngay_Trong_Tuan[thu] #0 la thu 2
            if self.is_Empty_Danh_Sach_Hoc_Phan():
                return
            for maLHP in self.danhSachHocPhan:
                for chiTietLop in maLHP.values():
                    for tungLop in chiTietLop:
                        lop = ClassData(tungLop)
                        if lop.kiem_Tra_Ngay_Hoc(strNgayHienTai) and lop.kiem_Tra_Thu_Hoc(thu):
                            if lop.kiem_Tra_Ca_Hoc():
                                self.ca_Sang(thu, lop)
                            else:
                                self.ca_Chieu(thu, lop)
    def xem_Tat_Ca_Cac_Mon(self):
        self.xemMon = XemFullMon(self)
        self.xemMon.show()
class XemFullMon(QMainWindow):
    def __init__(self, appMain):
        super(XemFullMon, self).__init__()
        self.app = appMain
        uic.loadUi('xemMon.ui', self)
        self.them_LHP()

        self.danhSachMHP = self.findChild(QListWidget, 'danhSachMHP')
        self.btnXoaTatCa = self.findChild(QPushButton, 'btnXoaTatCa')
        self.btnXoaMon = self.findChild(QPushButton, 'btnXoaMon')

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        self.danhSachMHP.setFont(font)

        self.btnXoaMon.clicked.connect(self.xoa1Mon)
        self.btnXoaTatCa.clicked.connect(self.xoaTatCaCacMon)
    def xoa1Mon(self):
        if self.app.is_Empty_Danh_Sach_Hoc_Phan():
            return
        row = self.danhSachMHP.currentRow()
        self.danhSachMHP.takeItem(row)
        del self.app.danhSachHocPhan[row]
        self.app.DRAW.xoa_Het_Lop_Hoc()
        self.app.lich_Hoc()
    def xoaTatCaCacMon(self):
        self.danhSachMHP.clear()
        self.app.danhSachHocPhan.clear()
        self.app.DRAW.xoa_Het_Lop_Hoc()
        self.app.lich_Hoc()
    def them_LHP(self):
        if self.app.is_Empty_Danh_Sach_Hoc_Phan():
            return
        for hocphan in self.app.danhSachHocPhan:
            for mhp in hocphan.keys():
                self.danhSachMHP.addItem(str(mhp))
        self.danhSachMHP.show()

def main():
    app = QApplication(sys.argv)
    ui = App()
    app.exec()
    ui.ghi_LHP()
main()