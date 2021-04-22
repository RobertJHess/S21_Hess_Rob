# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request
import urllib.error


def read_file(file_name):
    dates = []
    with open(file_name) as f:
        for line in f:
            dates.append(line.strip())
    return dates


def main():
    dates_file = "D:\\Spring 2021\\Senior Project\\Dates_Formatted_For_Download.csv"
    dates = read_file(dates_file)

    for date in dates:
        try:
            urllib.request.urlretrieve(
                'https://www.federalreserve.gov/newsevents/pressreleases/monetary' + str(date) + 'a.htm',
                "D:\\Spring 2021\\Senior Project\\Statement_htmls\\" + str(date) + "FOMC_statement.html")
            print('https://www.federalreserve.gov/newsevents/pressreleases/monetary' + str(date) + 'a.htm', 'saved')
        except urllib.error.HTTPError:
            print('https://www.federalreserve.gov/newsevents/pressreleases/monetary' + str(date) + 'a.htm', "is not found")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
