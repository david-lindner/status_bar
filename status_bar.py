import psutil
import subprocess
import re
import time

def style_label(s):
   return "<span color='white'>%s</span>" % s

def style_value(s):
   return "<span color='LimeGreen'>%s</span>" % s

SEP = "<span font_weight='bold' color='white'> | </span>"

GB = 10**9
KB = 10**3

cpu_percent = psutil.cpu_percent()

mem = psutil.virtual_memory()
mem_used = (mem.total - mem.available) / GB
mem_total = mem.total / GB
mem_percent = mem.percent

# getting current KB sent and received per second
network_info = psutil.net_io_counters()
downstream_kb = network_info.bytes_recv
upstream_kb = network_info.bytes_sent
time.sleep(1)
network_info = psutil.net_io_counters()
downstream_kb = (network_info.bytes_recv - downstream_kb) / KB
upstream_kb = (network_info.bytes_sent - upstream_kb) / KB


# using linux tools to get audio volume (in alsa)
# didn't find a good pure python alternative here
try:
   vol_stdout = subprocess.run(['amixer', 'sget', 'Master'], stdout=subprocess.PIPE).stdout.decode().replace('\n', '')
   m = re.match(r'.*\[(.*?)%\].*', vol_stdout)
   volume_percent = int(m.group(1))
except Exception:
   volume_percent = -1

battery = psutil.sensors_battery()
battery_percent = battery.percent
if battery.power_plugged:
   battery_plugged_in_str = ' (plugged in) '
else:
   battery_plugged_in_str = ''


output_str = '<txt>' + style_label('CPU') + ' ' + style_value('%.0f%%' % cpu_percent) + SEP + \
	     style_label('Memory') + ' ' + style_value('%.2f GB / %.2f GB (%.2f%%)' % (mem_used, mem_total, mem_percent)) + SEP +\
	     style_label('Network') + ' ' + style_value('\u2193 %.0f KB \u2191 %.0f KB' % (downstream_kb, upstream_kb)) + SEP +\
	     style_label('Volume') + ' ' + style_value('%.0f%%' % volume_percent) + SEP +\
	     style_label('Power') + ' '  + style_value('%.0f%%' % battery_percent + battery_plugged_in_str) + '</txt>'

print(output_str)
