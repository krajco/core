import sys
from os import walk, makedirs
from os.path import exists
from datetime import datetime


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def time_to_sec(time):
    h, m, s = map(int, time.split(':'))
    return h * 3600 + m * 60 + s


def get_data_between_rows(row1, row2):
    interval = 10 * 60  # 15 min
    rv_interval = 1 / interval
    row1 = row1.replace('\n', '').split(',')
    row2 = row2.split(',')

    timestamp1 = float(row1[6])
    timestamp2 = float(row2[6])
    diff_timestamp = timestamp2 - timestamp1
    num_of_cycle = int(diff_timestamp * rv_interval)
    lines = ''
    for x in range(1, num_of_cycle):
        timestamp1 += interval
        dt_object = datetime.fromtimestamp(timestamp1)
        date = dt_object.date().strftime('%m/%d/%y')
        time = str(dt_object.time())
        seconds = str(time_to_sec(time))
        lines += date + ',' + row1[1] + ',' + row1[2] + ',' + time + ',' + row1[4] + ',' + seconds + ',' + str(timestamp1) + '\n'
    return lines


class LogManager:
    def __init__(self, object_id, dir_path='/var/log/nagios'):
        self._log_filenames = []
        self._merged_filename = None
        self._dir_path = dir_path
        self._object_id = object_id
        self._log_dates = next(walk(self._dir_path), (None, None, []))[1]
        self._log_dates.sort()
        self._log_dates.pop()  # Remove merged dir

    def _get_log_filenames(self):
        for date in self._log_dates:
            log_filename = '{0}/{1}/{2}.log'.format(self._dir_path, date, self._object_id)
            if exists(log_filename):
                self._log_filenames.append(log_filename)

    def set_date(self, date_from, date_to):
        new_log_dates = []
        actual = False

        # Check date format
        if len(date_from.split('-')) != 3 or len(date_to.split('-')) != 3:
            print('UPDATE LOG FILES: incompatible date format, %m-%d-%Y', file=sys.stderr)
            exit(1)

        timestamp_from = int(datetime.strptime(date_from, '%m-%d-%Y').strftime('%s'))
        timestamp_to = int(datetime.strptime(date_to, '%m-%d-%Y').strftime('%s'))

        for date in self._log_dates:
            log_timestamp = int(datetime.strptime(date, '%m-%d-%Y').strftime('%s'))
            if timestamp_from <= log_timestamp <= timestamp_to:
                new_log_dates.append(date)

        self._log_dates = new_log_dates

    def merge_log_files(self, path='/var/log/nagios/merged/'):
        self._get_log_filenames()

        if not exists(path):
            makedirs(path)
            print('Merged dir is created at: ' + path)

        lines = prev_line = line = float_value = float_col = ''
        for log_file in self._log_filenames:
            data = open(log_file, 'r').read().split('\n')
            for item in data:
                cells = item.split(' ')
                if len(cells) > 2 and cells[2].split('/')[0] != 'unavailable':
                    date = cells[0].replace('[', '')
                    date_indexes = date.split('/')

                    value = cells[2].split('/')[0]
                    if is_float(value):
                        day_index = datetime(int(date_indexes[2]), int(date_indexes[0]), int(date_indexes[1]))
                        time = cells[1].replace(']', '')
                        timestamp_time_in_day = time_to_sec(time)
                        timestamp_datetime = datetime.strptime(date, "%m/%d/%y").timestamp() + timestamp_time_in_day

                        prev_line = line
                        line = date + ',' + day_index.strftime('%w') + ',' + day_index.strftime('%j') + ',' + time + ',' + value + ',' + str(timestamp_time_in_day) + ',' + str(timestamp_datetime) + '\n'
                        if prev_line != '':
                            lines += get_data_between_rows(prev_line, line)
                        lines += line

        date_from = self._log_dates[0]
        date_to = self._log_dates[len(self._log_dates)-1]
        self._merged_filename = path + date_from + '_' + date_to + '_' + self._object_id + '.log'

        if not exists(self._merged_filename):
            columns = 'Date,Day in week,Day in year,Time,Value,Seconds,Timestamp\n'
            file = open(self._merged_filename, 'w')
            file.write(columns + lines)
            file.close()

        return self._merged_filename
