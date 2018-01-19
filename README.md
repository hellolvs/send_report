# send_report
用的python2.7，其中相关数据库参数、邮件参数、网址等真实数据都处理掉了，自己注意替换补全。

fetch_results()读库，返回结果，没啥好说的。

screen_shot(event_id)用于网页截屏，event_id用于传递url参数。使用selenium+phantomjs实现，都是python爬虫很典型的工具。注意其中使用Image截取DOM中id为main的元素的操作。截取后保存到本地。

send_mail(results)自然是发邮件，利用了mailer和jinja2模板，其中env = Environment(loader=PackageLoader(‘jinja’, ‘templates’))这一句是jinja2加载模板的代码，模板位于与此py脚本文件同目录的jinja包下templates目录下的mail.html中。可以看下在mail中嵌入图片和作为附件发送的操作。

