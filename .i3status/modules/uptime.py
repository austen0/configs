import subprocess
import time


class Py3status:
  cache_timeout = 60 * 60
  color = None
  format = '{days} days'

  def uptime(self, i3s_output_list, i3s_config):
    uptime = subprocess.check_output(['uptime', '-s']).strip()
    pattern = '%Y-%m-%d %H:%M:%S'

    uptime = int(time.time()) - int(time.mktime(time.strptime(uptime, pattern)))

    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    if '{weeks}' in self.format:
      weeks = uptime // 604800
      uptime = uptime % 604800
    if '{days}' in self.format:
      days = uptime // 86400
      uptime = uptime % 86400
    if '{hours}' in self.format:
      hours = uptime // 3600
      uptime = uptime % 3600
    if '{minutes}' in self.format:
      minutes = uptime // 60
      uptime = uptime % 60
    seconds = uptime

    response = {
      'cached_until': time.time() + self.cache_timeout,
      'full_text': self.format.format(
        weeks='%d' % weeks,
        days='%d' % days,
        hours='%d' % hours,
        minutes='%d' % minutes,
        seconds='%d' % seconds,
      ),
      'color': self.color,
    }

    return response

if __name__ == "__main__":
  x = Py3status()
  config = {
    'color_good': '#00FF00',
    'color_bad': '#FF0000',
  }
  while True:
    print(x.uptime([], config))
    time.sleep(1)
