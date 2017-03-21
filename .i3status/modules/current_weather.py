import json
import time

from pprint import pprint
from urllib2 import Request, urlopen, URLError


class Py3status():
  cache_timeout = 15 * 60
  format = '{summary}, {temperature}{format_units}'
  color = None
  api_key = 'aedbe423524c19d7d9e338af6ee8446d'
  location = '37.4012,-122.0519'
  units = 'auto'
  exclude='minutely,hourly,daily,alerts'

  def _get_forecast(self):
    api_url = ('https://api.forecast.io/forecast/%s/%s?units=%s&exclude=%s'
               % (self.api_key, self.location, self.units, self.exclude))
    request = Request(api_url)

    try:
      response = urlopen(request)
      data = json.loads(response.read())
      weather = data['currently']
      flags = data['flags']
      return weather, flags
    except URLError, e:
      return None

  def current_weather(self, i3s_output_list, i3s_config):
    weather, flags = self._get_forecast()

    if 'us' in flags['units']:
      format_units = 'F'
    elif 'si' in flags['units']:
      format_units = 'C'
    else:
      format_units = None

    if weather:
      response = {
        'cached_until': time.time() + self.cache_timeout,
        'full_text': self.format.format(
          summary='%s' % weather['summary'],
          temperature='%d' % int(weather['apparentTemperature']),
          format_units='%s' % format_units,
        ),
        'color': self.color,
      }
    else:
      response = {
        'cached_until': time.time() + self.cache_timeout,
        'full_text': 'error',
        'color': i3s_config['color_bad'],
      }

    return response


if __name__ == '__main__':
  x = Py3status()
  config = {
    'color_bad': '#FF0000',
    'color_degraded': '#FFFF00',
    'color_good': '#00FF00',
  }

  while True:
    print(x.current_weather([], config))
    time.sleep(5)
