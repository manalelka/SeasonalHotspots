def to_ts(df):
    ts = df.set_index("timestamp")
    ts['count'] = 1
    return ts
    
def agg_ts(ts, agg_size = '24H'):
    ts = ts.resample(agg_size).sum() # add variable resampling!
    ts['ds'] = ts.index
    ts.rename(columns={'count':'y'}, inplace = True)
    #ts.drop(min(ts4.index), inplace = True) # dropping the 12th since it is not complete for daily aggregation
    #ts.drop(max(ts4.index), inplace = True) # dropping the 12th since it is not complete for daily aggregation
    return ts

def fcast(ts, h=10, freq = 'D'):
    ''' Automatically forecast with defalt values of 10 as h and daily frequency'''
    from fbprophet import Prophet

    m = Prophet(changepoint_prior_scale=0.05).fit(ts)
    future = m.make_future_dataframe(periods=h, freq=freq)
    fcst = m.predict(future)
    y_hat = m.plot(fcst)
    fig = m.plot_components(fcst)
    return fig