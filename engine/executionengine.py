import sys
import unittest
from config import readconfig
from engine.parsekeyword import ParseKeyword
from common.oracle import Oracle
from driver.driver import browser
from pages.base.keyword import Action
from pages.loginpage import LoginPage
from common.storage import Storage
import re
import os
import time
from common.logger import logger

class DemoTestCase(unittest.TestCase, Action):

    def setUp(self):
        self.driver = browser(readconfig.browser_name)
        self.driver.maximize_window()
        LoginPage(self.driver).login(readconfig.login_user,readconfig.login_password)

    def tearDown(self):
        logger.info('**************************************************结束执行用例**************************************************')
        # self.driver.quit()

    def _use_keyword(self,func_name,opvalues=None):
        func = ParseKeyword(self.driver).parse(func_name)
        if opvalues == "" or opvalues == None:
            func()
        else:
            #  parse a variate from user defining
            var_list = re.findall("\$(.+?)\$",opvalues)
            for var in var_list:
                try:
                    if hasattr(Storage,var):
                        var_value = getattr(Storage,var,"找不到此变量%s"%var)
                        opvalues = re.sub("\$(.+?)\$",var_value,opvalues,count=1)
                except Exception as e:
                    raise e
            opvalist = opvalues.split('##')
            func(*opvalist)

    @staticmethod
    def group(keyword_list):
        def func(self):
            logger.info('**************************************************开始执行用例**************************************************')
            try:
                for key_dict in keyword_list:
                    self._use_keyword(key_dict["XF_ACTION"], key_dict["XF_OPVALUES"])
                    logger.info('执行用例 %s 的 %s %s %s %s 成功'%(key_dict["XF_CASEID"],key_dict["XF_TSID"],key_dict["XF_TSDESC"],key_dict["XF_ACTION"],key_dict["XF_OPVALUES"]))
            except Exception as e:
                logger.error('执行用例 %s 的 %s %s %s %s 出错' % (key_dict["XF_CASEID"], key_dict["XF_TSID"], key_dict["XF_TSDESC"], key_dict["XF_ACTION"],key_dict["XF_OPVALUES"]))
                logger.exception(e)
                raise e
        return func

def _generate_testcases(testcaseid_list):
    if testcaseid_list == []:
        return
    oracle = Oracle(readconfig.db_url)
    loop_kwlist = []

    for tl in testcaseid_list:
        caseid = tl['XF_CASEID']
        #  notice  the order of step execution
        loop_kwlist = oracle.dict_fetchall("select * from xf_testcase where xf_caseid='%s' order by xf_tsid"%caseid)
        func = DemoTestCase.group(loop_kwlist)
        setattr(DemoTestCase, 'test_' + caseid, func)
        loop_kwlist = []

    oracle.close()

#TODO need to fix
def _generate_mix_testcase(mixcase_list):
    if mixcase_list == []:
        return None
    loop_kwlist = []
    oracle = Oracle(readconfig.db_url)
    #  notice the order of testcase execution
    for sl in mixcase_list:
        mixid = sl['XF_MIXID']
        caseid_list = sl['XF_CASEID'].split(',')
        caseid_str = ','.join(caseid_list)
        caseids = str(tuple(caseid_list))
        #order by caseid,tsid
        loop_kwlist = oracle.dict_fetchall("select * from xf_testcase where xf_caseid in %s order by instr('%s',rtrim(cast(xf_caseid as nchar))),xf_tsid"%(caseids,caseid_str))
        func = DemoTestCase.group(loop_kwlist)
        setattr(DemoTestCase, 'test_' + mixid, func)
        loop_kwlist = []
    oracle.close()

def _generate_testsuite(testcaseid_list,mixid_list):
    if testcaseid_list == [] and mixid_list == []:
        return None
    caseid_list = []
    for tl in testcaseid_list:
        caseid = tl['XF_CASEID']
        caseid = 'test_' + caseid
        caseid_list.append(caseid)
    for tl in mixid_list:
        mixid = tl['XF_MIXID']
        mixid = 'test_' + mixid
        caseid_list.append(mixid)
    suite = unittest.TestSuite(map(DemoTestCase, caseid_list))
    return suite

oracle = Oracle(readconfig.db_url)

testcaseid_list = oracle.dict_fetchall("select distinct xf_caseid from xf_testcase")
mixcase_list = oracle.dict_fetchall("select * from xf_mixcase")
mixid_list = oracle.dict_fetchall('select xf_mixid from xf_mixcase')

_generate_testcases(testcaseid_list)
_generate_mix_testcase(mixcase_list)
testsuite = _generate_testsuite(testcaseid_list, mixid_list=[])
if testsuite == None:
     print('please add data to xf_testcase or xf_mixcase')

oracle.close()

if __name__ == "__main__":
    unittest.TextTestRunner().run(testsuite)
    result = unittest.main(verbosity=2)




