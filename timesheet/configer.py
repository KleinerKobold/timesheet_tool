import yaml
from pathlib import Path 
import os


def get_config(config_file=None):
    homedir = Path.home()
    timesheet_dir = homedir / ".timesheet"
    if config_file is None:
        config_file = timesheet_dir / 'config.yaml'
    try:
        config = dict()
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config
    except:
        if not timesheet_dir.exists():
            timesheet_dir.mkdir()
        data = dict()
        yaml.safe_dump(data)
        if not os.path.isfile(config_file):
            with open(config_file, 'w') as outfile:
                yaml.safe_dump(data, outfile, default_flow_style=False)
                print(f"Keine config vorhanden, config wurde neu erstellt in {config_file}\n BITTE ANPASSEN")
        pass

