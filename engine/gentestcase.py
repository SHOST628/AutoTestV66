import unittest
from common.oracle import Oracle
from common.logger import logger
from config import readconfig
from engine.demotestcase import DemoTestCase
from pages.keywords.actionkeyword import Action


# TODO: add function to check which case can exectute or can not execute and add to report

def generate_testcases(testcaseid_list):
    if testcaseid_list == []:
        logger.info("找不到基础用例信息")
        return None
    oracle = Oracle(readconfig.db_url)
    logger.info("<开始生成基础测试用例>")
    for tl in testcaseid_list:
        caseid = tl['XF_CASEID']
        #  notice  the order of step execution
        sql = "select * from xf_testcase where xf_caseid='%s' order by xf_tsid" % caseid
        loop_kwlist = oracle.dict_fetchall(sql)
        if loop_kwlist:
            ifmix = loop_kwlist[0]['XF_IFMIX']  # it will not execute the case if ifmix larger than 0
            if ifmix:
                logger.info("测试用例 %s 不能单独执行" % caseid)
            else:
                func = DemoTestCase.group(loop_kwlist)
                method_name = "test_" + caseid
                setattr(DemoTestCase, method_name, func)
                logger.info("已生成用例 %s" % method_name)
                Action.set_case_info(method_name, loop_kwlist[0]["XF_CASEDESC"], DemoTestCase)
        else:
            logger.info("找不到该用例id %s，无法生成用例 test_%s" % (caseid, caseid))
    logger.info("<基础测试用例生成结束>")

    oracle.close()

# TODO:NOTICE
# bug: it can  still generate mix testcase if has a true caseid although contains false caseid
# no checking : you don't know a true caseid
# add checking : case fails if a false caseid
def generate_mix_testcase(mixcase_list):
    if not mixcase_list:
        logger.info("没有需要组合的用例")
        return None
    oracle = Oracle(readconfig.db_url)
    logger.info("<开始生成组合测试用例>")
    for sl in mixcase_list:
        mixid = sl['XF_MIXID']
        caseid_list = sl['XF_CASEID'].split(',')
        caseid_str = ','.join(caseid_list)
        caseids = str(tuple(caseid_list))
        if len(caseid_list) == 1:
            caseids = caseids.replace(',', '')
        # order by caseid,tsid
        sql = "select * from xf_testcase where xf_caseid in %s " \
              "order by instr('%s',rtrim(cast(xf_caseid as nchar))),xf_tsid" % (caseids, caseid_str)
        loop_kwlist = oracle.dict_fetchall(sql)
        if loop_kwlist:
            func = DemoTestCase.group(loop_kwlist)
            method_name = "test_" + mixid
            setattr(DemoTestCase, method_name, func)
            logger.info("已生成组合用例 %s ,包含基础用例id %s" % (method_name, caseid_list))
            Action.set_case_info(method_name, loop_kwlist[0]["XF_CASEDESC"], DemoTestCase)
        else:
            logger.info("基础用例id %s 错误,无法生成组合用例 test_%s " % (caseid_list, mixid))

    logger.info("<组合测试用例生成结束>")
    oracle.close()


# todo notice
# another method to generate testsuite is that finds test method name containing character test
# by dir method,but order by method name
def generate_testsuite(testcaseid_list, mixid_list):
    if testcaseid_list == [] and mixid_list == []:
        return None
    caseid_list = []
    logger.info("<开始加载测试用例>")
    for tl in testcaseid_list:
        caseid = tl['XF_CASEID']
        test_method_id = 'test_' + caseid
        if hasattr(DemoTestCase, test_method_id):
            caseid_list.append(test_method_id)
        else:
            logger.info("无法加载基础测试用例id %s " % caseid)
    logger.info("已加载基础测试用例 %s" % caseid_list)
    for tl in mixid_list:
        mixid = tl['XF_MIXID']
        test_method_id = 'test_' + mixid
        if hasattr(DemoTestCase, test_method_id):
            caseid_list.append(test_method_id)
        else:
            logger.info("组合用例id %s 没有基础用例信息，无法加载" % mixid)
    logger.info("已加载全部测试用例 %s" % caseid_list)
    logger.info("<测试用例加载结束>")
    logger.debug("<开始组合测试套件>")
    suite = unittest.TestSuite(map(DemoTestCase, caseid_list))
    logger.debug("已组合全部测试套件 %s" % suite)
    logger.debug("<测试套件组合结束>")
    return suite
