import pandas as pd
import numpy as np
from modules.DataLoader import DataLoader

class Dataframes(DataLoader):

    def __init__(self):
        dl = DataLoader()
        self.project_df = dl.get_df()


    