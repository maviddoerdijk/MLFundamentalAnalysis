# workflows.py
import os
from financetoolkit import Toolkit
import pandas as pd
import matplotlib.pyplot as plt
from logger import get_logger
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from data_processing import load_data, preprocess_data, split_data, prepare_financial_data
from models import train_model, evaluate_model, preprocess_training_data, train_linear_regression, evaluate_regression_model


logger = get_logger(__name__)

class Workflows:
    def __init__(self, config):
        self.config = config

    def run_classification(self):
        logger.info('Running classification workflow')

        # Load and preprocess data
        data = load_data(self.config['data_path'])
        data = preprocess_data(data)

        # Split data
        X_train, X_test, y_train, y_test = split_data(data)

        # Preprocess training data
        X_train, X_test, sc = preprocess_training_data(X_train, X_test)

        # Train model   
        model = train_model(X_train, y_train, **self.config['classification']['model_params'])

        # Evaluate model
        accuracy, y_pred = evaluate_model(model, X_test, y_test)
        logger.info(f'Accuracy: {accuracy:.2f}')

        # Plot results as confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.savefig('plots/confusion_matrix.png')
        plt.clf()
        
        
    def run_regression(self):
        logger.info('Running regression workflow')

        # Load and preprocess data
        data = load_data(self.config['data_path'])
        data = preprocess_data(data)
        

        # Split data
        X_train, X_test, y_train, y_test = split_data(data)

        # Preprocess training data
        X_train, X_test, sc = preprocess_training_data(X_train, X_test)

        # Train and evaluate MLP model (classification)
        model_mlp = train_model(X_train, y_train, **self.config['classification']['model_params'])
        accuracy, y_pred_mlp = evaluate_model(model_mlp, X_test, y_test)
        logger.info(f'MLP Accuracy: {accuracy:.2f}')

        # Train and evaluate Linear Regression model (regression)
        model_lr = train_linear_regression(X_train, y_train)
        mse, y_pred_lr = evaluate_regression_model(model_lr, X_test, y_test)
        logger.info(f'Linear Regression MSE: {mse:.2f}')


        # Plot results
        plt.scatter(y_test, y_pred_lr)
        plt.xlabel('Actual EPS')
        plt.ylabel('Predicted EPS')
        plt.title('Actual vs Predicted EPS')
        plt.savefig('plots/actual_vs_predicted.png')
        plt.clf()
        
    def run_revenue_prediction(self):
        logger.info('Running revenue prediction workflow')

        # Fetch financial data using finance_toolkit
        companies = Toolkit(["AAPL", "MSFT"], api_key=os.getenv('FINANCIAL_MODELING_PREP_API_KEY'), start_date="2017-12-31")

        income_statement = companies.get_income_statement()
        

        # Prepare the data for revenue prediction
        input_feature_names = ['Gross Profit', 'Cost of Goods Sold', 'Research and Development Expenses']
        X, y = prepare_financial_data(income_statement, input_feature_names)
        X_train, X_test, y_train, y_test = split_data(pd.concat([X, y], axis=1))

        # Preprocess training data
        X_train, X_test, sc = preprocess_training_data(X_train, X_test)

        # Train and evaluate Linear Regression model (for revenue prediction)
        model_lr = train_linear_regression(X_train, y_train)
        mse, y_pred_lr = evaluate_regression_model(model_lr, X_test, y_test)
        logger.info(f'Linear Regression MSE: {mse:.2f}')

        # Plot results
        plt.scatter(y_test, y_pred_lr)
        plt.xlabel('Actual Revenue')
        plt.ylabel('Predicted Revenue')
        plt.title('Actual vs Predicted Revenue')
        plt.savefig('plots/actual_vs_predicted_revenue.png')
        plt.clf()