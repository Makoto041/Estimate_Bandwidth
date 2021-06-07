
import icmp_cal
import time

class Estimator(object):


    def report_states(self, stats: dict):
        '''
        stats is a dict with the following items
        {
            "send_time_ms": uint,
            "arrival_time_ms": uint,
            "payload_type": int,
            "sequence_number": uint,
            "ssrc": int,
            "padding_length": uint,
            "header_length": uint,
            "payload_size": uint
        }
        '''

    def get_estimated_bandwidth(self) -> int:
        data_file = './data.txt'
        file_name_ref = './estimate_bandwidth.txt'
        with open(data_file) as f1:
            count = f1.readline()
            count = int(count.rstrip())            
        if count == 0 or (count % 10) == 0:
            file_name = './result1.txt'
            estimate_bandwidth = int(icmp_cal.calc_bandwidth())
            # 推定帯域幅記録用
            with open(file_name, mode="a", encoding="utf8") as f:
                f.write(str(estimate_bandwidth) + "\n")
            # 10回おきに参照するため推定帯域幅を別ファイルに保存する。
            with open(file_name_ref, mode="w", encoding="utf8") as f3:
                f3.write(str(estimate_bandwidth))
        else:
            # ICMPコードを実行しない時は保存した最新の推定帯域幅を参照する。
            with open(file_name_ref) as f4:
                estimate_bandwidth = f4.readline()
                estimate_bandwidth = int(estimate_bandwidth.rstrip())


        count = count + 1
        with open(data_file, mode="w") as f2:
            f2.write(str(count))
        time.sleep(0.05)
        return int(estimate_bandwidth) # 予想される帯域幅を返す
        # return int(1e6) 


