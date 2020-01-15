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

cwd_path = os.getcwd()


def join_cwd_path( folder, base_path=None):
    if base_path:
        return os.path.join(base_path, folder)
    else:
        return os.path.join(cwd_path, folder)


class ObjPaths:
    suits = join_cwd_path('suits')
    static = join_cwd_path('static')
    screenshots = join_cwd_path('screenshots', static)
    videos = join_cwd_path('videos', static)
    reports = join_cwd_path('reports', static)
    config = join_cwd_path('config')
    config_file = join_cwd_path(config_file, config)
    dbs = join_cwd_path('dbs', static)
    sqlite3 = join_cwd_path(sqlite3_file, dbs)


