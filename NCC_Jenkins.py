# ~*~ coding: utf-8 ~*~
import re
import os
import time
import importlib,sys
importlib.reload(sys)

from JenkinsClass import Jenkins
from mailers import SendMessages
from NCC_Mailers import NCC_Mailers
#from Log import get_logger
#logger = get_logger("jenkins.log")
from JenkinsClass import logger

jen = Jenkins()

def BuildJob(job_name):

    #get last job number
    last_num = jen.get_now_build_number(job_name)
    #get last job status and parser
    jen.get_last_build_status(job_name,last_num)

    num = jen.get_next_build_number(job_name)
    #start build job
    jen.build_job(job_name)
    #get build job status
    jen.get_build_status(job_name,num)
    #get buld job print
    res = jen.get_build_result(job_name,num)
    if res == 'SUCCESS':
        logger.info('{} 构建成功'.format(job_name))
    else:
        error = jen.get_build_console_output(job_name,num)
        error_list = error.split('\n')
        email_msg = []

        for e in error_list:
            if e.find('错误') != -1:
                email_msg.append(e)
                logger.info(e)
        #NCC_Mailers = ['haochx@yonyou.com']
        SendMessages(NCC_Mailers, email_msg, job_name)


BuildJob('2012-test-ncc-hcx')
