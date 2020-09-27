from time import time, sleep
from multiprocessing import Process, Pool


def get_files_under_path(path, all_files):
    # 获取文件夹下文件路径和文件名的方法 –采用递归的方式
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    import os
    file_list = os.listdir(path)  # 首先遍历当前目录所有文件及文件夹
    for file in file_list:
        cur_path = os.path.join(path, file)
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        if os.path.isdir(cur_path):  # 判断是否是文件夹
            get_files_under_path(cur_path, all_files)
        else:
            all_files.append(file)
    return all_files

# __main__函数应该传入空的list接收文件名
# 比如contents = get_files_under_path("e:\\python", [])


def download_file(file_name, time):
    print('start to download %s...' % file_name)
    sleep(time)
    print('%s Done!' % file_name)

# Way01 Process类创建进程
# target参数表示目标函数，即进程启动后要执行的代码，args参数是目标函数所需要的参数，用一个元组接收。
# Process的start( )方法用于启动进程，而join( )方法表示等待进程执行结束再继续往下运行。


def process_method():
    start = time()
    p1 = Process(target=download_file, args=('test01.pdf', 2))
    p1.start()
    p2 = Process(target=download_file, args=('test02.pdf', 2))
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print("The whole process takes %.2f seconds" % (end-start))

# Way02 Pool进程池的方法
# apply()是同步开启进程，每次只执行一个，不能实现并发
# apply_async,可以实现并发，但使用时要注意join
# 创建结束调用close( )方法，调用此方法后进程池就不能继续添加新的进程了。
# 最后调用join( )方法等待所有子进程执行完毕


def apply_method():
    files = ['test01.pdf', 'test02.pdf', 'test03.pdf', 'test04.pdf']
    need_times = [2, 2, 3, 2]
    start_time = time()
    p = Pool()
    # Pool()不设定数值时，是电脑默认的设定
    # 如果想要同事执行多个进程，可以在Pool()做设定
    for i in range(4):
        p.apply_async(download_file, args=(files[i], need_times[i]))
        # args后面接的必须是元组，如果是只有一个元素的情况下，应该写成 args = (i,) 逗号不可省略
    p.close()
    p.join()
    end_time = time()
    print("The whole process takes %.2f seconds" % (end_time - start_time))

# map
# map() 自带join功能，每次开启的进程数量最好不要大于CPU核数+1
# 第一个参数为要执行的函数，第二个参数要传递可迭代类型数据。如列表、元祖等.
# 多个参数可以封装成字典、元祖、列表等嵌套进可迭代数据类型中：


def map_method():
    files = ['test01.pdf', 'test02.pdf', 'test03.pdf', 'test04.pdf']
    need_times = [2, 2, 3, 2]
    start_time = time()
    p = Pool(5)
    p.map(download_file, files, need_times)
    p.close()
    p.join()
    end_time = time()
    print("The whole process takes %.2f seconds" % (end_time - start_time))

# 进程间的返回值问题
# 关于多进程的返回值问题，在普通的多进程中，无法取得函数返回值,只能通过队列、管道等方式进行多进程间的通信。
# 而在进程池中可以获取返回值，其中apply方法直接return结果
# 但是apply则返回进程的对象，可以通过 object.get()方式获取，但是会导致进程变成同步进程
# 解决方式为把执行结果添加到列表中，也就是将返回的对象先存储，最后再遍历列表通过对象的.get（）方法获取结果。
