from os import path
import pandas as pd
import numpy as np
import sqlite3
import statsmodels.api as sm

class DataLoader():
    db_path = "./data/db.sqlite3"
    parquet_path = "./data/data.parquet"

    def get_df(self) -> pd.DataFrame:
        if path.exists(self.parquet_path):
            print("Loading cached data…")
            df = pd.read_parquet(self.parquet_path)
        else:
            print("Loading from SQLite…")
            conn = sqlite3.connect("./data/db.sqlite3")
            df = pd.read_sql_query("select * from ProjectDataset", conn)
            conn.close()
            df = self.model_project_df(df)
            df.to_parquet(self.parquet_path)
        return df
    
    def model_project_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace("NA", np.nan)
        df['decimalodds'] = pd.to_numeric(df['decimalodds'], errors='coerce')
        df['event_start'] = pd.to_datetime(df['event_start'], errors="coerce", utc=True)
        df['placed_date'] = pd.to_datetime(df['placed_date'])
        df['settled_date'] = pd.to_datetime(df['settled_date'])
        return df
    
    def load_daily_ggr(self):
        parquet_path = './data/daily_ggr.parquet'

        if path.exists(parquet_path):
            print("Loading cached data…")
            df = pd.read_parquet(parquet_path).copy()
        else:
            df = self.get_df()
            print('Loaded raw df')

            # Add day column
            df['day'] = df['event_start'].dt.floor('D')
            print('Added day column')

            # Aggregate GGR by day, sport, and bet type
            daily_ggr = df.groupby(['day', 'sportname', 'bet_type'])['ggr'].sum().reset_index()
            print('Aggregated GGR by day, sport, and bet type')

            # Cache to parquet
            daily_ggr.to_parquet(parquet_path)
            print('Saved parquet')

            df = daily_ggr

        return df
    
    def load_act_diversity_model(self):
        parquet_path = './data/act_diversity_model.parquet'
        if path.exists(parquet_path):
            print("Loading cached data…")
            df = pd.read_parquet(parquet_path).copy()
        else:
            df = self.get_df()
            player_df = df.groupby('playerid').agg(
                total_ggr=('ggr', 'sum'),
                total_bets=('wagerid', 'count'),
                total_stake=('net_stake', 'sum'),
                sport_diversity=('sportname', 'nunique'),
                type_diversity=('bet_type', 'nunique')
            ).reset_index()
            player_df.to_parquet(parquet_path)
            print('Saved parquet')
            df = player_df
        return df
    
    def load_model_coeffs(self):
        parquet_path = './data/model_coeffs.parquet'
        if path.exists(parquet_path):
            print("Loading cached data…")
            df = pd.read_parquet(parquet_path).copy()
        else:
            player_df = self.load_act_diversity_model()
            X = player_df[['sport_diversity','type_diversity','total_bets','total_stake']]
            X = sm.add_constant(X)
            y = player_df['total_ggr']
            model = sm.OLS(y, X).fit()
            coef_df = pd.DataFrame({
                "feature": model.params.index,
                "coef": model.params.values,
                "stderr": model.bse.values
            }).drop(index=0)  # drop intercept
            # Cache to parquet
            coef_df.to_parquet(parquet_path)
            print('Saved parquet')
            df = coef_df
        return df


