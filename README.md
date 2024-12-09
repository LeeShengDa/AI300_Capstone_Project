# oct24-p02
AI300 Capstone (oct24-p02)
With CI/CD deployment (DOCKER and AWS)

Author: Lee Sheng Da
Date: December 2024

AWS Public URL: http://ec2-54-169-209-186.ap-southeast-1.compute.amazonaws.com/

Note: it is a http connection NOT https

Details of mode:
Final model chosen was the XGBoost Classifier as it outperforms Catboost model in Research phase
XGBoost Classifier model is efficient, accurate, and well-suited for structured data.

 RandomizedSearchCV hyperparameter tuning was performed and the below parameters were used:
 XGBClassifier(subsample = 1.0, reg_lambda = 2,
                                reg_alpha = 0.01, n_estimators = 100,
                                min_child_weight = 5, max_depth = 3,
                                learning_rate = 0.05, gamma = 0.2,
                                colsample_bytree = 1.0, verbosity = 0)

AUC Score: 0.869

Only 2 predictions output message:

"Customer is expected to Churn next month"
OR
"Customer is NOT expected to Churn next month"