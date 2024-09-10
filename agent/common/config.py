import yaml
import os

class Config:
    DATABASE_URL = "postgresql://root:root@localhost:5432/firewall"
    POLICY_CHECK_INTERVAL = 5
    CHECK_INTERVAL = 5# Check new processes every 5 seconds
    DATABASE_NAME = 'firewall'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'root'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DEFAULT_CHAIN_POLICY='input_chain'
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        self.config = self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration file: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

# Create a singleton instance of Config
config = Config()
