from flask import Flask, request, render_template
from model import Model
import pandas as pd
from datetime import datetime
import pytz


app = Flask(__name__)

# Initialize the global prediction counter and history
prediction_counter = 0
prediction_history = []

# Method: Via HTML Form
@app.route('/', methods=['GET', 'POST'])
def home():
    global prediction_counter, prediction_history  # Declare as global to modify the global variables
    if request.method == 'POST':
        # Increment the prediction counter
        prediction_counter += 1
        form_input = dict(request.form)

        total_refunds = float(form_input['total_refunds'])
        tenure_months = int(form_input['tenure_months'])
        num_referrals = int(form_input['num_referrals'])

        has_premium_tech_support = str(form_input['has_premium_tech_support'])
        contract_type = str(form_input['contract_type'])
        has_dependents = str(form_input['has_dependents'])

        # raw_dict used for html output only. to show what inputs was used to predict
        raw_dict = { "total_refunds": total_refunds,
             "tenure_months": tenure_months,
             "num_referrals": num_referrals,
                "contract_type": contract_type,
             "has_dependents": has_dependents,
             "has_premium_tech_support": has_premium_tech_support
            }

        if has_premium_tech_support == "Yes":
            has_premium_tech_support_Yes = True
        else: 
            has_premium_tech_support_Yes = False

        if contract_type == "One Year":
            contract_type_One_Year = True
            contract_type_Two_Year = False
        elif contract_type == "Two Year":
            contract_type_One_Year = False
            contract_type_Two_Year = True
        else:
            contract_type_One_Year = False
            contract_type_Two_Year = False

        if has_dependents == "Yes":
            has_dependents_1 = True
        else: 
            has_dependents_1 = False

        # commented. below is used for testing without using html inputs interface.
        # model_inputs = pd.DataFrame(
        #     { "total_refunds": float(0.2),
        #      "tenure_months": int(10),
        #      "num_referrals": int(2),
        #         "contract_type_One_Year": contract_type_One_Year,
        #      "contract_type_Two_Year": contract_type_Two_Year,
        #      "has_dependents_1": True,
        #      "has_premium_tech_support_Yes": True
             
        #     }, index=[0])


        input_dict = { "total_refunds": total_refunds,
             "tenure_months": tenure_months,
             "num_referrals": num_referrals,
                "contract_type_One_Year": contract_type_One_Year,
             "contract_type_Two_Year": contract_type_Two_Year,
             "has_dependents_1": has_dependents_1,
             "has_premium_tech_support_Yes": has_premium_tech_support_Yes
            }
        
        # used to generate tinestamp of prediction
        gmt_plus_8 = pytz.timezone('Asia/Singapore')
        current_time_gmt8 = datetime.now(gmt_plus_8)
        formatted_time_gmt8 = current_time_gmt8.strftime("%Y-%m-%d %H:%M:%S")

        model_inputs = pd.DataFrame(input_dict, index=[0])
        prediction = Model().predict(model_inputs)

        # Store the prediction and timestamp in the history
        prediction_history.append({
            'timestamp': formatted_time_gmt8,
            'prediction': prediction
        })

        # Keep only the last 10 predictions
        if len(prediction_history) > 20:
            prediction_history = prediction_history[-10:]

        # initialise only. 
        out_text = "Please enter variables and click Predict"

        if prediction == True:
            out_text = "Customer is expected to Churn next month"


        elif prediction == False:
            out_text = "Customer is NOT expected to Churn next month"

        return render_template('index.html',timestamp = formatted_time_gmt8, input_variables = str(raw_dict),prediction=out_text, prediction_count=prediction_counter, prediction_history=prediction_history)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
