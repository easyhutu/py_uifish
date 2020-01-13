import os


sqlite3_file = 'uifish.db'
config_file = 'config.yml'
case_template_file = 'uifish_eg.yml'

object_folders = {
    'suits': None,
    'static': {
        'screenshots': None,
        'videos': None,
        'reports': None,
    }
}

object_files = {
    'static': {
        'dbs': sqlite3_file
    },
    'config': {
        config_file: None
    },
    'suits': case_template_file

}

video_file_format = '{idx}_{timestamp}_{tag}'
screenshots_file_format = '{idx}_{timestamp}_{tag}'
reports_file_format = '{idx}_{timestamp}_{tag}.html'

