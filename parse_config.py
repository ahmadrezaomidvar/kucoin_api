import yaml
from pathlib import Path

class Config:
    def __init__(self, config_path):
        '''
        module to parse the config file
        '''

        self.config_path = config_path
        self.config = self.read_yaml()


    def read_yaml(self):

        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)


# if __name__ == '__main__':
#     config_path = str(Path(__file__).resolve().parents[0].joinpath('configs', 'config.yaml'))
#     config = Config(config_path=config_path)
#     print(config.config)

# TODO: