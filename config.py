from configparser import ConfigParser
import os

def load_config(filename='database.ini', section='postgresql'):

    parser = ConfigParser()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(current_dir, filename)
    parser.read(filename)

    config = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config
