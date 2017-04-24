import paramiko
import os.path
class HostConnection:
    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.description = "Connection to a host"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, username=self.username, password=self.password, port=self.port)
        self.transport = self.ssh.get_transport()
        self.session = self.transport.open_session()
        self.session.get_pty()

    def run_command(self, command):
        # self.transport = self.ssh.get_transport()
        if self.ssh.get_transport is not None:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            # stdin.write(r_password +'\n')
            stdin.flush()
            output = stdout.readlines()
            return output
        else:
            print("Not active")

    def put_file(self, sourceFile, destFile):
        # check I can read the file
        canRead = os.path.exists(sourceFile)
        if self.ssh.get_transport is not None:
            if canRead:
                self.sftp = self.ssh.open_sftp()
                self.sftp.put(sourceFile, destFile)

    def get_file(self, sourceFile, destFile):
        # check I can read the file
        canRead = self.run_command("if [ -r " + sourceFile + " ] ;then echo -n yes; else echo -n no; fi")
        if self.ssh.get_transport is not None:
            if "yes" in canRead:
                self.sftp = self.ssh.open_sftp()
                self.sftp.get(sourceFile, destFile)
