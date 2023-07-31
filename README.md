# web_print
依靠Python+Windows实现的自助打印  
我家的打印机是fuji xreox cp105b 固然linux上有对应的ppd文件，但是在cups下客户端无驱动仍然不行……手机打印还是拉胯……  
正好我有一台All in One，有个24小时开机的Windows，我想可以通过Python来实现自助打印这一点。  
由于我家内网部分服务对外开放，所以我还写了个登录系统，考虑到基本都是家用，各位自己去MySQL自己添加  
到时候还会有个IPP实现的版本，也会发到上面，这样的话手机可以通过自带服务实现打印。  
安装：
Anaconda环境下一般只要安装pymysql即可，mysql上两个表，一个是user_info，一个是user  
user下两个字段，一个id一个password  
userinfo下两个字段，一个account，一个email  
email字段和password字段的数据都要相互对应，id和account相等即可。  
最后在windows下设置好默认打印机，启动server.py即可  
