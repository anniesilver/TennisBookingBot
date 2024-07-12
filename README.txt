1. 获得授权码，将其替换到booking.lic文件中
2. 运行exe之前，必须先按自己的账号信息修改b_config.json配置文件并保存

    #你的white oak账号登录的email地址
    "userId": "user@somedomain.com",

    #你的white oak账号登录的密码
    "password": "yourpassword",

    #计划预定星期几就填几，比如，星期三，填3，星期日填7 ，只能填1-7之间的数字！！！
    "book_day": 5,

    #现在不用，不要管
    "book_option": "DAY",

    #预定场地起始时段，比如早上8点，08：00 AM， 下午 6点半，写 06:30 PM， 严格按照格式，不要改动任何其他地方
    "book_slot": "07:00 AM",

     #现在不用，不要管
    "slot_option": "+60",

    #预定场地的partner 球友备选清单， 最好放至少两三个，因为如果第一个人的名额被book满了或者当天已经book过了，程序会自动尝试用下一个人去预定，如果只填一个人就不一定能抢到想要的那块场
    "player_list": ["Wei Zhao","Emma Wang", "Scott Han","Li Liz"]
3. 运行 booking.exe， 查看结果log.txt
4. 在windows中设置定时运行程序 booking.exe, 此处注意一定要在Edit Action的时候，把你的exe所在的目录填入 Start in (Optional) 这一栏， 否则运行结果会写入log.txt无法写入导致程序退出, 预约运行时间之后可以打开log.txt查看相关信息
