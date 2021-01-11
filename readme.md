使用pycharm运行该项目程序，需要先做以下操作：
1.需要在新增的configuration的Environment variables中加入 LD_LIBRARY_PATH=/usr/local/webots/lib/controller，用分号和前一个变量隔开；
2.在对应项目的Project Structure里，右侧的Add Content Root处添加Webots的对应控制器python接口代码目录，如：（LD_LIBRARY_PATH=）/usr/local/webots/lib/controller；