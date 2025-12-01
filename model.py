from modules.Dataframes import Dataframes
import statsmodels.api as sm

dfs = Dataframes()
player_df = dfs.load_act_diversity_model()

corr = player_df[['total_ggr','sport_diversity','type_diversity','total_bets','total_stake']].corr()
print(corr)

X = player_df[['sport_diversity','type_diversity','total_bets','total_stake']]
X = sm.add_constant(X)
y = player_df['total_ggr']

model = sm.OLS(y, X).fit()
print(model.summary())
