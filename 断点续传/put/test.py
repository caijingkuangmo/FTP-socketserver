REQUEST_CODE = {
    '1001': 'cmd info',
    '1002': 'cmd ack',
    '2001': 'post info',
    '2002': 'ACK（可以开始上传）',
    '2003': '文件已经存在',
    '2004': '续传',
    '2005': '不续传',
    '3001': 'get info',
    '3002': 'get ack',

}

def bar(num=1, sum=100):

    rate = float(num) / float(sum)
    rate_num = int(rate * 100)
    temp = '\r%d %%' % (rate_num, )
    sys.stdout.write(temp)
    sys.stdout.flush()