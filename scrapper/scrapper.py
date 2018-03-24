from bs4 import BeautifulSoup
import datetime
import requests

WINDOW_TEXT = 'В это время окно'
TIMES = ['08:30', '10:25', '12:20', '14:15', '16:10', '18:05']

def get_html(group):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    url = f'http://rasp.tpu.ru/view.php?for={group}'  # url для второй страницы
    r = requests.get(url, headers=headers)

    return r.text


def scrape_rasp(group):
    """find all subjects"""
    rasp = get_html(group=group)
    soup = BeautifulSoup(rasp, 'html.parser')
    tables = soup.body.findAll()
    tables = soup.body.findAll('table', {'class': 'c-table schedule'})
    weeks = [tables[0].findAll('td'), tables[1].findAll('td')]
    a = 0

    odd_week = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': [], 'saturday': []}
    even_week = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': [], 'saturday': []}
    both_weeks = {'odd': odd_week, 'even': even_week}
    week_idx = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    idx = 'odd'
    for one_week in weeks:
        for i in one_week:
            if i.text in TIMES:
                pass
            else:
                if len(i.text) > 0:
                    print(i.text)
                    both_weeks[idx][week_idx[a]].append(i.text)
                else:
                    both_weeks[idx][week_idx[a]].append('Этой пары нет')
                if a < 5:
                    a += 1
                else:
                    a = 0
        idx = 'even'
    return both_weeks


def get_week(both_weeks):
    print()


def scrape_today(group):

    rasp = get_html(group=group)

    soup = BeautifulSoup(rasp, "html.parser")
    # print(soup.body.prettify())
    # print(soup.body.find)
    tables = soup.body.findAll('table', {'class': 'c-table schedule'})
    current_day = ''
    for table in tables:
        try:
            current_day = table.findAll('div', {'class': 'subject'})
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
    group = '4б51'
    week = scrape_rasp(group=group)
    print(week) 