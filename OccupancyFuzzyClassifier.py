import pandas as pd
import simpful as sf
from simpful import Gaussian_MF, Triangular_MF, Trapezoidal_MF
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split


class OccupancyFuzzyClassifier:
    def __init__(self, split = False, under_sample_size=600,spread=0.05,function="GAU"):
        # Load and prepare data
        self.function = function
        self._prep_data(under_sample_size=under_sample_size,split = split)
        self._build_fuzzy_system(spread)
        
        



    def _prep_data(self,data_path="data/Occupancy_Estimation.csv",under_sample_size=600,split=False):
        self.df = pd.read_csv(data_path)
        self.target_name = "Room_Occupancy_Count"
        self.df = self.df.drop(columns=["Date", "Time"])
        self.df = self._under_sample(under_sample_size)

        if split:
            X = self.df.drop(columns=[self.target_name])
            y = self.df[self.target_name]
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X,
                y,
                test_size=0.3,
                random_state=42,
                shuffle=True
            )
            self.df = pd.concat([self.X_train, self.y_train], axis=1)


    def _under_sample(self, size):
        target_name = self.target_name
        X = self.df.drop(columns=[target_name])
        y = self.df[target_name]
        rus = RandomUnderSampler(
            sampling_strategy={0: size},
            random_state=42
        )
        X_res, y_res = rus.fit_resample(X, y)
        return pd.concat([X_res, y_res], axis=1)

    def _build_fuzzy_system(self,spread):
        self.data_groups = {}
        self.class_names = sorted(self.df[self.target_name].value_counts().index.tolist())
        for c in self.class_names:
            self.data_groups[c] = self.df[self.df[self.target_name] == c]

        self.feature_names = [col for col in self.df.columns if col != self.target_name]

        self.FS = sf.FuzzySystem(operators=['AND_PRODUCT'],show_banner=False)

        for feature in self.feature_names:
            fuzzy_sets_for_feature = {}
            for c_name in self.class_names:
                avg = self.data_groups[c_name][feature].mean()
                std = max(self.data_groups[c_name][feature].std(), 1e-6)

                sets = 0
                if self.function == "GAU":
                    sets = sf.FuzzySet(
                        function=Gaussian_MF(mu=avg, sigma=std),
                        term=f"{c_name}_{feature}"
                    )
                if self.function == "TRI":
                    sets = sf.FuzzySet(
                        function=sf.Triangular_MF(a=avg-std*3, b=avg, c=avg+std*3),
                        term=f"{c_name}_{feature}"
                    )
                if self.function == "TRA":
                    sets =  sf.FuzzySet(
                        function=sf.Trapezoidal_MF(a=avg-3*std, b=avg-std, c=avg+std, d=avg+3*std),
                        term=f"{c_name}_{feature}"
                    )

                fuzzy_sets_for_feature[c_name]  = sets
            self.FS.add_linguistic_variable(
                feature,
                sf.LinguisticVariable(list(fuzzy_sets_for_feature.values()))
            )

        output_sets = []
        for c_name in self.class_names:
            singleton = sf.FuzzySet(
                points=[[c_name - spread, 0], [c_name, 1], [c_name + spread, 0]],
                term=f"class_{c_name}"
            )
            output_sets.append(singleton)
        self.FS.add_linguistic_variable(
            "occupancy",
            sf.LinguisticVariable(output_sets, universe_of_discourse=[0, 3])
        )

        # Rules (one per class)
        rules = []
        for c_name in self.class_names:
            conds = []
            for feature in self.feature_names:
                conds.append(f"({feature} IS {c_name}_{feature})")
            conds = " AND ".join(conds)
            rule = f"IF ({conds}) THEN (occupancy IS class_{c_name})"
            rules.append(rule)
        self.FS.add_rules(rules)

    def predict(self, X_data):
        preds = []
        for idx, row in X_data.iterrows():
            for feat in self.feature_names:
                self.FS.set_variable(feat, row[feat])
            result = self.FS.Mamdani_inference(['occupancy'])
            preds.append(round(result['occupancy']))
        return preds