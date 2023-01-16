# 蘑菇丁-工学云上下班打卡脚本
Hel1antHu5  (上来就偷走的能不能④一④)

## 描述
一个很简单的脚本, 支持上班打卡、下班打卡、Server酱推送消息。

## 运行方式
首先要打开脚本将自己的信息填上，主要是手机号、密码、打卡地点、经&纬度。
### 上班
```
python3 GongXueYunSign.py START
```

### 下班
```
python3 GongXueYunSign.py END
```

## 建议运行方式
首先是建议运行在Linux下，使用crontab定时.
```
28 8 * * 1,2,3,4,5 cd ~/GongXueYun && python3 GongXueYunSign.py START
31 17 * * 1,2,3,4,5 cd ~/GongXueYun && python3 GongXueYunSign.py END
```
这样也就是工作日早上8:28上班打卡，下午5:31下班打卡.

## 随机时间
```
28 8 * * 1,2,3,4,5 cd ~/GongXueYun && python3 GongXueYunSign.py START 1
31 17 * * 1,2,3,4,5 cd ~/GongXueYun && python3 GongXueYunSign.py END 1
```
在动作后面跟上随便一个参数，脚本即在1分钟到10分钟的范围内随机延迟执行签到。

## 借鉴
- [https://github.com/laradocs/moguding-solution](https://github.com/laradocs/moguding-solution)
- [https://github.com/laradocs/php-moguding-sdk](https://github.com/laradocs/php-moguding-sdk)
- [https://github.com/grisse/mogudingRobot](https://github.com/grisse/mogudingRobot)