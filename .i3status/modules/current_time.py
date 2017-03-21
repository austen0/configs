import time

from datetime import datetime

class Py3status:
  cache_timeout = 1
  color = None
  format = ''

  def current_time(self, i3s_output_list, i3s_config):
    now = datetime.now()
    current_time = now.strftime('%a %b %e %l:%M:%S %p')
    response = {
      'cached_until': time.time() + self.cache_timeout,
      'full_text': current_time,
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
    print(x.current_time([], config))
    time.sleep(1)
