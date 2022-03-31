# 从csv获取资源日志
def csv_to_dataFrame(file):
    import csv
    import pandas as pd
    tmp_lst = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    return df



# A获取资源日志
def get_resource_log(fn_event_log,units,final):
    from orgminer.IO.reader import read_xes
    with open(fn_event_log, 'r', encoding='utf-8') as f:
        el = read_xes(f)
    from orgminer.ExecutionModeMiner import informed_groupby
    sp_time_unit = units
    exec_mode_miner = informed_groupby.TraceClusteringFullMiner(el,resolution=sp_time_unit)
    rl = exec_mode_miner.derive_resource_log(el)
    print(rl)
    rl.to_csv(final)


# 生成资源日志
if __name__ == '__main__':
    fn_event_log='../数据/原始日志/BPIC15_1_sorted_new.csv'
    units='weekday'
    final='../数据/资源日志/bpic15_1_rl.csv'
    get_resource_log(fn_event_log, units, final)

