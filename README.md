<div align="center" id="top"> 
  <img width="30%" src="/images/spider-robot.png" alt="crawler" />
</div>

<h1 align="center">Dcard Crawler Using Wright</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/Xinbow99/dcard_crawler_based_on_playwright">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/Xinbow99/dcard_crawler_based_on_playwright">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/Xinbow99/dcard_crawler_based_on_playwright">

  <img alt="License" src="https://img.shields.io/github/license/Xinbow99/dcard_crawler_based_on_playwright">
</p>

<br>

## :rocket: Technologies ##

The following tools were used in this project:

- [Playwright](https://playwright.dev/python/docs/intro#installation)
- [Python](https://www.python.org)
- [Mysql](https://hub.docker.com/_/mysql)
- [Docker](https://www.docker.com)
## :checkered_flag: Starting ##

```bash
# Clone this project
$ https://github.com/XinBow99/dcard_crawler_based_on_playwright.git

# Access
$ cd dcard_crawler_based_on_playwright

# Install requirements, if you don't have conda, you can use pip
$ pip install -r requirements.txt
# or you want to use conda
$ conda create env -f environment.yaml
# before you run the code, you need to install the dependencies
# the command means downlaod the chrominum, firefox, webkit, ffmpeg, and some playwright requirements, you can read the document of playwright to get more information.
$ playwright install

# Run the project
$ bash script/crawler_all.sh 
$ bash script/update_comment.sh
```
## How to use ##
### To crawl all the posts, you can run the following command:

```bash
$ python crawler_dcard.py -f relationship -l false -L 100
```
Figure 1: The output of the command above.
<img width="30%" src="/images/figure1.png" alt="f1" />

### The following parameters are available:
* To get post information, you can use the following command:
  * `python crawler_dcard.py -f <forum_english_name> -l <get_latest_post> -L <limit_of_crawl_posts>`
  * `-f`: forum name, if you want to crawl all the posts, you dont need to specify this parameter
  * `-l`: get latest post, if you want to crawl Dcard default hot posts, you dont need to specify this parameter. default is `false`, change to `true` if you want to crawl latest posts.
  * `-L`:limit of crawl posts. type -1 to get all the posts. default is `100`, means you can crawl 100 posts at most.

### Next step is to crawl the comments of the posts.

```bash
python update_dcard_comment.py -L -1 -e "your_dcard_login_email" -p "your_dcard_login_password" -L "limit_of_crawl_comments"
```
Figure 2 and 3: The output of the command above.
<img width="30%" src="/images/figure2.png" alt="f2" />
<img width="30%" src="/images/figure3.png" alt="f3" />
### The following parameters are available:
* To get post information, you can use the following command:
  * `python update_dcard_comment.py -L -1 -e "your_dcard_login_email" -p "your_dcard_login_password" -L "limit_of_crawl_comments"`
  * -L: limit of crawl comments. type -1 to get all the comments. default is `100`, means you can crawl 100 comments under a post at most. 
  * -e: your dcard login email
  * -p: your dcard login password
    * Be sure to use the same email and password you used to login Dcard. Otherwise, the crawler will not working well and you will get an error when try to crawl the comments, like `Oh no! 500 The server is not responding. Please try again later.`
## Some tips ##
### For Ubuntu no desktop environment, you can use the following command to run the project:
##### If you get some error about can't not found the Screen or Display, when you run the command on `Ubuntu server no desktop version`, you can use the following command to fix it:
```bash
$ bash script/ubuntu_no_desktop_verison.sh
```
##### and make sure you have installed the following packages:
```bash
playwright install
playwright install-deps
```


## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE) file.


Made with :heart: by <a href="https://github.com/Xinbow99" target="_blank">Xinbow99</a>

&#xa0;

<a href="#top">Back to top</a>
