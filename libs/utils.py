import os
import sys
import json
from collections import OrderedDict
from pythonping import ping


class Utils:

    @staticmethod
    def resource_path(relative_path) -> str:
        application_path = os.path.abspath(".")
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the pyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        # print(application_path)
        return os.path.join(application_path, relative_path)

    @staticmethod
    def check_ping(ipaddr) -> bool:
        # response = os.system("ping -n 1 " + ipaddr)
        response = ping(ipaddr)
        return response.success()

    @staticmethod
    def text2dict(file) -> dict:
        with open(file, 'r', encoding='utf-8') as myfile:
            config = list()
            section_dict = OrderedDict()
            list_of_dicts = list()
            section_header = ''

            for line in myfile:
                single_dict = dict()
                if line.strip() != '':  # checks if line is not empty
                    if line.startswith('config'):
                        section_header = line.strip()
                        continue
                    try:
                        key, val = line.strip().split(" '")
                    except ValueError as V:
                        key = line.strip().split(" '")[0]
                        val = ''
                    single_dict[key] = val.replace("'", '')
                    list_of_dicts.append(single_dict)
                elif section_header:
                    section_dict[section_header] = list_of_dicts
                    config.append(section_dict)
                    section_dict = OrderedDict()
                    list_of_dicts = list()
                    section_header = ''
            else:
                if section_header:
                    section_dict[section_header] = list_of_dicts
                    config.append(section_dict)

        return json.loads(json.dumps(config))

    @staticmethod
    def dict2text(fileObj) -> str:
        myfile = fileObj
        content = ''
        for section in myfile:
            for key, value in section.items():
                section_header = key
                content += section_header + '\n'
                for each in value:
                    content += 5 * ' ' + ''.join(key + f"{' '}" + f"'{str(val)}'" for key, val in each.items()) + '\n'
            content += '\n'
        return content

    @staticmethod
    def read_file(file, is_json=False):
        """
        check if file is not a dir, open it and return it's contents after reading
        :param file:
        :param is_json: default False
        :return:
        """
        output = ''
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                output = f.read()
            if is_json:
                output = json.loads(output, strict=False)
        return output

    @staticmethod
    def write_file(filename, file_content, is_json=False):
        """
        write file content to provided filename:
        param filename: abs path of the file
        param file_content: str or json content
        """
        if is_json:
            with open(filename, 'w', encoding='utf-8') as fw:
                json.dump(file_content, fw, indent=4)
        else:
            with open(filename, 'w', encoding='utf-8') as fw:
                fw.write(file_content)