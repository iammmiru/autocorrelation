import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
import scipy.fftpack as fft

def correlation_scipy(time,data):
    """
    Calculate autocorrelation using scipy.signal.correlate function.
    Note that due to the difference in definition, the result is divided by
    "factor", which is the number of entries that are correlated.
    """
    m            = data.shape[0]
    dt           = time[1]-time[0]
    if m%2 != 0:
        factor       = np.arange(m,0,-1)[:m//2+1]
        correl       = np.zeros(m//2+1)
        time_out     = time[:m//2+1]
    else:
        factor       = np.arange(m,0,-1)[:m//2]
        correl       = np.zeros(m//2)
        time_out     = time[:m//2]
    correl   = sp.correlate(data,data,
                            mode='same',method='fft')[m//2:]/factor
    return time_out,correl


def correlation_manual(time, data):
    """
    Manually calculate autocorrelation.
    """
    m            = data.shape[0]
    correl       = np.zeros_like(data[:m//2])
    n = correl.shape[0]
    for i in range(n):
        if i == 0:
            correl[i] = np.sum(data*data, axis = 0)/m
        else:
            correl[i] = np.sum(data[:-i]*data[i:], axis = 0)/data[:-i].shape[0]
    return time[:m//2],correl

def correlation_fft(time, data, zero_padding = True):
    """
    Calculate autocorrelation using the fast fourier transform (fft).
    Since the fft assumes the data is cyclical, one needs to pad some zeros into
    the data, so that the algorithms runs as if it is acyclical. Otherwise, the
    algorithm returns an incorrect autocorrelation function.

    Note the result is divided by "factor" only when the zero padding is performed.

    """
    m            = data.shape[0]
    dt           = time[1]-time[0]
    data1        = fft.ifftshift(data)
    factor       = m
    if zero_padding == True:
        data1    = np.r_[data1[:m//2]
                      ,np.zeros_like(data1),data1[m//2:]]
        factor   = np.arange(m,0,-1)[:m//2]
    fft_data     = fft.fft(data1)
    correl_w     = np.abs(fft_data)**2
    correl       = fft.ifft(correl_w,axis=0).real[:m//2]/factor
    return time[:m//2],correl
