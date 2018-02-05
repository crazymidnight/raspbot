from bs4 import BeautifulSoup
import requests

WINDOW_TEXT = 'В это время окно'
TIMES = ['8:30', '10:25', '12:20', '14:15', '16:10', '18:05']

def get_html(group):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    url = f'http://rasp.tpu.ru/view.php?for={group}&aslist=0'  # url для второй страницы
    r = requests.get(url, headers=headers)

    return r.text


def scrape_today(group):

    rasp = get_html(group=group)

    soup = BeautifulSoup(rasp, "html.parser")
    # print(soup.body.prettify())
    # print(soup.body.find)
    tables = soup.body.findAll('table', {'class': 'c-table schedule'})
    current_day = ''
    for table in tables:
        try:
            current_day = table.findAll('td', {'class': 'current-day'})
        except AttributeError:
            return 'Расписание не найдено :( \nПопробуйте ввести заново'

    today_subjects = ''
    time_num = 0
    for i in current_day:

        if len(i.text) < 3:
            today_subjects += (TIMES[time_num] + '\n')
            today_subjects += (WINDOW_TEXT + '\n')
            today_subjects += ('-----------------------' + '\n')

        else:
            today_subjects += (TIMES[time_num] + '\n')
            today_subjects += (i.text + '\n')
            today_subjects += ('-----------------------' + '\n')

        time_num += 1

    if len(today_subjects) < 3:
        return 'Расписание не найдено :( \nПопробуйте ввести заново'

    return today_subjects

if __name__ == '__main__':
    group = '8е41'
    rasp = scrape_today(group=group)
    print(rasp)
