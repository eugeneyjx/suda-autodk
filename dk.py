# encoding=utf-8

from selenium import webdriver
import time
import json

# 开启浏览器
def openChrome():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=option)
    return driver

def find(driver,str):
    try:
        driver.find_element_by_xpath(str)
    except:
        return False
    else:
        return True

# 流程
def operate_dk(driver):
    # 打开配置文件
    try:
        with open("config.json",encoding='utf-8') as f:
            config=json.load(f)
    except:
        print("配置文件错误！请检查配置文件是否与py文件放置于同一目录下，或配置文件是否出错！\n请注意'现人员位置'只可填入以下四项中的任意一项：'留校', '在苏州', '江苏省内其他地区', '在其他地区'")
        return -1
    else:
        url = "http://ids1.suda.edu.cn/amserver/UI/Login?goto=http%3a%2f%2fmyauth.suda.edu.cn%2fdefault.aspx%3fapp%3dsswsswzx2%26jumpto%3d&welcome=%e5%b8%88%e7%94%9f%e7%bd%91%e4%b8%8a%e4%ba%8b%e5%8a%a1%e4%b8%ad%e5%bf%83&linkName=%e5%a6%82%e6%9e%9c%e6%97%a0%e6%b3%95%e4%bd%bf%e7%94%a8%e7%bb%9f%e4%b8%80%e8%ba%ab%e4%bb%bd%e7%99%bb%e5%bd%95%ef%bc%8c%e8%af%b7%e7%82%b9%e5%87%bb%e8%bf%99%e9%87%8c&linkUrl=http://aff.suda.edu.cn/_web/ucenter/login.jsp&gx_charset=UTF-8"
        driver.get(url)
        # 找到输入框并输入查询内容
        elem = driver.find_element_by_id("IDToken1")
        elem.send_keys(config["学号"])
        elem = driver.find_element_by_id("IDToken9")
        elem.send_keys(config["密码"])
        # 提交表单
        driver.find_element_by_xpath("//*[@id='loginBtn']").click()
        try:
            driver.find_element_by_xpath("//*[text()='首页']")
        except:
            print('登陆失败！请检查学号密码是否正确')
            return -1
        else:
            print('登录成功！')
            url = "http://aff.suda.edu.cn/_web/fusionportal/detail.jsp?_p=YXM9MSZwPTEmbT1OJg__&id=2749&entranceUrl=http%3A%2F%2Fdk.suda.edu.cn%2Fdefault%2Fwork%2Fsuda%2Fjkxxtb%2Fjkxxcj.jsp&appKey=com.sudytech.suda.xxhjsyglzx.jkxxcj."
            driver.get(url)
            driver.find_element_by_xpath("//*[@class='action-btn action-do']").click()

            # 切换到小框内
            iframe1=driver.find_element_by_id("layui-layer-iframe1")
            driver.switch_to.frame(iframe1)
            flag=False
            while(flag==False):
                time.sleep(1)
                flag=find(driver, "//*[text()='"+config["学号"]+"']")

            elem = driver.find_element_by_id("input_swtw")
            elem.send_keys("36.8")
            elem = driver.find_element_by_id("input_xwtw")
            elem.send_keys("36.8")
            driver.find_element_by_xpath("//*[@id='checkbox_jkzk33']").click()
            xrywz={'留校':'radio_xrywz5','在苏州':'radio_xrywz7','江苏省内其他地区':'radio_xrywz9','在其他地区':'radio_xrywz23'}
            driver.find_element_by_xpath("//*[@id='"+xrywz[config["现人员位置"]]+"']").click()
            elem = driver.find_element_by_id("input_jtdz")
            elem.send_keys(config["家庭地址"])
            driver.find_element_by_xpath("//*[@id='radio_sfyxglz27']").click()

            # 提交
            driver.find_element_by_xpath("//*[@id='tpost']").click()
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//*[text()='提交成功！']")
                print('打卡成功！')
            except:
                try:
                    driver.find_element_by_xpath("//*[text()='当天已经提交过，是否继续提交？']")
                    print("已打卡过！")
                    driver.find_element_by_xpath("//a[@class='layui-layer-btn0']").click()
                except:
                    print("打卡失败！请重新开始")
            driver.find_element_by_xpath("//a[@class='layui-layer-btn0']").click()
            time.sleep(3)
            print("即将退出程序...")
            driver.quit()

# 主函数
if __name__ == '__main__':
    print("这是一个自动健康打卡的程序。\n\n请在同目录下的config.json中配置打卡信息，例如：\n'学号': '1827405055',\n'密码': '12345678',\n'现人员位置': '在苏州',      (请注意只可填入以下四项中的任意一项：'留校', '在苏州', '江苏省内其他地区', '在其他地区')\n'家庭地址': '工业园区'\n其余所有属性均为打卡系统自动填充的上一次打卡信息\n\n程序即将启动...")
    driver = openChrome()
    operate_dk(driver)