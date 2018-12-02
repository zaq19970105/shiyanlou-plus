import sys
from pymongo import MongoClient
import pandas as pd

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    df = pd.DataFrame(list(contests.find()))
    df = df.iloc[:, 2:].groupby('user_id').sum()
    df.sort_values(by='submit_time', inplace=True)
    df.sort_values(by='score', ascending=False, inplace=True)
    df.reset_index(inplace=True)
    data = df[df['user_id'] == user_id]
    return data.index.values[0]+1, data.score.values[0], data.submit_time.values[0]

if __name__ == '__main__':
    user_id = int(sys.argv[1])
    userdata = get_rank(user_id)
    print(userdata)
