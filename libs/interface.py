import os
import json
from nirad import Nirad
from libs.logger import NiradLogger
from libs.utils import Utils
from pathlib import Path
from bs4 import BeautifulSoup as bs


Logger = NiradLogger.set_logger()


class Interface(Nirad):
    def __init__(self, session):
        ipaddress = session.get("ipaddress", None)
        username = session.get("username", 'root')
        password = session.get("password", 'NiRaD$123$')
        super().__init__(ipaddress, username, password)
        self.logger = Logger

    def download_files(self):
        self.download_remote_files(Nirad.config_files)

    def parse_downloaded_file(self):
        config_file_list = os.listdir(self.download_dir)
        if 'openvpn' in config_file_list:
            openvpn_dict = Utils.text2dict(os.path.join(self.download_dir, 'openvpn'))
        if 'network' in config_file_list:
            network_dict = Utils.text2dict(os.path.join(self.download_dir, 'network'))
        self.combined_segment = [{'openvpn': openvpn_dict}, {'network': network_dict}]
        # self.combined_segment = network_dict
        # print(self.combined_segment)
        # Utils.write_file('config.json', self.combined_segment, is_json=True)
        return self.combined_segment

    def download_and_parse_files(self):
        self.download_files()
        data = self.parse_downloaded_file()
        return data

    def get_hw_details(self):
        output = self.send_command('lshw -short')
        output_list = output.splitlines()
        return output_list