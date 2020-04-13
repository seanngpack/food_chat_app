import food_chat_app.models.scraper.webscraper as webscraper
import time
import pandas as pd

if __name__ == '__main__':
    # print('getting...')
    # webscraper.run('data/restaurant_data5.csv', 100, 200)
    # time.sleep(10)
    # print('getting...')
    # webscraper.run('data/restaurant_data1.csv', 200, 400)
    # time.sleep(10)
    # print('getting...')
    # webscraper.run('data/restaurant_data2.csv', 400, 600)
    # time.sleep(10)
    # print('getting...')
    # webscraper.run('data/restaurant_data3.csv', 600, 800)
    # time.sleep(10)
    # print('getting...')
    # webscraper.run('data/restaurant_data4.csv', 800, 1000)
    # time.sleep(10)
    # print('getting...')
    # webscraper.run('data/restaurant_data5.csv', 1000, 1200)
    # time.sleep(10)

    df0=pd.read_csv("data/restaurant_data0.csv")
    df1=pd.read_csv("data/restaurant_data1.csv")
    df2=pd.read_csv("data/restaurant_data2.csv")
    df3=pd.read_csv("data/restaurant_data3.csv")
    df4=pd.read_csv("data/restaurant_data4.csv")
    df5=pd.read_csv("data/restaurant_data5.csv")

    full_df = pd.concat([df0,df1,df2,df3,df4,df5])
    final_df = full_df.drop_duplicates(keep='last')
    final_df.to_csv('data/restaurant_data.csv', index=False)
