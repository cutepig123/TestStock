
import akshare as ak

if False:
    current_data_df = ak.stock_hk_spot()
    print(current_data_df)


stock_hk_daily_hfq_df = ak.stock_hk_daily(symbol="00522", adjust="")
print(stock_hk_daily_hfq_df)

stock_hk_daily_hfq_df.plot( y=['open', 'close'] ,kind='line')
import matplotlib.pyplot as plt
plt.show()