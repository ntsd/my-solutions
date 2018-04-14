<<<<<<< Updated upstream
import pandas as pd

data = pd.read_csv('bi-lstm.csv')
data["Criminal"] = [int(round(i))for i in data["Criminal"]]
data.to_csv('bi-lstm-round.csv',index=0)
=======
import pandas as pd
p=pd.read_csv('bi-lstm.csv')
p['Criminal']= [round(i) for i in p['Criminal']]
p.to_csv('bi-lstm-round.csv', index=0)
>>>>>>> Stashed changes
