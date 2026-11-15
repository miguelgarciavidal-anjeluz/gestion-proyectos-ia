from Fraudes import ModeloFraudes, MonitorModel

if __name__ == '__main__':

    try:
        model = ModeloFraudes(path_dataset="data/fraudes.csv", test_size=0.2, target="IS_FRAUD", name="Exp1 - Base")
        model.train()
        monitor = MonitorModel(model)
        monitor.execute_monitoring("Exp1 - Base")
    except Exception as e:
        print(e)
    try:
        model = ModeloFraudes(path_dataset="data/fraudes.csv", test_size=0.2, target="IS_FRAUD", name="Exp2 - Latencia")
        model.train()
        monitor = MonitorModel(model)
        monitor.execute_monitoring(monitor_name="Exp2 - Latencia", simulate_time_out=True, degrada=False)
    except Exception as e:
        print(e)
    try:
        model = ModeloFraudes(path_dataset="data/fraudes.csv", test_size=0.2, target="IS_FRAUD", name="Exp3 - DataDrift")
        model.train()
        model.train()
        monitor = MonitorModel(model)
        monitor.execute_monitoring(monitor_name="Exp3 - DataDrift", degrada=True, normal_degradado_simulation=0.95)
    except Exception as e:
        print(e)
    try:
        model = ModeloFraudes(path_dataset="data/fraudes.csv", test_size=0.2, target="IS_FRAUD", name="Exp4 - Umbral")
        model.train()
        monitor = MonitorModel(model)
        monitor.execute_monitoring("Exp4 - Umbral", umbral=0.5)
    except Exception as e:
        print(e)
