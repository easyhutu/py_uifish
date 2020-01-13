import os
from uifish.settings import config_file, case_template_file, sqlite3_file

current_path = os.path.abspath(os.path.dirname(__file__))

to_path = lambda filename: os.path.join(current_path, filename)

template_paths = {
    case_template_file: to_path(case_template_file),
    config_file: to_path(config_file),
    sqlite3_file: to_path(sqlite3_file)
}
