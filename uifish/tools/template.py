from uifish.settings import config_file, case_template_file, sqlite3_file


config_template = """
# 设备ID
device_id: 'xxx'

# mysql DB_URL mysql+pymysql://username:pwd@host/db?charset=utf8mb4 如果是空默认使用本地sqlite3
DB_URL: 
"""

case_template = """
init: 
    video: true,
    device_id: '',
    diff_tag: ''
click: ''
input: ''
drow: ''
check
"""

template_content = {
    config_file: config_template,
    case_template_file: case_template,
    sqlite3_file: 'sql'
}