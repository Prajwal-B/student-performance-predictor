from flask import Flask, request, render_template
import os

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
from src.logger import logging

application = Flask(__name__)

app = application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Validate required fields
            required_fields = ['gender', 'ethnicity', 'parental_level_of_education', 
                             'lunch', 'test_preparation_course', 'reading_score', 'writing_score']
            
            for field in required_fields:
                if not request.form.get(field):
                    return render_template('home.html', 
                                        error=f"Missing required field: {field.replace('_', ' ').title()}")

            # Validate score ranges
            try:
                reading_score = float(request.form.get('reading_score'))
                writing_score = float(request.form.get('writing_score'))
                
                if not (0 <= reading_score <= 100):
                    return render_template('home.html', 
                                        error="Reading score must be between 0 and 100")
                if not (0 <= writing_score <= 100):
                    return render_template('home.html', 
                                        error="Writing score must be between 0 and 100")
            except ValueError:
                return render_template('home.html', 
                                    error="Scores must be valid numbers")

            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=reading_score,
                writing_score=writing_score
            )
            
            pred_df = data.get_data_as_data_frame()
            logging.info(f"Prediction input: {pred_df.to_dict()}")

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            
            predicted_score = round(results[0], 2)
            logging.info(f"Predicted math score: {predicted_score}")
            
            return render_template('home.html', results=predicted_score)
        
        except CustomException as e:
            logging.error(f"Custom exception: {str(e)}")
            return render_template('home.html', error=f"Prediction error: {str(e)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return render_template('home.html', error="An unexpected error occurred. Please try again.")


@app.errorhandler(404)
def not_found(error):
    return render_template('home.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('home.html', error='Internal server error'), 500


if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)        


