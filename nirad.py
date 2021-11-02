import os
import sys
import paramiko
from scp import SCPClient
import time
from libs.utils import Utils
from libs.logger import NiradLogger


Logger = NiradLogger.set_logger()
Script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(Script_dir)


class Nirad:

    port = 22
    config_files = [
                '/etc/config/network', 
                '/etc/config/openvpn',
                '/etc/sysctl.conf', 
                ]

    def __init__(self, ipaddr, username, password ):
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connections = list()
        self.scp = ''
        self.download_dir = ''
        self.logger = Logger
        
        NiradLogger.get_logger(self.ipaddr)
        try:
            self.logger.info("Checking Device Reachability")
            pingstatus = Utils.check_ping(self.ipaddr)
            if pingstatus:
                self.logger.info("Device is reachable")
            else:
                self.logger.error(f"Ping Test to {self.ipaddr} Failed, Device not reachable.")
                sys.exit()
            self.logger.info("Trying to connect to Device using default username and password")
            self.ssh.connect(self.ipaddr, Nirad.port, self.username, self.password, look_for_keys=False, allow_agent=False)
            self.connections.append(self.ssh)
        except Exception as E:
            self.logger.error(f"Unable to login to device, kindly check the credentials -> {E}")
            sys.exit()
        # return self

    def send_command(self, command):
        try:
            command = command.strip('\n').strip()
            for conn in self.connections:
                ssh_stdin, ssh_stdout, ssh_stderr = conn.exec_command(command)
            ssh_stdout = "".join(ssh_stdout.readlines())
            #print(ssh_stdout)
            return ssh_stdout
        except:
            self.logger.error("Unable to execute commands")

    def rename_remote_files(self):
        try:
            self.logger.info("Creating backup of existing files")
            self.ssh.exec_command("mv /etc/config/network /etc/config/network.bkup")
            self.logger.info("Network File Backup:-> Successful")
            self.ssh.exec_command("mv /etc/config/openvpn /etc/config/openvpn.bkup")
            self.logger.info("OpenVPN File Backup:-> Successful")
            self.ssh.exec_command("mv /etc/sysctl.conf /etc/sysctl.conf.bkup")
            self.logger.info("Sysctl.conf File Backup:-> Successful")
            self.ssh.exec_command("mv /lib/modules/4.14.176/dnp_nf.ko /lib/modules/4.14.176/dnp_nf.ko.bkup")
            self.logger.info("dnp_nf_ko File Renaming:-> Successful")
        except Exception as e:
            self.logger.error(f"Exception -> {e}")

    def edit_file(self, filename):
        """
        * following updates needs to be done
        # option tun_mtu '9000'
        # option nice '-20'
        # option txqueuelen '60000'
        # option sndbuf '32000000'
        # option rcvbuf '32000000'
        # option auth 'SHA256'
        """
        file_path = os.path.join(self.logger.report_dir, 'bkup', filename)
        self.logger.info(f"Initializing {filename} file editing")
        with open(file_path, 'r') as myfile:
            data = myfile.read().splitlines()
        new_data = data
        new_data = ["     option tun_mtu '9000'" if line.lstrip().startswith('option tun_mtu') else line for line in new_data]
        new_data = ["     option nice '-20'" if line.lstrip().startswith('option nice') else line for line in new_data]
        new_data = ["     option txqueuelen '60000'" if line.lstrip().startswith('option txqueuelen') else line for line in new_data]
        new_data = ["     option sndbuf '32000000'" if line.lstrip().startswith('option sndbuf') else line for line in new_data]
        new_data = ["     option rcvbuf '32000000'" if line.lstrip().startswith('option rcvbuf') else line for line in new_data]
        new_data = ["     option auth 'SHA256'" if line.lstrip().startswith('option auth') else line for line in new_data]

        file_path = os.path.join('config_files', 'openvpn')
        with open(Utils.resource_path(file_path), 'w') as update_file:
            for line in new_data:
                update_file.write(line + '\n')
        self.logger.info(f"{filename} file editing complete")

    def download_remote_files(self, config_files: list, remote_dir=None):
        """
        # Downloading files from remote machine to local machine
        """
        for file_path in config_files:
            self.logger.info(f"Initiating {file_path.split('/')[-1]} file download")
            self.scp = SCPClient(self.ssh.get_transport())
            self.download_dir = os.path.join(self.logger.report_dir, 'bkup')
            if not os.path.exists(self.download_dir):
                os.mkdir(self.download_dir)
            if remote_dir:
                self.scp.get(remote_dir + file_path, self.download_dir)
            else:
                self.scp.get(file_path, self.download_dir)

            # if 'openvpn' in file_path:
            #     self.edit_file(file_path)
            self.scp.close()

    def upload_file(self, filename, remote_dir=None):
        self.logger.info(f"Starting {filename} file Upload to Remote Device")
        self.scp = SCPClient(self.ssh.get_transport())
        file_path = os.path.join('config_files', filename)
        resource_path = Utils.resource_path(file_path)
        if remote_dir:
            self.scp.put(resource_path, remote_dir + filename)
            self.logger.info(f"{filename} file upload Successful")
        else:
            self.scp.put(resource_path, '/etc/config/' + filename)
            self.logger.info(f"{filename} file upload Successful")

    def restart_service(self):
        try:
            self.logger.info("Restarting Network Services")
            self.ssh.exec_command("/etc/init.d/network restart")
            self.logger.info("Restarting VPN Services")
            self.ssh.exec_command("/etc/init.d/openvpn stop")
            self.ssh.exec_command("/etc/init.d/openvpn start")
        except Exception as e:
            self.logger.info(f"Error in restarting the service -> {e}")

    def data_dump(self):
        self.logger.info("Dumping Internet Status")
        # command = "netstat -napt"
        command = "netstat -napt | grep openvpn | grep EST"
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
        time.sleep(1)
        ssh_stdout = "".join(ssh_stdout.readlines())
        time.sleep(2)
        self.logger.info(f"Flow Details -> \n{ssh_stdout}")


if __name__ == '__main__':

    ipaddress = input("Enter IP address of Nirad device: ")
    username = "root"
    password = "NiRaD$123$"
    # ipaddress = '192.168.10.120'
    # username = 'root'
    # password = 'root'

    try:
        config_files = Nirad.config_files
        myObj = Nirad(ipaddress, username, password)  
        myObj.download_remote_files(config_files=config_files)
        
        # myObj.rename_remote_files()
        # for file_path in config_files:
        #     if file == 'sysctl.conf':
        #         myObj.upload_file(file, remote_dir='/etc/')
        #     else:
        #         myObj.upload_file(file)
        # myObj.restart_service()
        # myObj.data_dump()
    except Exception as e:
        print(f"Error Encountered ->:{e}")
    finally:
        finish = input("Press Enter to Exit...")

