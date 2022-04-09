from optparse import OptionParser

from pkg_resources import require


def parserOpt():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--forum", dest="forum",
                      help="forum eng name", default="")
    parser.add_option("-l", "--latest", dest="latest",
                      help="是否要最新的文章, 預設為False", default=False)
    parser.add_option("-L", "--limit-post", dest="limit_post",
                      help="限制文章數量, 預設為100, -1為不限制", default=100, type=int)
    (options, args) = parser.parse_args()
    print("[info]options: \n{}".format(options))
    print("==========================================================")
    return options


def commentParserOpt():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-L", "--limit-comment", dest="limit_comment",
                      help="限制每篇留言數量, 預設為100, -1為不限制", default=100, type=int)
    parser.add_option("-p", "--dcard-password", dest="password",
                      help="為了產生爬蟲所需auth，故需登入dcard", type=str)
    parser.add_option("-e", "--dcard-email", dest="email",
                      help="為了產生爬蟲所需auth，故需登入dcard", type=str)
    (options, args) = parser.parse_args()
    required = ['password', 'email']
    for r in required:
        if options.__dict__[r] is None:
            parser.error("參數 %s 是必填的！使用-h查看" % r)
    print("[info]options: \n{}".format(options))
    print("==========================================================")
    return options
