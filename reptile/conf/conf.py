#! /usr/bin/python
#! coding=utf-8

def get_bank_url():
    return {
        "zgjsyh": {
            "name": "中国建设银行",
            "url":"http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp?jsoncallback=jQuery191042587765765254715_1494841341378",
            "values": {
               "pageNo": 1,
               "pageSize": 100
            },
            "headers": {
               'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            },
            "fields": ("name", "purFloorAmt", "validateDate", "invalidateDate", "investBgnDate", "investEndDate", "investPeriod", "yieldRate")
        },

        "zgzsyh": {
            "name": "中国招商银行",
            "url":"http://www.cmbchina.com/cfweb/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=&currency=&term=&keyword=&series=01&risk=&city=&date=&pagesize=1500&orderby=ord1&t=0.18208376006731108",
            "values": None,
            "headers": {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            },
            "fields": (
                "PrdCode", "PrdName", "NetValue", "IsNewFlag", "Style", "InitMoney", "IncresingMoney", "Risk", "FinDate"
            ),
            "url2": "http://www.cmbchina.com/cfweb/Personal/Default.aspx"
        },

        "zgmsyh": {
            "name": "中国民生银行",
            "url":"https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp?rd=0.3198463827041087&page=1&rows=150&jsonpcallback=jQuery17103298055748152533_1494916604228&_=1494916604416",
            "values": None,
            "headers": {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            },
            "fields": (
                "prd_code", "prd_name", "face_value", "start_date", "end_date", "prd_scale", "pfirst_amt", "prd_next_date", "next_income_rate", "live_time", "opdate", "eddate"
            ),
            "url2": "http://www.cmbc.com.cn/cs/Satellite?c=Page&cid=1356495590851&currentId=1356495507925&pagename=cmbc%2FPage%2FTP_PersonalProductSelLayOut&rendermode=preview"
        },

        "zgnyyh": {
            "name": "中国农业银行",
            "url":"http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=150&o=0&w=%25E5%258F%25AF%25E5%2594%25AE%257C%257C%257C%257C%257C%257C%257C1%257C%257C0%257C%257C0",
            "values": None,
            "headers": {},
            "fields": (
                "ProdArea", "ProdClass", "ProdLimit", "ProdName", "ProdProfit", "ProdSaleDate", "ProdYildType", "ProductNo", "PurStarAmo"
            ),
            "url2": "http://ewealth.abchina.com/fs/filter/"
        }
    }