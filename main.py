import pandas as pd
import matplotlib.pyplot as plt
import glob

# constants
# column names
column = {"time": "timestamp", "power": "power", "price": "price"}
# folders
price_folder = "electricityData"
devices_folder = "devices"
# devices
INFO_FILE = "0_smart_plugs_devices"


def import_electricity_data(country: str) -> pd.DataFrame:
    """
    Import the electricity data from the csv file and plot the price per hour of the day.
    :param country: the name of the country
    :return: dataframe of the electricity data. The dataframe contains the date (as datetime) and price columns.
    """
    df = pd.read_csv(price_folder + "/" + country + '.csv')
    df = df[["Datetime (Local)", "Price (EUR/MWhe)"]]
    df = df.rename(columns={"Datetime (Local)": column["time"], "Price (EUR/MWhe)": column["price"]})
    df['Date'] = pd.to_datetime(df[column["time"]], format='%Y-%m-%d %H:%M:%S')
    return df


def calculate_average_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the average values of the columns per hour of the day
    :param df: dataframe containing the date (as datetime) and other numerical columns to be calculated.
    :return: the dataframe containing the averages per hour of the day
    """
    df[column["time"]] = pd.to_datetime(df[column["time"]])
    hourly = df.groupby(df[column["time"]].dt.hour).mean()
    hourly[column["time"]] = hourly.index
    # rename all columns except the time column to Average <column name>
    # [hourly.rename(columns={col: "Average " + col}, inplace=True) for col in hourly.columns if col != column["time"]]
    return hourly


def import_devices(folder: str) -> dict[str, pd.DataFrame]:
    """
    Import the devices from the csv files.
    :param folder: the name of the folder containing the devices
    :return: dictionary of the devices. The key is the name of the device and the value is the dataframe of the device.
    """
    devices = {}
    for file in glob.glob(folder + '/*.csv'):
        device_name = file.split('/')[1].split('.')[0]
        if device_name == INFO_FILE:
            continue
        device_df = pd.read_csv(file)
        device_df['timestamp'] = pd.to_datetime(device_df['timestamp'])
        devices.update({device_name: device_df})
    return devices


def main():
    """
    Main function
    :return: None
    """
    # import the electricity data
    electricity_df = import_electricity_data("Spain")
    # plot the average price per hour of the day
    price_avg_df = calculate_average_per_hour(electricity_df)
    price_avg_df.plot(x=column["time"], y=column["price"], title="Average price per hour of the day")
    # import the devices
    devices = import_devices(devices_folder)
    # plot the average power consumption per hour of the day for each device
    for device_name, device_df in devices.items():
        average_df = calculate_average_per_hour(device_df)
        average_df.plot(x=column["time"], y=column["power"], title=device_name)
    plt.show()


if __name__ == '__main__':
    main()
