from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import *
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import joblib
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score



class ModelEvaluator:
    def __init__(self, name, model):
        self.name = name
        self.model = model

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X, threshold=0.5):
        p = self.model.predict_proba(X)[:, 1]
        y = (p >= threshold).astype(int)
        return y, p

    def metrics(self, y_true, y_pred, y_prob):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return {
            'Model': self.name,
            'Accuracy': accuracy_score(y_true, y_pred),
            'Precision': precision_score(y_true, y_pred),
            'Recall': recall_score(y_true, y_pred),
            'F1': f1_score(y_true, y_pred),
            'ROC_AUC': roc_auc_score(y_true, y_prob),
            'Specificity': tn / (tn + fp)
        }

    def find_best_threshold(self, y_true, proba):
        best = (0, 0.90, 0.89)  #Umbrales mínimos:(t=0.5, f1 0.9, Precisión 0.89)
        for t in np.arange(.1, .95, .01):
            f1 = f1_score(y_true, (proba >= t).astype(int))
            precision = precision_score(y_true, (proba >= t).astype(int))
            if f1 > best[1] and precision > best[2]:
                best = (t, f1, precision)
        if best[0] == 0:
            print(f"No se encotnró mejor valor para el modelo {self.name}, se deja threshold con valor 0.5")
            best = (0.5, 0, 0)
        return best




class PLDEvaluatorModels:
    def __init__(self, datasetPath: str = '../data/resultados_pld.csv',
                 target: str = 'diabetes_target',
                 models_list=None, test_size: float = 0.2, model_path: str = 'models/'):
        if models_list is None:
            models_list = ['LogisticRegression', 'RandomForest']
        self.datasetPath = datasetPath
        self.df = pd.read_csv(self.datasetPath)
        self.target = target
        self.models_list = models_list
        self.test_size = test_size
        self.X = None
        self.y = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}

        self.results_df = pd.DataFrame()
        self.artifacts = {}

        self.result_test_ab = pd.DataFrame()
        self.model_path = model_path

    def preprocess(self):
        print(f"Pre-procesando Dataset: {self.datasetPath}")
        if self.datasetPath is None:
            print(f"Dataset not loaded")
            return

        self.X = self.df.drop(columns=[self.target])
        self.y = self.df[self.target]

        cat = self.X.select_dtypes(include=['object', 'str']).columns.tolist()
        nan = self.X.select_dtypes(exclude=['object', 'str']).columns.tolist()
        num = [c for c in self.X.columns if c not in cat]

        prep = ColumnTransformer([
            ('num', StandardScaler(), num),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat)
        ])
        if self.models_list is not None:
            self.models = {
                'RandomForest': Pipeline(
                    [('prep', prep), ('clf', RandomForestClassifier(n_estimators=300, random_state=42))]),
            }
        print(f"Dividiendo Dataset: total de datos para prueba {self.test_size}%")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                test_size=self.test_size,
                                                                                stratify=self.y, random_state=42)

    def run_models(self):


        results = []
        for name, pipe in self.models.items():
            print(f"Iniciando entrenamiento del modelo {name} - {pipe}")
            ev = ModelEvaluator(name, pipe)
            ev.fit(self.X_train, self.y_train)
            _, prob = ev.predict(self.X_test)

            threshold, best_recall, best_prec = ev.find_best_threshold(self.y_test, prob)
            print(f"Model: {name} Treshold: {threshold}, Best f1 score: {best_recall}, Best Precision: {best_prec}")
            pred, prob = ev.predict(self.X_test, threshold=threshold)

            m = ev.metrics(self.y_test, pred, prob)
            scoring = {
                'accuracy': 'accuracy',  # Las métricas como accuracy no generan division zero
                'prec': make_scorer(precision_score, average='macro', zero_division=0),
                'f1': make_scorer(f1_score, average='macro', zero_division=0),
                'roc_auc': 'roc_auc',
                'recall': make_scorer(recall_score, average='macro', zero_division=0),

            }
            cv = cross_validate(pipe, self.X, self.y, cv=StratifiedKFold(5, shuffle=True, random_state=42),
                                scoring=scoring
                                )

            scores = cross_val_score(pipe, self.X, self.y, cv=StratifiedKFold(5, shuffle=True, random_state=42),
                                     scoring='recall')
            mean_score = np.round(np.mean(scores), 2)
            std_f1 = np.std(scores, ddof=1)
            n = len(scores)
            t_value = stats.t.ppf(1 - 0.025, df=n - 1)
            margin_error = t_value * (std_f1 / np.sqrt(n))
            ci_lower = mean_score - margin_error
            ci_upper = mean_score + margin_error

            m['CV_ROC_AUC_MEAN'] = cv['test_roc_auc'].mean()
            m['CV_ROC_AUC_STD'] = cv['test_roc_auc'].std()
            m['threshold'] = threshold
            m['intervalo_confianza'] = f"({ci_lower:4f}, {ci_upper:4f})"
            m["margin_error"] = margin_error
            m['standard_deviation'] = std_f1

            results.append(m)
            self.artifacts[name] = {'pred': pred, 'prob': prob, 'cv': cv}
            with open(f'{self.model_path}pld_model_{name}.pkl', 'wb') as f:
                joblib.dump(ev.model, f)
                print(f"Model saved at {self.model_path}pld_model_{name}.pkl'")

        self.results_df = pd.DataFrame(results).sort_values('ROC_AUC', ascending=False)
        return self.results_df

path = '../data/archive/resultados.csv'
save_model_path = '../models/'

evaluatorModel = PLDEvaluatorModels(datasetPath=path, target='IS_FRAUD', models_list=['RandomForest'], model_path=save_model_path)
evaluatorModel.preprocess()
evaluatorModel.run_models()