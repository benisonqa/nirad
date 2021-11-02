import logging
import os
import platform
import datetime
from libs.utils import Utils


def singleton(cls):
    """
    Used to create a singleton for StigLogger()
    """
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()


@singleton
class NiradLogger:
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self.logging_directory = None
        self.banner = None
        # self.lsb_release = self.get_lsb_release()
        formatter = logging.Formatter('%(asctime)s  %(levelname)-8s | [%(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()
        self.report_dir = "./Reports/NIRAD_SETUP_LOG_" + now.strftime("%d-%m-%Y_%H-%M-%S")

        if not os.path.exists(self.report_dir):
            try:
                access_rights = 0o777
                os.makedirs(self.report_dir, access_rights)
            except OSError as e:
                print("Unable to Create Log Directory {} --> Try running the script in Sudo mode".format(e))
        fileHandler = logging.FileHandler(self.report_dir + "/LOG_" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".log")
        self.logging_file = os.path.join(self.report_dir, fileHandler.baseFilename)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)

        # Logs to be shown on terminal
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)
        self._logger.report_dir = self.report_dir

    # def get_version(self) -> dict:
    #     details = platform.uname()
    #     os_details = dict()
    #     os_details['platform'] = details[0]
    #     os_details['release'] = details[2]
    #     os_details['version'] = details[3]
    #     return os_details
    #
    # def get_lsb_release(self) -> dict:
    #     try:
    #         self._logger.info("Fetching lsb details")
    #         data = Utils.get_lsb()
    #         return data['Description']
    #     except:
    #         self._logger.error("Unable to fetch lsb details")
    #         return None

    def show_banner(self, ipaddr=None):
        # os_details = self.get_version()
        banner = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                                       >>>>>>> STARTING NIRAD SETUP <<<<<<<

>> Remote IP Address..........: {ip}
>> NIRAD APP Version..........: {v}
>> LOG FILE Location............: {d}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''.format(ip=ipaddr, d=self.logging_file, v='4')
        self.banner = banner.encode('ascii', 'ignore').decode('ascii')
        return self.banner

    def get_logger(self, ipaddr=None):
        ''' Intialize logger and show banner '''
        # self._logger.info(self.get_version())   #TODO remove in prod
        self._logger.info(self.show_banner(ipaddr))
        return self._logger

    def set_logger(self):
        ''' Initialize logger '''
        return self._logger