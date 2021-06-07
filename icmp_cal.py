# from ping3 import ping, verbose_ping
# import pings
import sys, subprocess, re
import numpy as np
import time
# import numpay

DEST_IP = '172.17.0.3'
RTT_ARRY = []
OLD_VALUE = 0.0
COUNT_ARRY = []


def calc_bandwidth():
  # time.sleep(1)
  estimate_size = icmp_size_inc()  # bps
  return estimate_size


def get_rtt(value): # pingを1回飛ばして、RTTを返す関数
  ping_command = 'ping ' + DEST_IP + ' -c 1 -l ' + str(value)
  # ping_command = 'ping ' + DEST_IP + ' -c 1'
  result = subprocess.getoutput(ping_command)

  regex = re.compile('rtt min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms') 
  for line in result.split('\n'):
      m = regex.match(line)
      if m:
        rtt = re.findall(r"[\d.]+", line)[0]
        return rtt
  
def icmp_size_inc():
  ans = 0
  j = 0
  i = 0
  #ここで増分変化を検知するまでループ
  while True:
    i = i + 1000 # RTTの値を取得 byte 0.1MBずつ増やす
    calc = get_rtt(i)
    if calc == None:
      continue
    ans = jadge_inc(float(calc), j)
    j = j + 1
    # 30回計測もしくはRTTが差分50になれば推定帯域としてみなす暫定
    # print('ans:' + str(ans))
    if ans == 1 : #ここの基準を最小二乗法などで傾きの変化で決定するようにしたい
      # send_size = (i * 8) / float(calc)
      send_size = int(i / float(calc)) 
      break
    
  return send_size

def jadge_inc(new_rtt, count):
  global OLD_VALUE
  
  # 最新のRTTを配列に格納し、差分を計算する。
  # if count > 0:
  #   RTT_ARRY.append(new_rtt)
  #   RTT_DIFF = np.diff(RTT_ARRY, n=1)  # 差分計算
  #   rtt_max = max(RTT_DIFF, default = 0)
  RTT_ARRY.append(new_rtt) # y
  COUNT_ARRY.append(count)  # x
  if count > 2:
    k = np.polyfit(COUNT_ARRY, RTT_ARRY, 1)
    a = k[0]  # 傾き
    diff_value = (abs(OLD_VALUE - a) / OLD_VALUE) * 100
    OLD_VALUE = a

  # 配列の中で増分が大きい値が閾値を超えたら,推定帯域のポイントとしてflag = 1を返す
    if diff_value > 100.0 and diff_value < 800.0:  # %
      flag = 1
    else:
      flag = 0
  else:
    flag = 0
  return flag

if __name__ == "__main__":
  calc_bandwidth()