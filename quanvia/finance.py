import numpy as np
import pandas as pd
from datetime import date
from binance.client import Client

def get_data(asset_list = []):
    """ Obtains historic data from a list of assets using Binance's API

    Parameters
    ----------
    asset_list : list
        List of assets to retrieve information from

    Returns
    -------
    Dataframe
        A dataframe containing OHLV data from provided assets
    """
    client = Client()
    info = client.get_all_tickers()
    
    # Time frame
    today = date.today()
    yearago = today.replace(year = today.year -1).strftime("%Y.%m.%d")
    today = today.strftime("%Y.%m.%d")
    timeframe="1d"

    # Iterate for each asset
    data = {}
    for tick in info:
        asset = tick["symbol"]
        # We will filter the assets to work with
        if asset in asset_list:
            data[asset] = client.get_historical_klines(asset, timeframe, yearago, today)
            
    # Append all dataframes
    df = pd.DataFrame(columns=["Asset","Open time","Open","High","Low","Close","Volume", "Closing time","Quote asset vol", "Num traders", "Taker buy base asset vol", "Taker buy quote asset vol","To be ignored"])
    for asset in asset_list:
        df_tmp = pd.DataFrame(data[asset], columns=["Open time","Open","High","Low","Close","Volume", "Closing time","Quote asset vol", "Num traders", "Taker buy base asset vol", "Taker buy quote asset vol","To be ignored"])
        df_tmp["Asset"] = asset
        df = df.append(df_tmp)
            
    return df
    
def get_mu_sigma(data):
    """ Computes the expected returns for each asset at set time interval and their covariance

    Parameters
    ----------
    data : DataFrame
        DataFrame containg data about asset prices in USD at Close time

    Returns
    -------
    (mu, sigma) : tuple
        mu: mean value for each asset zero-padded
        sigma: covariance matriz between asset returns
    """
    asset_list = data["Asset"].unique()

    mu = {}
    return_list = []
    for asset in asset_list:
        num_list = np.array(data[data["Asset"] == asset]["Close"].astype("float"))
        # Sign will be used to indicate the value gradient direction
        returns = (num_list[1:]/num_list[:-1])-1
        mu[asset] = returns.mean()
        return_list.append(returns)
        
    # Compute covariance between returns
    sigma = np.cov(np.vstack(return_list))
    
    return (mu, sigma)
    