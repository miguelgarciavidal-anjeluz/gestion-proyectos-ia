import hashlib
import json
import logging

import joblib
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import seaborn as sns
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import (
    train_test_split,
    cross_validate,
    GridSearchCV,
    StratifiedKFold
)


class ClassificationTrainer:

    def __init__(
            self,
            csv_path,
            target_column,
            model_name='logistic_regression',
            experiment_name='ClassificationExperiment',
            registered_model_name='ClassificationModel',
            tracking_uri='http://localhost:5000',
            test_size=0.2,
            random_state=42
    ):

        self.csv_path = csv_path
        self.target_column = target_column
        self.model_name = model_name
        self.experiment_name = experiment_name
        self.registered_model_name = registered_model_name
        self.test_size = test_size
        self.random_state = random_state

        self.model = None
        self.best_model = None
        self.run = None

        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

        logging.basicConfig(
            filename='training.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def load_data(self):
        df = pd.read_csv(self.csv_path)

        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            stratify=y,
            random_state=self.random_state
        )

        logging.info(f'Dataset cargado: {df.shape}')

    def register_dataset_metadata(self):
        df = pd.read_csv(self.csv_path)

        dataset_hash = hashlib.md5(
            pd.util.hash_pandas_object(df, index=True).values
        ).hexdigest()

        mlflow.log_param('dataset_path', self.csv_path)
        mlflow.log_param('dataset_rows', len(df))
        mlflow.log_param('dataset_columns', len(df.columns))
        mlflow.log_param('dataset_hash', dataset_hash)

    def create_model(self):

        models = {
            'logistic_regression': LogisticRegression(
                max_iter=1000,
                random_state=self.random_state
            ),
            'random_forest': RandomForestClassifier(
                random_state=self.random_state
            )
        }

        if self.model_name not in models:
            raise ValueError(f'Modelo no soportado: {self.model_name}')

        self.model = models[self.model_name]

    def start_experiment(self):

        self.run = mlflow.start_run(
            run_name=self.model_name
        )

        mlflow.log_param('model_name', self.model_name)
        mlflow.log_param('target_column', self.target_column)
        mlflow.log_param('test_size', self.test_size)
        mlflow.log_param('random_state', self.random_state)

        mlflow.set_tags({
            'algorithm': self.model_name,
            'target': self.target_column
        })

    def cross_validation(self, cv=5):

        scoring = {
            'accuracy': 'accuracy',
            'precision': 'precision',
            'recall': 'recall',
            'f1': 'f1',
            'roc_auc': 'roc_auc'
        }

        results = cross_validate(
            self.model,
            self.X_train,
            self.y_train,
            cv=cv,
            scoring=scoring
        )

        summary = {}

        for metric, values in results.items():
            if metric.startswith('test_'):
                metric_name = metric.replace('test_', '')
                metric_value = np.mean(values)
                summary[metric_name] = metric_value
                mlflow.log_metric(
                    f'cv_{metric_name}',
                    metric_value
                )

        return summary

    def hyperparameter_tuning(self, param_grid, cv=5):

        strategy = StratifiedKFold(
            n_splits=cv,
            shuffle=True,
            random_state=self.random_state
        )

        grid = GridSearchCV(
            estimator=self.model,
            param_grid=param_grid,
            scoring='f1',
            cv=strategy,
            n_jobs=-1
        )

        grid.fit(self.X_train, self.y_train)

        self.best_model = grid.best_estimator_

        mlflow.log_params(grid.best_params_)
        mlflow.log_metric('best_cv_score', grid.best_score_)

        return grid.best_params_, grid.best_score_

    def train(self):

        model = self.best_model or self.model
        model.fit(self.X_train, self.y_train)

    def evaluate(self):

        model = self.best_model or self.model

        y_pred = model.predict(self.X_test)

        metrics = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred),
            'recall': recall_score(self.y_test, y_pred),
            'f1': f1_score(self.y_test, y_pred)
        }

        if hasattr(model, 'predict_proba'):
            y_prob = model.predict_proba(self.X_test)[:, 1]
            metrics['roc_auc'] = roc_auc_score(
                self.y_test,
                y_prob
            )

        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        return metrics

    def log_confusion_matrix(self, result_path='./results/'):

        model = self.best_model or self.model

        y_pred = model.predict(self.X_test)

        cm = confusion_matrix(self.y_test, y_pred)

        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.tight_layout()

        file_name = result_path + 'confusion_matrix.png'
        plt.savefig(file_name)
        plt.close()

        mlflow.log_artifact(file_name)

    def log_classification_report(self, result_path: str = './results/'):

        model = self.best_model or self.model

        y_pred = model.predict(self.X_test)

        report = classification_report(
            self.y_test,
            y_pred,
            output_dict=True
        )

        report_file = result_path + 'classification_report.json'

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=4)

        mlflow.log_artifact(report_file)

    def save_local_model(self, path='model.pkl'):

        model = self.best_model or self.model
        joblib.dump(model, path)

    def save_and_register_model(self):

        model = self.best_model or self.model

        predictions = model.predict(self.X_test)

        signature = infer_signature(
            self.X_test,
            predictions
        )

        return mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            registered_model_name=self.registered_model_name,
            serialization_format="cloudpickle"
        )

    def promote_to_staging(self):

        client = MlflowClient()

        versions = client.search_model_versions(
            f"name='{self.registered_model_name}'"
        )

        latest = max(versions, key=lambda x: int(x.version))

        client.transition_model_version_stage(
            name=self.registered_model_name,
            version=latest.version,
            stage='Staging'
        )

    def promote_to_production(self, min_f1=0.80):

        results = self.evaluate()

        if results['f1'] < min_f1:
            return False

        client = MlflowClient()

        versions = client.search_model_versions(
            f"name='{self.registered_model_name}'"
        )

        latest = max(versions, key=lambda x: int(x.version))

        client.transition_model_version_stage(
            name=self.registered_model_name,
            version=latest.version,
            stage='Production'
        )

        return True

    def load_production_model(self):
        return mlflow.pyfunc.load_model(
            f'models:/{self.registered_model_name}/Production'
        )

    def end_experiment(self):
        mlflow.end_run()
