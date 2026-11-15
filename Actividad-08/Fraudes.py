import datetime
import json
import logging
import pickle
import sys
import time
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, \
    classification_report
from sklearn.model_selection import train_test_split
import mlflow


class ModeloFraudes:
    def __init__(self, path_dataset:str="data/fraudes.csv", test_size=0.2, random_state=42, target:str="label",
                 n_estimators=100, max_features='sqrt', min_samples_split=2, min_samples_leaf=2, criterion='gini',
                 max_depth=100, class_weight='balanced', name:str="RandomForest"):
        self.random_state = random_state
        self.test_size = test_size
        self.target = target
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.max_depth = max_depth
        self.class_weight = class_weight
        self.name = name
        if path_dataset is None or path_dataset == "":
            raise ValueError("El dataset no se puede estar vacío")
        if test_size <= 0.0 or test_size >= 1.0:
            raise ValueError("El valor de test_size debe ser entre 0 y 1")
        try:
            self.df = pd.read_csv(filepath_or_buffer=path_dataset)
        except FileNotFoundError:
            print("El archivo no existe")
        self.nombre_dataset = path_dataset
        try:
            x = self.df.drop(columns=[target])
            y = self.df[target]

        except ValueError:
            print(f"El nombre {target} no existe en el Dataset")
            raise ValueError(f"El nombre {target} no existe en el Dataset")

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x,y, test_size=test_size, random_state=random_state)
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            criterion=criterion,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            random_state=random_state,
            class_weight=class_weight,
            max_depth=max_depth,
        )

        self.y_pred = None
        self.results = {}
        self.confusion_matrix = None
        self.report = None

    def train(self):
        print("Entrenando modelo")
        self.model.fit(self.X_train, self.y_train)
        with open(f"models/RandomForest{self.name}.pkl", "wb") as file:
            pickle.dump(self.model, file)

    def evaluate(self, X_test:pd.DataFrame, y_test:pd.DataFrame, umbral:float=0.25, simulate_time_out:bool=False):
        print("Evaluando modelo")
        time_init = time.time()
        if simulate_time_out:
            time.sleep(1.5)
        if not X_test.empty:
            self.X_test = X_test
        if not y_test.empty:
            self.y_test = y_test

        proba = self.model.predict_proba(self.X_test)[:,1]
        self.y_pred = (proba > umbral).astype(int)
        latency = (time.time() - time_init)*1000

        self.results["Latency"] = round(latency, 4)
        self.results["Accuracy"] = round(accuracy_score(self.y_test, self.y_pred), 4)
        self.results["Precision"] = round(precision_score(self.y_test, self.y_pred), 4)
        self.results["Recall"]= round(recall_score(self.y_test, self.y_pred), 4)
        self.results["F1_score"] = round(f1_score(self.y_test, self.y_pred), 4)
        self.results["Roc_auc"] = round(roc_auc_score(self.y_test, self.y_test), 4)

        self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred)
        self.report = classification_report(
            self.y_test,
            self.y_pred,
            output_dict=True
        )

        return self.results

    def predict(self, init_balance:float, tx_amount:float, hist_amount:float,client_incomes:float,incorporate_days:int):
        y_pred = None
        try:
            data = {"INIT_BALANCE":init_balance,
                    "TX_AMOUNT":tx_amount,
                    "HIST_AMOUNT":hist_amount,
                    "CLIENT_INCOMES":client_incomes,
                    "INCORPORATION":incorporate_days}
            X = pd.DataFrame(data, index=[0])
            y_pred = self.model.predict(X)
        except NotFittedError as e:
            print(f"Debe realizar primero en entrenamiento antes de llamar al predict, {e}")
        return y_pred


