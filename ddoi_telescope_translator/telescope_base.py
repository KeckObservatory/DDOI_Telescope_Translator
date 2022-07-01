from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIConfigFileException

import configparser

import os


class TelescopeBase(TranslatorModuleFunction):

    @staticmethod
    def _load_config(cfg, args=None):

        if not cfg:
            cfg_path_base = os.path.dirname(os.path.abspath(__file__))
            if not args:
                inst = 'default'
            else:
                inst = args.get('instrument', 'default')
            file_name = f"{inst.lower()}_tel_config.ini"
            cfg = f"{cfg_path_base}/ddoi_configurations/{file_name}"
            print(f"config: {cfg}")

        # return if config object passed
        param_type = type(cfg)
        if param_type == configparser.ConfigParser:
            return cfg
        elif param_type != str:
            raise DDOIConfigFileException(param_type, configparser.ConfigParser)

        config = configparser.ConfigParser()
        config.read(cfg)

        return config
