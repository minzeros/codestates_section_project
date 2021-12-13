import os
import csv
import sqlite3
from flask import Flask, render_template, request

# CSV 파일 경로와 임시 파일 경로입니다.
CSV_FILEPATH = os.path.join(os.getcwd(), 'hotel.csv') 

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'GET':
        text = ''
        return render_template('index.html', cancel=text)
    elif request.method=='POST':
        import pandas as pd
        from sklearn.pipeline import make_pipeline
        from category_encoders import OrdinalEncoder
        from xgboost import XGBClassifier

        hotel_df = pd.read_csv('./hotel.csv')
        hotel_df.drop('Unnamed: 0', axis=1, inplace=True)

        target = 'is_canceled'
        features = hotel_df.drop(target, axis=1).columns

        X_train = hotel_df[features]
        y_train = hotel_df[target]

        # enc = OneHotEncoder()
        # scaler = StandardScaler()
        # model_rf = RandomForestClassifier(random_state=1, max_depth=7)

        # X_train_encoded = enc.fit_transform(X_train)
        # X_train_scaled = scaler.fit_transform(X_train_encoded)
        # model_rf.fit(X_train_scaled, y_train)

        # pipe = make_pipeline(
        #     OrdinalEncoder(),
        #     RandomForestClassifier(n_jobs=-1, random_state=10, oob_score=True)
        # )
        # pipe.fit(X_train, y_train)


        pipe = make_pipeline(
            OrdinalEncoder(),
            XGBClassifier(n_estimators=200
                        , random_state=2
                        , n_jobs=-1
                        , max_depth=7
                        , learning_rate=0.2
                        , use_label_encoder=False
                        , eval_metric='logloss'
                        )
        )

        pipe.fit(X_train, y_train)

        month = request.form.get('arrival_date_month')
        day = request.form.get('arrival_date_day_of_month', type=int)
        lead_time = request.form.get('lead_time')
        week = request.form.get('stays_in_week_nights', type=int)
        weekend = request.form.get('stays_in_weekend_nights', type=int)
        adult = request.form.get('adults', type=int)
        children = request.form.get('children', type=int)
        baby = request.form.get('babies', type=int)
        repeated_guest = request.form.get('is_repeated_guest', type=int)
        adr = request.form.get('adr', type=float)
        parking = request.form.get('required_car_parking_spaces', type=int)
        special = request.form.get('total_of_special_requests', type=int)

        test_df = pd.DataFrame({
            'lead_time' : [lead_time],
            'arrival_date_month' : [month],
            'arrival_date_day_of_month' : [day],
            'stays_in_weekend_nights' : [weekend],
            'stays_in_week_nights' : [week],
            'adults' : [adult],
            'children' : [children],
            'babies' : [baby],
            'is_repeated_guest' : [repeated_guest],
            'adr' : [adr],
            'required_car_parking_spaces' : [parking],
            'total_of_special_requests' : [special]
        })

        proba_cancel = round(pipe.predict_proba(test_df)[0][1] * 100, 2)

        return render_template('index.html', proba_cancel=proba_cancel)
    

if __name__ == "__main__":
    app.run(debug=True)