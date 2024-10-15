import connection_to_db as db
import sys

from box_score_window import Ui_BoxScoreWindow
from game_start_window import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from tkinter import messagebox as msg


def add_teams_to_combo(ui: Ui_MainWindow, teams: list):
    possible_teams = [item['team_name'] for item in teams]
    print(possible_teams)
    ui.combo_home.addItems(possible_teams)
    ui.combo_away.addItems(possible_teams)
    ui.combo_home.currentIndexChanged.connect(lambda: change_current_team(ui.checkbox_home_list, ui.combo_home))
    ui.combo_away.currentIndexChanged.connect(lambda: change_current_team(ui.checkbox_away_list, ui.combo_away))


def change_current_team(checkbox_list, current_combobox):
    ui.hide_elements(checkbox_list)
    change_color_label()
    query = f"""select shirt_number from basket.players p
                inner join basket.teams t on t.team_id = p.team_id 
                where t.team_name = '{current_combobox.currentText()}'"""
    players = db.select_data_from_db(config, query)
    for index, player in enumerate(players):
        checkbox_list[index].show()
        checkbox_list[index].setText(str(player['shirt_number']))



def count_starters_2(my_list : list) -> int:
    # counter = 0
    # for player in my_list:
    #     if player.isChecked():
    #         counter += 1
    #
    # return counter

    new_list = [player for player in my_list if player.isChecked()]
    return len(new_list)


def change_color_label():
    current_home_team = ui.combo_home.currentText()
    color_home = "black"
    for team in teams:
        if team['team_name'] == current_home_team:
            color_home = team['home_color']
            break

    # ui.team_home_label.setText("ala bala portocala")
    ui.team_home_label.setStyleSheet(f"color: {color_home};")

    current_away_team = ui.combo_away.currentText()
    color_away = "black"
    for team in teams:
        if team['team_name'] == current_away_team:
            color_away = team['away_color']
            break
    ui.team_away_label.setStyleSheet(f"color: {color_away};")

def start_boxscore_window():
    app2 = QtWidgets.QApplication(sys.argv)
    MainWindow2 = QtWidgets.QMainWindow()
    ui2 = Ui_BoxScoreWindow()
    ui2.setupUi(MainWindow2)
    MainWindow2.show()
    sys.exit(app2.exec())


def start_game():
    if ui.combo_home.currentText() == ui.combo_away.currentText():
        msg.showerror("Error on starting game", "Please choose different teams")
    else:
        count_starters = lambda my_list: len([player for player in my_list if player.isChecked()])
        home_counter = count_starters(ui.checkbox_home_list)
        away_counter = count_starters(ui.checkbox_away_list)
        if home_counter >= 3 and away_counter >= 3:
            # here happens the magic
            # QtWidgets.QApplication.quit()
            MainWindow.close()
            start_boxscore_window()
            # TODO connect the two windows together (doesn' t work yet)
        else:
            msg.showerror("Error on starting game", "Please choose your starters.")




if __name__ == '__main__':
    config = db.read_config()
    teams = db.select_data_from_db(config)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    qpixmap = QtGui.QPixmap("basketball.png")
    ui.logo_image.setPixmap(qpixmap)
    add_teams_to_combo(ui, teams)
    ui.start_game_button.clicked.connect(start_game)

    MainWindow.show()
    sys.exit(app.exec())