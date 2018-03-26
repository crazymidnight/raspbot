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
    # odd and even weeks
    odd_week = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    even_week = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    both_weeks = {'odd': odd_week, 'even': even_week}
    week_idx = [0, 1, 2, 3, 4, 5]
    idx = 'odd'
    for one_week in weeks:
        for i in one_week:
            if i.text in TIMES:
                pass
            else:
                if len(i.text) > 0:
                    both_weeks[idx][week_idx[a]].append(i.text)
                else:
                    both_weeks[idx][week_idx[a]].append('Этой пары нет')
                if a < 5:
                    a += 1
                else:
                    a = 0
        idx = 'even'
    return both_weeks


def get_current_week(both_weeks):
    date = datetime.datetime.today()
    week = date.isocalendar()[1]
    if week % 2 == 0:
        return both_weeks['even']
    else:
        return both_weeks['odd']


def get_current_day(week):
    date = datetime.datetime.today()
    day = date.weekday()
    if day < 6:
        schedule = week[day]
        today_subjects = ''
        time_num = 0
        for i in schedule:
            today_subjects += (TIMES[time_num] + '\n')
            today_subjects += (i + '\n')
            today_subjects += ('-----------------------' + '\n')

            time_num += 1
        return today_subjects
    else:
        return 'Сегодня выходной'


if __name__ == '__main__':
    group = '8е41'
    weeks = scrape_rasp(group=group)
    current_week = get_current_week(weeks)
    text = get_current_day(week=current_week)
    print(text)