class MonitorModel:
    def __init__(self, modelo:ModeloFraudes):
        if modelo is None:
            raise ValueError("Modelo no valido")
        self.modelo = modelo
        mlflow.set_experiment(f"Modelo {self.modelo.name} - monitoring")

        self.run = None
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("monitor.log"),
                logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger("MonitorModel")
        self.slo = {
            "latency_max_mx": 500,
            "accuracy_min": 0.90,
            "precision_min": 0.95,
            "recall_min": 0.98,
            "f1_min": 0.95,
            "roc_auc_min": 0.95,
        }


    def verify_slos(self, metricas_nuevas:dict):
        errors = {}
        if metricas_nuevas is None:
            raise ValueError("Metricas nuevas no validas")
        if metricas_nuevas["Latency"] > self.slo["latency_max_mx"]:
            latency = metricas_nuevas["Latency"]
            errors["Latencia"] = f"Latencia {latency} debe ser menor de {self.slo['latency_max_mx']}"
        if metricas_nuevas["Accuracy"] < self.slo["accuracy_min"]:
            accuracy = metricas_nuevas["Accuracy"]
            errors["Accuracy"] = f"Accuracy {accuracy} debe ser mayor de {self.slo['accuracy_min']}"
        if metricas_nuevas["Precision"] < self.slo["precision_min"]:
            precision = metricas_nuevas["Precision"]
            errors["Precision"] = f"Precision {precision} debe ser mayor de {self.slo['precision_min']}"
        if metricas_nuevas["Recall"] < self.slo["recall_min"]:
            recall = metricas_nuevas["Recall"]
            errors["Recall"] = f"Recall {recall} debe ser mayor de {self.slo['recall_min']}"
        if metricas_nuevas["F1_score"] < self.slo["f1_min"]:
            f1 = metricas_nuevas["F1_score"]
            errors["F1"] = f"F1-score {f1} debe ser mayor de {self.slo['f1_min']}"
        if metricas_nuevas["Roc_auc"] < self.slo["roc_auc_min"]:
            roc_auc = metricas_nuevas["Roc_auc"]
            errors["Roc_auc"] = f"ROC_AUC {roc_auc} debe ser mayor de {self.slo['roc_auc_min']}"
        return errors

    def execute_monitoring(self, monitor_name:str, umbral:float=0.25, degrada:bool=False, normal_degradado_simulation:float=3.0, simulate_time_out:bool=False):

        self.logger.info(f"Monitoring {monitor_name}")
        if degrada:
            self.logger.warning(f"Simulando degradado del modelo")
            X_test = self.modelo.X_test * normal_degradado_simulation
            X_train = self.modelo.X_train * normal_degradado_simulation
        else:
            X_test = self.modelo.X_test
            X_train = self.modelo.X_train


        y_test = self.modelo.y_test
        metricas = self.modelo.evaluate(X_test, y_test, umbral=umbral, simulate_time_out=simulate_time_out)
        errors = self.verify_slos(metricas)

        self.run = mlflow.start_run(
            run_name=self.modelo.name
        )
        mlflow.set_tags({
                "monitor_name": monitor_name,
                "Model":self.modelo.model,
                "Dataset":self.modelo.nombre_dataset,
                "umbral":umbral,
                "degradado":str(degrada),
                "timestamp":str(datetime.datetime.now())
            })
        mlflow.log_params({
                "n_estimators": self.modelo.n_estimators,
                "max_features": self.modelo.max_features,
                "min_samples_leaf": self.modelo.min_samples_leaf,
                "test_size": self.modelo.test_size,
                "random_state": self.modelo.random_state,
                "criterion": self.modelo.criterion,
                "max_depth": self.modelo.max_depth,
                "class_weight": self.modelo.class_weight,
                "slo_accuracy_min": self.slo["accuracy_min"],
                "slo_precision_min": self.slo["precision_min"],
                "slo_recall_min": self.slo["recall_min"],
                "slo_f1_min": self.slo["f1_min"],
                "slo_roc_auc_min": self.slo["roc_auc_min"],
                "slo_latency_max_mx": self.slo["latency_max_mx"],
            })
            # -- Métricas --
        mlflow.log_metrics(metricas)
        mlflow.log_metric("slo_violations", len(errors))
        mlflow.log_metric("error_recall_dif",max(0,self.slo["recall_min"]-metricas["Recall"]))
        mlflow.log_metric("error_accuracy_dif", max(0, self.slo["accuracy_min"] - metricas["Accuracy"]))
        mlflow.log_metric("error_f1_dif", max(0, self.slo["f1_min"] - metricas["F1_score"]))
        mlflow.log_metric("error_precision_dif", max(0, self.slo["precision_min"] - metricas["Precision"]))
        mlflow.log_metric("error_latency_dif", max(0, metricas["Latency"] - self.slo["latency_max_mx"]))
            # -- Logs --
        if errors:
                self.logger.error(f"Errors durante el experimento SLO superados: {errors}")
                print("Errors durante el experimento SLO superados:")
                for error in errors:
                    self.logger.error(f"{errors[error]}")
                    print(f"{errors[error]}")
                mlflow.set_tag("status","SLO superado")

                if 'Latencia' in errors:
                    self.runbook_alta_latencia(errors)
                if 'Accuracy' in errors or 'F1' in errors or 'Precision' in errors or 'Recall' in errors or 'Roc_auc' in errors:
                    y_train = self.modelo.y_train
                    self.runbook_reentrena_modelo(X_train, y_train, X_test, y_test, errors)
        else:
                self.logger.info(f"SLO dentro de los umbrales")
                print("SLO dentro de los umbrales")
                mlflow.set_tag("status","OK")
        # -- Artefactos --
        self.log_confusion_matrix()
        self.log_report()

        # -- Guardar Modelo --
        mlflow.sklearn.log_model(
            sk_model=self.modelo.model,
            name="Modelo Fraudes - RandomForest",
            skops_trusted_types=["sklearn.tree._tree.Tree"],
        )
        mlflow.end_run()

    def log_confusion_matrix(self,result_path='./results/'):

        cm = self.modelo.confusion_matrix
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        file_name = result_path + 'confusion_matrix.png'
        plt.savefig(file_name)
        plt.close()
        mlflow.log_artifact(file_name)

    def log_report(self,result_path='./results/'):
        report_file = result_path + 'classification_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.modelo.report, f, indent=4)
        mlflow.log_artifact(report_file)

    def runbook_reentrena_modelo(self,X_train, y_train, X_test, y_test, errors):
        self.logger.info(f"RUNBOOK-01 - REENTRENA modelo iniciando {datetime.datetime.now().isoformat()}")
        self.logger.info(f"1) Causa del error: DataDrift detectado")
        self.logger.info(f"2) Descargando datos actualizados")
        self.modelo.X_train = X_train
        self.modelo.y_train = y_train
        self.logger.info(f"3) Comenzando reentrenamiento")
        self.modelo.train()
        self.logger.info(f"4) Evaluando modelo reentrenado")
        eval_reentrenamiento = self.modelo.evaluate(X_test, y_test)
        self.logger.info(f"5) Verificando SLOs del reentrenamiento")
        errors = self.verify_slos(eval_reentrenamiento)
        if errors:
            self.logger.error(f"Errors durante el reentrenamiento, Nuevo modelo no cumple los SLOs: {errors}")
            self.logger.info(f"Necesario escalar con el equipo técnico de ML")
        else:
            self.logger.info(f"Nuevo modelo cumple los SLOs: {eval_reentrenamiento}")
        self.logger.info(f"RUNBOOK-01 - REENTRENA modelo completado {datetime.datetime.now().isoformat()}")

        return eval_reentrenamiento

    def runbook_alta_latencia(self, errors):
        self.logger.info(f"RUNBOOK-02 - ALTA latencia del modelo iniciando {datetime.datetime.now().isoformat()}")
        self.logger.info(f"1) Latencia detectada: {errors.get('Latencia')}")
        self.logger.info(f"2) Causa - Saturación de servidores actual")
        self.logger.info(f"3) Resolución - Desplegando nuevo servidor (escalando infraestructura) - SIMULACIÓN")
        time.sleep(5)
        self.logger.info(f"4) Verificando recuperación de SLOs de Latencia")
        latencia_nueva = 357
        self.logger.info(f"Latencia detectada: {latencia_nueva}ms")
        self.logger.info(f"Error registrado en el log de incidentes")
        self.logger.info(f"RUNBOOK-02 - ALTA latencia del modelo completado {datetime.datetime.now().isoformat()}")






