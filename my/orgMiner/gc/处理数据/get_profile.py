#获取profile
def get_profile(rl):
    # 生成profile
    from orgminer.ResourceProfiler.raw_profiler import count_execution_frequency
    profiles = count_execution_frequency(rl, scale=None)
    return profiles