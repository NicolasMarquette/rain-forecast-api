from enum import Enum


class MlModels(str, Enum):
    """List of the models of machine learning."""
    gbc = "gbc"
    knn = "knn"
    dtc = "dtc"
    lr = "lr"
    gnb = "gnb"
    