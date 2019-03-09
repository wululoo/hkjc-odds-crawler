import sys
from PyQt5 import QtWidgets, QtCore
from crawler import *

class LeagueSelectionPanel(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.checkboxes = {
            'ACL': ['90', QtWidgets.QCheckBox('Asian Champions League')],
            'AD1': ['89', QtWidgets.QCheckBox('Australian Division 1')],
            'APL': ['94', QtWidgets.QCheckBox('Argentine Division 1')],
            'AGC': ['117', QtWidgets.QCheckBox('Argentine Cup')],
            'ASC': ['47', QtWidgets.QCheckBox('Asian Cup')],
            'BPC': ['118', QtWidgets.QCheckBox('Brazilian Paulista League')],
            'BD1': ['56', QtWidgets.QCheckBox('Brazilian Division 1')],
            'BFL': ['33', QtWidgets.QCheckBox('Belgian Division 1')],
            'BFC': ['38', QtWidgets.QCheckBox('Belgian Cup')],
            'CD1': ['123', QtWidgets.QCheckBox('Chilean Division 1')],
            'CLB': ['72', QtWidgets.QCheckBox('Other Matches')],
            'CNC': ['100', QtWidgets.QCheckBox('Central and North American Cup')],
            'CWP': ['67', QtWidgets.QCheckBox('Club World Cup')],
            'DFL': ['16', QtWidgets.QCheckBox('Dutch Division 1')],
            'DF2': ['104', QtWidgets.QCheckBox('Dutch Division 2')],
            'DAC': ['39', QtWidgets.QCheckBox('Dutch Cup')],
            'EPL': ['1', QtWidgets.QCheckBox('English Premier')],
            'ED1': ['29', QtWidgets.QCheckBox('English Championship')],
            'ED2': ['30', QtWidgets.QCheckBox('English League 1')],
            'ED3': ['101', QtWidgets.QCheckBox('English League 2')],
            'EFA': ['5', QtWidgets.QCheckBox('English FA Cup')],
            'ELC': ['8', QtWidgets.QCheckBox('English League Cup')],
            'ELT': ['99', QtWidgets.QCheckBox('English League Trophy')],
            'FF2': ['103', QtWidgets.QCheckBox('French Division 2')],
            'FFA': ['35', QtWidgets.QCheckBox('French FA Cup')],
            'FFC': ['28', QtWidgets.QCheckBox('French League Cup')],
            'FFL': ['14', QtWidgets.QCheckBox('French Division 1')],
            'GD2': ['54', QtWidgets.QCheckBox('German Division 2')],
            'GSC': ['11', QtWidgets.QCheckBox('German Cup')],
            'GSL': ['3', QtWidgets.QCheckBox('German Division 1')],
            'IFC': ['9', QtWidgets.QCheckBox('Italian Cup')],
            'ISA': ['2', QtWidgets.QCheckBox('Italian Division 1')],
            'ISC': ['51', QtWidgets.QCheckBox('Italian Super Cup')],
            'JD1': ['55', QtWidgets.QCheckBox('Japanese Division 1')],
            'JD2': ['87', QtWidgets.QCheckBox('Japanese Division 2')],
            'JEC': ['75', QtWidgets.QCheckBox('Emperors Cup')],
            'JSC': ['70', QtWidgets.QCheckBox('Japanese Super Cup')],
            'KD1': ['88', QtWidgets.QCheckBox('Korean Division 1')],
            'KFA': ['148', QtWidgets.QCheckBox('Korean FA Cup')],
            'LBC': ['71', QtWidgets.QCheckBox('Copa Libertadores')],
            'MLS': ['79', QtWidgets.QCheckBox('US Football League')],
            'MXL': ['124', QtWidgets.QCheckBox('Mexican Premier')],
            'MXC': ['127', QtWidgets.QCheckBox('Mexican Cup')],
            'NTL': ['59', QtWidgets.QCheckBox('Norwegian Division 1')],
            'NWC': ['83', QtWidgets.QCheckBox('Norwegian Cup')],
            'PFL': ['17', QtWidgets.QCheckBox('Portuguese Premier')],
            'PFC': ['40', QtWidgets.QCheckBox('Portuguese Cup')],
            'PLC': ['86', QtWidgets.QCheckBox('Portuguese League Cup')],
            'RPL': ['122', QtWidgets.QCheckBox('Russian Premier')],
            'RFC': ['126', QtWidgets.QCheckBox('Russian Cup')],
            'SAC': ['106', QtWidgets.QCheckBox('South American Cup')],
            'SEC': ['91', QtWidgets.QCheckBox('South East Asian Championship')],
            'SFA': ['37', QtWidgets.QCheckBox('Scottish FA Cup')],
            'SFC': ['10', QtWidgets.QCheckBox('Spanish Cup')],
            'SFL': ['4', QtWidgets.QCheckBox('Spanish Division 1')],
            'SLC': ['36', QtWidgets.QCheckBox('Scottish League Cup')],
            'SPL': ['15', QtWidgets.QCheckBox('Scottish Premier')],
            'UCL': ['6', QtWidgets.QCheckBox('UEFA Champions League')],
            'UEC': ['7', QtWidgets.QCheckBox('UEFA Europa League')]}

        vbox = QtWidgets.QVBoxLayout()
        for l in self.checkboxes:
            vbox.addWidget(self.checkboxes[l][1])
        # vbox.addWidget(self.checkboxes['EPL'][1])
        # vbox.setWidth(150)

        self.setLayout(vbox)
        # self.show()


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):

        self.checked_matches = []

        self.match_table = QtWidgets.QTableWidget()
        self.match_table.setFixedWidth(1000)
        self.match_table.setColumnCount(7)
        self.match_table.setColumnWidth(0, 100)
        self.match_table.setColumnWidth(1, 75)
        self.match_table.setColumnWidth(2, 75)
        self.match_table.setColumnWidth(3, 200)
        self.match_table.setColumnWidth(4, 200)
        self.match_table.setColumnWidth(5, 200)
        self.match_table.setColumnWidth(6, 50)
        self.match_table.setHorizontalHeaderLabels(['ID', 'Date', 'Time', 'League', 'Home Team', 'Away Team', 'Export']) 
        self.match_table.verticalHeader().setVisible(False)
        self.match_table.horizontalHeader().setSectionResizeMode(2)

        self.export_btn = QtWidgets.QPushButton('Export')
        self.export_btn.released.connect(
                lambda: self.saveFileDialog(self.match_table))

        self.checkboxes = {
            'ACL': ['90', QtWidgets.QCheckBox('Asian Champions League')],
            'AD1': ['89', QtWidgets.QCheckBox('Australian Division 1')],
            'APL': ['94', QtWidgets.QCheckBox('Argentine Division 1')],
            'AGC': ['117', QtWidgets.QCheckBox('Argentine Cup')],
            'ASC': ['47', QtWidgets.QCheckBox('Asian Cup')],
            'BPC': ['118', QtWidgets.QCheckBox('Brazilian Paulista League')],
            'BD1': ['56', QtWidgets.QCheckBox('Brazilian Division 1')],
            'BFL': ['33', QtWidgets.QCheckBox('Belgian Division 1')],
            'BFC': ['38', QtWidgets.QCheckBox('Belgian Cup')],
            'CD1': ['123', QtWidgets.QCheckBox('Chilean Division 1')],
            'CLB': ['72', QtWidgets.QCheckBox('Other Matches')],
            'CNC': ['100', QtWidgets.QCheckBox('Central and North American Cup')],
            'CWP': ['67', QtWidgets.QCheckBox('Club World Cup')],
            'DFL': ['16', QtWidgets.QCheckBox('Dutch Division 1')],
            'DF2': ['104', QtWidgets.QCheckBox('Dutch Division 2')],
            'DAC': ['39', QtWidgets.QCheckBox('Dutch Cup')],
            'EPL': ['1', QtWidgets.QCheckBox('English Premier')],
            'ED1': ['29', QtWidgets.QCheckBox('English Championship')],
            'ED2': ['30', QtWidgets.QCheckBox('English League 1')],
            'ED3': ['101', QtWidgets.QCheckBox('English League 2')],
            'EFA': ['5', QtWidgets.QCheckBox('English FA Cup')],
            'ELC': ['8', QtWidgets.QCheckBox('English League Cup')],
            'ELT': ['99', QtWidgets.QCheckBox('English League Trophy')],
            'FF2': ['103', QtWidgets.QCheckBox('French Division 2')],
            'FFA': ['35', QtWidgets.QCheckBox('French FA Cup')],
            'FFC': ['28', QtWidgets.QCheckBox('French League Cup')],
            'FFL': ['14', QtWidgets.QCheckBox('French Division 1')],
            'GD2': ['54', QtWidgets.QCheckBox('German Division 2')],
            'GSC': ['11', QtWidgets.QCheckBox('German Cup')],
            'GSL': ['3', QtWidgets.QCheckBox('German Division 1')],
            'IFC': ['9', QtWidgets.QCheckBox('Italian Cup')],
            'ISA': ['2', QtWidgets.QCheckBox('Italian Division 1')],
            'ISC': ['51', QtWidgets.QCheckBox('Italian Super Cup')],
            'JD1': ['55', QtWidgets.QCheckBox('Japanese Division 1')],
            'JD2': ['87', QtWidgets.QCheckBox('Japanese Division 2')],
            'JEC': ['75', QtWidgets.QCheckBox('Emperors Cup')],
            'JSC': ['70', QtWidgets.QCheckBox('Japanese Super Cup')],
            'KD1': ['88', QtWidgets.QCheckBox('Korean Division 1')],
            'KFA': ['148', QtWidgets.QCheckBox('Korean FA Cup')],
            'LBC': ['71', QtWidgets.QCheckBox('Copa Libertadores')],
            'MLS': ['79', QtWidgets.QCheckBox('US Football League')],
            'MXL': ['124', QtWidgets.QCheckBox('Mexican Premier')],
            'MXC': ['127', QtWidgets.QCheckBox('Mexican Cup')],
            'NTL': ['59', QtWidgets.QCheckBox('Norwegian Division 1')],
            'NWC': ['83', QtWidgets.QCheckBox('Norwegian Cup')],
            'PFL': ['17', QtWidgets.QCheckBox('Portuguese Premier')],
            'PFC': ['40', QtWidgets.QCheckBox('Portuguese Cup')],
            'PLC': ['86', QtWidgets.QCheckBox('Portuguese League Cup')],
            'RPL': ['122', QtWidgets.QCheckBox('Russian Premier')],
            'RFC': ['126', QtWidgets.QCheckBox('Russian Cup')],
            'SAC': ['106', QtWidgets.QCheckBox('South American Cup')],
            'SEC': ['91', QtWidgets.QCheckBox('South East Asian Championship')],
            'SFA': ['37', QtWidgets.QCheckBox('Scottish FA Cup')],
            'SFC': ['10', QtWidgets.QCheckBox('Spanish Cup')],
            'SFL': ['4', QtWidgets.QCheckBox('Spanish Division 1')],
            'SLC': ['36', QtWidgets.QCheckBox('Scottish League Cup')],
            'SPL': ['15', QtWidgets.QCheckBox('Scottish Premier')],
            'UCL': ['6', QtWidgets.QCheckBox('UEFA Champions League')],
            'UEC': ['7', QtWidgets.QCheckBox('UEFA Europa League')]}

        vbox = QtWidgets.QVBoxLayout()
        for l in self.checkboxes:
            self.checkboxes[l][1].league_name = l
            vbox.addWidget(self.checkboxes[l][1])
            self.checkboxes[l][1].stateChanged.connect(
                lambda: self.check_league(self.match_table))

        groupbox = QtWidgets.QGroupBox()
        groupbox.setLayout(vbox)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(False)
        scroll.setHorizontalScrollBarPolicy(1)
        scroll.setFixedHeight(400)
        scroll.setFixedWidth(250)

        self.matches = HKJCHandler.fetch_all_odds()

        for i, match in enumerate(self.matches):
            self.match_table.insertRow(i)

            item = QtWidgets.QTableWidgetItem(match.short_id)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem(match.date)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 1, item)

            item = QtWidgets.QTableWidgetItem(match.time)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 2, item)

            item = QtWidgets.QTableWidgetItem(str(match.league))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 3, item)

            item = QtWidgets.QTableWidgetItem(str(match.home_team))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 4, item)

            item = QtWidgets.QTableWidgetItem(str(match.away_team))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.match_table.setItem(i, 5, item)

            item = QtWidgets.QTableWidgetItem('')
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.row = i
            # item.stateChanged.connect(
            #     lambda: self.check_match())
            self.match_table.setItem(i, 6, item)

        self.match_table.cellChanged.connect(self.check_match)

        # # self.tableWidget.move(0, 0)

        main_layout = QtWidgets.QVBoxLayout()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(self.match_table)

        main_layout.addLayout(layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.export_btn)

        main_layout.addLayout(layout)

        self.setLayout(main_layout)
        self.setWindowTitle('HKJC Odds Crawler')
        self.setFixedSize(1175, 450)
        self.show()

    def check_league(self, table):

        allRows = table.rowCount()
        league_name = self.sender().league_name
        state = self.sender().isChecked()
        for row in range(allRows):
            
            if league_name in table.item(row, 3).text():

                print(league_name)
                table.item(row, 6).setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)

    def check_match(self, row, column):

        print('Clicked row', row)
        if column == self.match_table.columnCount() - 1:

            if self.match_table.item(row, 6).checkState():

                print('Add', str(self.matches[row]))
                self.checked_matches.append(row)

            else:

                print('Remove', str(self.matches[row]))
                self.checked_matches.remove(row)

    def saveFileDialog(self, table):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV(*.csv)", options=options)
        
        if len(self.checked_matches) == 0:

            return

        print(fileName)

        with open(fileName, 'w+') as f:

            f.write(','.join(self.matches[0].export_keys()) + '\n')

            for row in sorted(self.checked_matches):
                
                print('Export', str(self.matches[row]))

                f.write(','.join(self.matches[row].export()) + '\n')

if __name__ == '__main__': 

    app = QtWidgets.QApplication(sys.argv)
    a_window = Window()
    sys.exit(app.exec_())