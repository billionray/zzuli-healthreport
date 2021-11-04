def header_generate(finaldakaurl, cookies):
    # 替换cookie中可能出现的%3D为等号
    xsrf_token = cookies.get("XSRF-TOKEN", )
    xsrf_token = xsrf_token.replace('%3D', '=')
    get_headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "DNT": "1",
        "X-XSRF-TOKEN": xsrf_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": ("%s" % finaldakaurl),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=" + cookies["PHPSESSID"] + ";XSRF-TOKEN=" + cookies[
            "XSRF-TOKEN"] + ";" + "laravel_session=" + cookies["laravel_session"]
    }

    headers = {
        "Connection": "keep-alive",
        "X-XSRF-TOKEN": xsrf_token,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://msg.zzuli.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": ("%s" % finaldakaurl),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "PHPSESSID=" + cookies["PHPSESSID"] + ";XSRF-TOKEN=" + cookies[
            "XSRF-TOKEN"] + ";" + "laravel_session=" + cookies["laravel_session"]
    }

    return [get_headers, headers]
