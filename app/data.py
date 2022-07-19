import json

import requests


def data_generate(get_user_url, headers, cookies, proxies, debug, report_type, data, datetime):
    # 从服务器获得部分数据
    source_data = requests.get(get_user_url, headers=headers[0], cookies=cookies, proxies=proxies)
    source_data.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    source_data = source_data.text
    user_dict = json.loads(source_data)
    if debug == 1:
        print(f"从服务器获取的数据：\n{user_dict}")

    mobile = data[0]
    homemobile = data[1]
    gpslocation = data[2]
    lat = data[3]
    lon = data[4]
    region = data[5]
    area = data[6]
    build = data[7]
    dorm = data[8]
    schoolgps = data[9]
    schoollat = data[10]
    schoollon = data[11]
    vaccine = data[12]
    nucleicacidtest = data[13]
    lasttest = data[14]
    novaccine_reason=data[15]
    novaccine_detail=data[16]

    home_data = {
        "user_code": user_dict.get("user_code", ),
        "user_name": user_dict.get("user_name", ),
        "id_card": user_dict.get("id_card", ),
        "date": datetime,
        "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ),
        "org": user_dict.get("org", ),
        "year": user_dict.get("year", ),
        "spec": user_dict.get("spec", ),
        "class": user_dict.get("class", ),
        "region": "",
        "area": "",
        "build": "",
        "dorm": "",
        "mobile": mobile,
        "jt_mobile": homemobile,
        "province": user_dict.get("province", ),
        "city": user_dict.get("city", ),
        "district": user_dict.get("district", ),
        "address": user_dict.get("address", ),
        "hjdz": user_dict.get("hjdz", ),
        "hj_province": user_dict.get("hj_province", ),
        "hj_city": user_dict.get("hj_city", ),
        "hj_district": user_dict.get("hj_district", ),
        "out": "否",
        "out_address": "[{\"start_date\":\"\",\"end_date\":\"\",\"province\":\"\",\"city\":\"\",\"district\":\"\",\"area\":\"\",\"address\":\"\"}]",
        "hb": "否",
        "hb_area": "",
        "hn": "否",
        "hn_area": "",
        "lat": lat,
        "lon": lon,
        "gcj_lat": lat,
        "gcj_lon": lon,
        "jz_address": gpslocation,
        "jz_province": user_dict.get("province", ),
        "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ),
        "jz_sfyz": "是",
        "sj_province": "",
        "sj_city": "",
        "sj_district": "",
        "temp": "正常",
        "jrzz": "健康",
        "jzqk": "",
        "stzk": "无",
        "jcbl": "否",
        "jcqk": "",
        "yqgl": "否",
        "glrq": "",
        "gljc": "",
        "glp": "",
        "glc": "",
        "gld": "",
        "gla": "",
        "glyy": "",
        "glztlb": "",
        "yjs": 0,
        "other": "无",
        "jjymqk": vaccine,
        "hsjcqk": nucleicacidtest,
        "no_yy":novaccine_reason,
        "no_jtyy":novaccine_detail,
        "last_time": datetime,
        "last_result":"阴性",
        "fxdj": "低风险", "flgl": "正常", "jkmzt": "绿色", "hb_date": "", "jz_qzbl": "",
        "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "",
        "jc_jcrq": "",
        "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "", "qz_yqbl": "否",
        "qz_yqrq": "",
        "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "", "zl_address": "", "zl_sfzy": "",
        "zl_zyrq": "",
        "xq_province": "", "xq_city": "", "xq_district": "", "xq_area": "", "xq_address": "", "home_time": "",
        "wj_type": 0
    }
    morn_data = {
        "user_code": user_dict.get("user_code", ),
        "user_name": user_dict.get("user_name", ),
        "id_card": user_dict.get("id_card", ),
        "date": datetime, "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ),
        "org": user_dict.get("org", ),
        "year": user_dict.get("year", ),
        "spec": user_dict.get("spec", ),
        "class": user_dict.get("class", ),
        "region": region,
        "area": area,
        "build": build,
        "dorm": dorm,
        "mobile": mobile,
        "jt_mobile": homemobile,
        "province": user_dict.get("province", ),
        "city": user_dict.get("city", ),
        "district": user_dict.get("district", ),
        "address": user_dict.get("address", ),
        "hjdz": user_dict.get("hjdz", ),
        "hj_province": user_dict.get("hj_province", ),
        "hj_city": user_dict.get("hj_province", ),
        "hj_district": user_dict.get("hj_district", ),
        "out": "", "out_address": "[]", "hb": "", "hb_area": "", "hn": "", "hn_area": "",
        "lat": schoollat, "lon": schoollon,
        "gcj_lat": schoollat, "gcj_lon": schoollon,
        "jz_address": schoolgps,
        "jz_province": user_dict.get("province", ),
        "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ),
        "jz_sfyz": "是",
        "sj_province": "",
        "sj_city": "",
        "sj_district": "",
        "temp": "正常",
        "jrzz": "无", "jzqk": "", "stzk": "无", "jcbl": "", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
        "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "jkmzt": "绿色", "no_jtyy": "", "no_yy": "",
        "jjymqk": vaccine, 
        "hsjcqk": nucleicacidtest, 
        "no_yy":novaccine_reason,
        "no_jtyy":novaccine_detail,
        "last_time": lasttest, 
        "hb_date": "", "jz_qzbl": "",
        "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "",
        "jc_jcrq": "", "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "",
        "qz_yqbl": "否", "qz_yqrq": "", "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "",
        "zl_address": "", "zl_sfzy": "", "zl_zyrq": "", "xq_province": "", "xq_city": "", "xq_district": "",
        "xq_area": "", "xq_address": "", "home_time": "", "wj_type": 1
    }

    dorm_data = {
        "user_code": user_dict.get("user_code", ),
        "user_name": user_dict.get("user_name", ),
        "id_card": user_dict.get("id_card", ),
        "date": datetime, "sex": user_dict.get("sex", ),
        "age": user_dict.get("age", ),
        "org": user_dict.get("org", ),
        "year": user_dict.get("year", ),
        "spec": user_dict.get("spec", ),
        "class": user_dict.get("class", ),
        "region": region,
        "area": area,
        "build": build,
        "dorm": dorm,
        "mobile": mobile,
        "jt_mobile": homemobile,
        "province": user_dict.get("province", ),
        "city": user_dict.get("city", ),
        "district": user_dict.get("district", ),
        "address": user_dict.get("address", ),
        "hjdz": user_dict.get("hjdz", ),
        "hj_province": user_dict.get("hj_province", ),
        "hj_city": user_dict.get("hj_province", ),
        "hj_district": user_dict.get("hj_district", ),
        "out": "", "out_address": "[]", "hb": "", "hb_area": "", "hn": "", "hn_area": "",
        "lat": schoollat, "lon": schoollon,
        "gcj_lat": schoollat, "gcj_lon": schoollon,
        "jz_address": schoolgps,
        "jz_province": user_dict.get("province", ),
        "jz_city": user_dict.get("city", ),
        "jz_district": user_dict.get("district", ),
        "jz_sfyz": "是",
        "sj_province": "",
        "sj_city": "",
        "sj_district": "",
        "temp": "正常",
        "jrzz": "无", "jzqk": "", "stzk": "无", "jcbl": "", "jcqk": "", "yqgl": "否", "glrq": "", "gljc": "", "glp": "",
        "glc": "", "gld": "", "gla": "", "glyy": "", "yjs": 0, "other": "无", "jkmzt": "绿色", "no_jtyy": "", "no_yy": "",
        "jjymqk": vaccine, "hsjcqk": nucleicacidtest, "last_time": lasttest, "hb_date": "", "jz_qzbl": "",
        "tz_qzbl": "",
        "tz_province": "", "tz_city": "", "tz_district": "", "tz_area": "", "tz_address": "", "jc_yqjc": "",
        "jc_jcrq": "", "jc_province": "", "jc_city": "", "jc_district": "", "jc_area": "", "jc_address": "",
        "qz_yqbl": "否", "qz_yqrq": "", "zl_province": "", "zl_city": "", "zl_district": "", "zl_area": "",
        "zl_address": "", "zl_sfzy": "", "zl_zyrq": "", "xq_province": "", "xq_city": "", "xq_district": "",
        "xq_area": "", "xq_address": "", "home_time": "20:00", "wj_type": 3
    }

    # 转换data字典类型为字符串类型并支持中文
    if report_type == "home":
        data_json = json.dumps(home_data, ensure_ascii=False)
    elif report_type == "morn":
        data_json = json.dumps(morn_data, ensure_ascii=False)
    elif report_type == "dorm":
        data_json = json.dumps(dorm_data, ensure_ascii=False)
    return data_json
