# ~*~ coding: utf-8 ~*~

import sys
import os
import requests
import json
import time
import configparser
#from NCC_Jenkins import logger
from Log import get_logger
logger = get_logger("jenkins.log")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'ncc.conf'))
default_username = config.get('ncc','username')
default_api_token = config.get('ncc','api_token')
default_server_url = config.get('ncc','server_url')

print ('default_username is',default_username)

class Jenkins():
    def __init__(self,username=None,api_token=None,server_url=None):
        if username == None:
            self.username = default_username
        else:
            self.username = username

        if api_token == None:
            self.api_token = default_api_token
        else:
            self.api_token = api_token

        if server_url == None:
            self.server_url = default_server_url
        else:
            self.server_url = server_url

        self.pre_url = 'http://{0}:{1}@{2}'.format(self.username, self.api_token, self.server_url)
        crumb_url = self.pre_url + '/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
        crumb_req = requests.get(crumb_url)
        crumb_res = crumb_req.text
        crumb = crumb_res.split(':')[-1].strip()
        logger.info('crumb is {}'.format(crumb))
        self.headers = {'Jenkins-Crumb': crumb, 'Content-Type': 'application/json;UTF-8'}

    def get_now_build_number(self,job_name):
        url = self.pre_url + '/job/{0}/lastBuild/api/json?pretty=true'.format(job_name)
        req = requests.post(url, headers=self.headers, data={})
        res = json.loads(req.text)
        build_number = res['id']
        now_build_number = int(build_number)
        #return [build_number,next_build_number]
        logger.info('now_build_number is {}'.format(now_build_number))
        return now_build_number

    def get_next_build_number(self,job_name):
        url = self.pre_url + '/job/{0}/lastBuild/api/json?pretty=true'.format(job_name)
        req = requests.post(url, headers=self.headers, data={})
        res = json.loads(req.text)
        build_number = res['id']
        next_build_number = int(build_number)+1
        #return [build_number,next_build_number]
        logger.info('next_build_number is {}'.format(next_build_number))
        return next_build_number

    def build_job(self,job_name,parameters=None):
        url = self.pre_url + '/job/{0}/build'.format(job_name)
        req = requests.post(url, headers=self.headers, data={})
        return req.text

    def get_last_build_status(self,name, number):

        try:
            url = self.pre_url + '/job/{0}/{1}/api/json?pretty=true'.format(name,number)
            req = requests.get(url, headers=self.headers)
            result = json.loads(req.text)['building']
            if result == False:
                #print ('{0} 已经构建完毕'.format(name))
                logger.info('{0} 已经构建完毕'.format(name))
            else:
                raise
        except:
            #print ('{0} 上次构建任务还未完成,本次构建任务关闭'.format(name))
            logger.info('{0} 上次构建任务还未完成,本次构建任务关闭'.format(name))
            sys.exit(1)

    def get_build_status(self,name, number):
        while True:
            try:
                url = self.pre_url + '/job/{0}/{1}/api/json?pretty=true'.format(name,number)
                req = requests.get(url, headers=self.headers)
                result = json.loads(req.text)['building']
                if result == False:
                    print ('{0} 已经构建完毕'.format(name))
                    logger.info('{0} 已经构建完毕'.format(name))
                    break
            except:
                #print ('{0} 构建中,请耐心等待'.format(name))
                time.sleep(3)
                pass

    def get_build_console_output(self,job_name, number):
        url = self.pre_url + '/job/{0}/{1}/consoleFull'.format(job_name,number)
        req = requests.post(url, headers=self.headers, data={})
        return req.text

    def get_build_result(self,job_name, number):
        url = self.pre_url + '/job/{0}/lastBuild/api/json?pretty=true'.format(job_name,number)
        req = requests.post(url, headers=self.headers, data={})
        res = json.loads(req.text)['result']
        return res

