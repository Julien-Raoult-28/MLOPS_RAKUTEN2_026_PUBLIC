# FEV26-CMLOPS-RAKUTEN
├── api       
├── data               
│   ├── processed    <-data préparées->  
│   │   │                 
│   │   ├── Y_train_encode.csv 
│   │   
│   └── raw          <-data d'origine->   
│   │   │                 
│   │   ├── X_test_update.csv 
│   │   ├── X_train_update.csv 
│   │   ├── Y_train_CVw08PX.csv 
│
├── models           <-models .pkl ou .joblib-> 
│   ├── 1.3_rakuten_model_final.pkl  
│
├── notebooks 
│   ├──Entrainement_test.ipynb   
│   ├──grid_search.ipynb           
│
├── requirements.txt   
│                         
├── src               
│   ├──data   <-code pour préparer les data-> 
│   │
│   │
│   ├── models   <-code pour générer le models .pkl ou .joblib->      
│   │   │                 
│   │   ├── 1.2_model_prediction.py
│   │
├── LICENSE
├── .gitignore
├── README.md  