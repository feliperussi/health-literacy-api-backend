import pandas as pd
from model_gb import GradientBoostingModel
from model_rf import RandomForestModel
from model_emd import EMDistanceModel

gb_model = GradientBoostingModel('C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/models/model_gb.pkl', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/weights.json', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/columns.json')
rf_model = RandomForestModel('C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/models/model_gb.pkl', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/weights.json', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/columns.json')
emd_model = EMDistanceModel('C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/weights.json', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/means_label_0.json', 'C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/means_label_1.json')

df = pd.read_csv("C:/Users/felip/Downloads/api-20230308T032233Z-001/api/app/data/test_set/data_test.csv").iloc[0]

print(gb_model.predict(df))
print(rf_model.predict(df))
# print(emd_model.predict(df)[0])