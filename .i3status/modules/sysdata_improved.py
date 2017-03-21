# -*- coding: utf-8 -*-


import re
import subprocess
from time import sleep, time


class GetData:

  def gpu(self):
    gpu_data = subprocess.check_output(
      ['nvidia-smi', '-q', '-d', 'UTILIZATION']).split()
    gpu_index = gpu_data.index('Gpu')
    gpu_mem_index = gpu_data.index('Memory')
    gpu_usage_percent = int(gpu_data[gpu_index + 2])
    gpu_mem_percent = int(gpu_data[gpu_mem_index + 2])

    return gpu_usage_percent, gpu_mem_percent

  def cpu(self):
    with open('/proc/stat', 'r') as fd:
      line = fd.readline()
    cpu_data = line.split()
    total_cpu_time = sum(map(int, cpu_data[1:]))
    cpu_idle_time = int(cpu_data[4])

    # return the cpu total&idle time
    return total_cpu_time, cpu_idle_time

  def memory(self):
    # Run 'free -m' command and make a list from output.
    mem_data = subprocess.check_output(['free', '-m']).split()
    mem_index = mem_data.index('Mem:')
    buffer_index = mem_data.index('buffers/cache:')
    total_mem = int(mem_data[mem_index + 1]) / 1024.
    #used_mem = int(mem_data[mem_index + 2]) / 1024.
    used_mem = int(mem_data[buffer_index + 1]) / 1024.

    # Caculate percentage
    used_mem_percent = int(used_mem / (total_mem / 100))

    # Results are in kilobyte.
    return total_mem, used_mem, used_mem_percent

  def cpuTemp(self):
    sensors = subprocess.check_output('sensors', shell=True)
    m = re.search("(Core 0|CPU Temp).+\+(.+).+\(.+", sensors)
    if m:
      cpu_temp = m.groups()[1].strip()
    else:
      cpu_temp = 'Unknown'

    return cpu_temp


class Py3status:
  cache_timeout = 10
  format = ''
  high_threshold = 75
  med_threshold = 40

  def __init__(self):
    self.data = GetData()
    self.cpu_total = 0
    self.cpu_idle = 0

  def sysDataImproved(self, i3s_output_list, i3s_config):
    # get CPU usage info
    cpu_total, cpu_idle = self.data.cpu()
    cpu_usage = 1 - (
      float(cpu_idle-self.cpu_idle) / float(cpu_total-self.cpu_total)
      )
    self.cpu_total = cpu_total
    self.cpu_idle = cpu_idle

    # if specified as a formatting option, also get the CPU temperature
    if '{cpu_temp}' in self.format:
      cpu_temp = self.data.cpuTemp()
    else:
      cpu_temp = ''

    # get RAM usage info
    mem_total, mem_used, mem_used_percent = self.data.memory()

    # get GPU usage info
    gpu_usage_percent, gpu_mem_percent = self.data.gpu()

    response = {
      'cached_until': time() + self.cache_timeout,
      'full_text': self.format.format(
        cpu_usage='%02d' % int(cpu_usage*100),
        cpu_temp=cpu_temp,
        mem_used='%d' % int(mem_used),
        mem_total='%d' % int(mem_total),
        mem_used_percent='%02d' % mem_used_percent,
        gpu_usage_percent='%02d' % gpu_usage_percent,
        gpu_mem_percent='%02d' % gpu_mem_percent,
      )
    }

    # set color based on most heavily taxed component
    max_load = max(int(cpu_usage*100), mem_used_percent, gpu_usage_percent,
                   gpu_mem_percent)
    if max_load <= self.med_threshold:
      response['color'] = i3s_config['color_good']
    elif max_load <= self.high_threshold:
      response['color'] = i3s_config['color_degraded']
    else:
      response['color'] = i3s_config['color_bad']

    return response

if __name__ == "__main__":
  x = Py3status()
  config = {
    'color_bad': '#FF0000',
    'color_degraded': '#FFFF00',
    'color_good': '#00FF00',
  }

  while True:
    print(x.sysDataImproved([], config))
    sleep(1)
