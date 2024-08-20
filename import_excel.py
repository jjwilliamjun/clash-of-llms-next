import pandas as pd
import xlrd

'''
    PACKAGE VERISIONS
    pandas 2.2.2
    xlrd 2.0.1
    openpyxl 3.1.5
'''


def import_settings(xls_path):
    settings = pd.read_excel(xls_path)
    red_team = settings.loc[0]
    blue_team = settings.loc[1]
    red_team.to_dict()
    blue_team.to_dict()

    # TO DO --> return objects for red/blue teams
    # TO DO --> validate input?

    return red_team, blue_team


def main():
    path = input()
    red_team, blue_team = import_settings(path)


if __name__ == '__main__':
    main()
