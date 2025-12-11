import os
import yaml
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    model_path: str
    preprocessor_path: str


@dataclass
class DataConfig:
    raw_data_path: str
    train_data_path: str
    test_data_path: str
    raw_data_output_path: str


@dataclass
class TrainingConfig:
    test_size: float
    random_state: int
    target_column: str


@dataclass
class AppConfig:
    host: str
    port: int
    debug: bool


@dataclass
class LoggingConfig:
    log_dir: str
    log_format: str
    log_level: str


class Config:
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        
        self.model = ModelConfig(**config_dict['model'])
        self.data = DataConfig(**config_dict['data'])
        self.training = TrainingConfig(**config_dict['training'])
        self.app = AppConfig(**config_dict['app'])
        self.logging = LoggingConfig(**config_dict['logging'])

