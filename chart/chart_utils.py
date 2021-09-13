import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid

def get_data(row: int) -> pd.DataFrame:
    a = np.random.randint(0, 10, size=[row, 4])
    index = []
    dt = datetime.now()
    for i in range(row):
        tmp_dt = dt + timedelta(days=-i)
        index.append(tmp_dt)

    df = pd.DataFrame(a, columns=['open', 'close', 'max', 'min'], index=index)
    return df

def show_chart(data: pd.DataFrame):
    bar = Bar()
    bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    bar.render()




if __name__ == '__main__':
    show_chart(get_data(10))