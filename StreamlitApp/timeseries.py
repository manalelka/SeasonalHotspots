def to_ts(df):
    ts = df.set_index("timestamp")
    ts['count'] = 1
    return ts
    
def agg_ts(ts, agg_size = '24H', tag = 'count'):
    ts = ts.resample(agg_size).sum() 
    ts['ds'] = ts.index
    ts.rename(columns={tag:'y'}, inplace = True)
    ts.drop([min(ts.index), max(ts.index)], inplace = True) # dropping the incomplete instances
    # ts.drop(max(ts.index), inplace = True)
    return ts

def fcast(ts, h=7, freq = 'D'):
    ''' Automatically forecast with defalt values of 7 as h and daily frequency'''
    from fbprophet import Prophet

    m = Prophet(changepoint_prior_scale=0.05).fit(ts)
    future = m.make_future_dataframe(periods=h, freq=freq)
    fcst = m.predict(future)
    y_hat = m.plot(fcst)
    fig = m.plot_components(fcst)
    return y_hat, fig