# webfetch
带UI界面的网站抓取工具，支持登录验证和推送到指定稿库的功能。

![](https://doc.ngzb.com.cn/server/index.php?s=/api/attachment/visitFile&sign=ff8bd57f233a1f09df1a72f48ceb1b0a)

## 使用说明

**1、 下载**

`
git clone https://github.com/weikion/webfetch.git
`

**2、 安装**

下载源代码，在PyCharm中运行即可。

**3、 配置文件**

配置文件在根目录中，名为：congfig.json，内容和说明如下：

```json
{
    "aes_key" : "xxx", //加密的密钥
    "login_url" : "xxx", //登录的验证地址
    "gaoku_url" : "xxx"  //稿库的API接口
}
```

**4、 登录配置**

默认是不要登录验证的就能使用的，如果需要登录，在配置文件里的输入登录验证地址。

登录时将会POST发送账户和密码到配置的登录验证地址，字段为：

```json
{
  "username": "",
  "password": ""
}
```

要求验证地址返回的数据包为json：

```json
{
    "code" : 0, //返回的代码，0为正确，非0为出错
    "msg" : "", //返回的信息提示
    "username" : "xxx", //用户名
    "expires" : "xxx"  //过期时间
}
```

**5、 推送到稿库**

如果需要推送到稿库，则需要添加稿库的API地址，否则不能推送，推送的数据包为json格式。

数据包例子：

```json
{
    "src_url": "http：//www.xinhua.com", //来源网址
    "title": "xxxxx", //标题
    "content": "xxxxxx", //内容
    "media_name": "新华网" //平台名称
}
```

**6、 仅支持抓取的网站** 

- 新华网
- 南方网
- 央视网
- 中国新闻网
- 人民日报
- 中国蓝新闻
- 求是网
- 现代快报

## 未来开发计划

- 登录验证使用加密模式传输，避免被拦截窃取。
- 使用远程模板维护方式，可支持在线更新抓取的网站模板，更高效，快捷。

## 联系

微信：weikion

qq：43188540