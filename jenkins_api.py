from jenkins import Jenkins
import os
import sys

JENKINS_URL = sys.argv[0]
JENKINS_NAME = sys.argv[1]
JENKINS_USERNAME = 'zhanghe'
JENINS_TOKEN = 'zhanghe1234'

class JenkinsApi:
    def __init__(self):
        self.url = JENKINS_URL
        self.username = JENKINS_USERNAME
        self.password = JENINS_TOKEN
        self.server = self.connect()

    def connect(self):
        """
        连接jenkins（实例化jenkins）
        :return:
        """
        server = Jenkins(self.url, username=self.username, password=self.password)
        return server

    def get_next_build_number(self, name):
        """
        获取下一次构建号
        :param name: 任务名称(项目名称)
        :return: "int" number
        """
        return self.server.get_job_info(name)['nextBuildNumber']

    def set_next_build_number(self, name, number):
        """
        设置下一次构建号
        :param name: 任务名称(项目名称)
        :return: "int" number
        这个貌似不可用。。。（self.server.set_next_build_number(name=name,number=number)）
        用curl顶一下。。
        """
        nexturl     = "%sjob/%s/nextbuildnumber/submit"%(self.url,name)
        shellexec   = """curl --user "%s:%s" --data "nextBuildNumber=%s" --header "Content-Type: application/x-www-form-urlencoded" %s"""%(self.username,self.password,number,nexturl)
        print(shellexec)
        execstatus  = os.system(shellexec)
        return number


    def build_job(self, name, parameters=None):
        """
        构建任务
        :param name: "str" 任务名称
        :param parameters: "dict" 参数
        :return: "int" queue number
        """
        return self.server.build_job(name=name, parameters=parameters)

    def get_build_console_output(self, name, number):
        """
        获取终端输出结果
        :param name: "str" 任务名称
        :param number: "str" 构建号
        :return: "str" 结果
        """
        return self.server.get_build_console_output(name, int(number))

    def stop_build_job(self, name, number):
        """
        终止一个build的执行
        :param name: "str" "任务名称"
        :param number: "str" "构建号"
        :return:
        """
        return self.server.stop_build(name, int(number))

    def delete_build_job(self, name, number):
        """
        删除一个build的执行
        :param name: "str" "任务名称"
        :param number: "str" "构建号"
        :return:
        """
        return self.server.delete_build(name, int(number))

    def get_build_info_result(self,name,number):
        """
        查看某个job的构建是否成功
        :param name:  "str" "任务名称"
        :param number: "str" "构建号"
        :return:
        """
        return self.server.get_build_info(name,int(number))['result']

    def get_build_info_building(self, name, number):
        """
        查看某个job的构建状态
        :param name:  "str" "任务名称"
        :param number: "str" "构建号"
        :return:
        """
        return self.server.get_build_info(name,int(number))['building']

    def get_queue_info(self):
        """
        获取未执行的队列
        :return:
        """
        return self.server.get_queue_info()

    def cancel_queue(self, number):
        """
        取消队列中的一个构建
        (1, '执行中'),
        :param number: "str" "构建号，注意，这个是返回的构建号"
        :return:
        """
        return self.server.cancel_queue(int(number))

jen = JenkinsApi()
jen_result = jen.get_build_console_output(JENKINS_NAME,12)
print (jen_result)
