import numpy as np
import pandas as pd
from datetime import date
from binance.client import Client

def get_binance_assets():
    """ Obtains list of assets using Binance's API

    Returns
    -------
    Dict
        A list containing available assets
    """
    client = Client()
    info = client.get_all_tickers()
    output = [x["symbol"] for x in info]
     
    return output

def get_binance_data(asset_list = []):
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
        if len(data[asset]) >= 365:
            df_tmp = pd.DataFrame(data[asset], columns=["Open time","Open","High","Low","Close","Volume", "Closing time","Quote asset vol", "Num traders", "Taker buy base asset vol", "Taker buy quote asset vol","To be ignored"])
            df_tmp["Asset"] = asset
            df = df.append(df_tmp)
            
    return df
    
def get_exp_cov(data):
    """ Computes the expected returns for each asset at set time interval and their covariance

    Parameters
    ----------
    data : DataFrame
        DataFrame containg data about asset prices in USD at Close time

    Returns
    -------
    (exp_ret, cov_mat) : tuple
        exp_ret: mean value on the expected return for each asset zero-padded
        cov_mat: covariance matriz between asset returns
    """
    asset_list = data["Asset"].unique()

    exp_ret = {}
    return_list = []
    for asset in asset_list:
        open_price = np.array(data[data["Asset"] == asset]["Open"].astype("float"))
        close_price = np.array(data[data["Asset"] == asset]["Close"].astype("float"))
        # Sign will be used to indicate the value gradient direction
        returns = ((close_price - open_price)/open_price)
        exp_ret[asset] = returns.mean()
        return_list.append(returns)
        
    # Compute covariance between returns
    cov_mat = np.cov(np.vstack(return_list))
    
    return (exp_ret, cov_mat)
    