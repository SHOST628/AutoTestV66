import os
import multiprocessing


def copy_file(file_name,old_folder,new_folder,q):
    # print("copy file %s from %s to %s" % (file_name,old_folder,new_folder))
    o_file_name = old_folder + "/" + file_name
    n_file_name = new_folder + "/" + file_name
    f_read = open(o_file_name,"rb")
    content = f_read.read()
    f_read.close()

    f_write = open(n_file_name,"wb")
    f_write.write(content)
    f_write.close()
    q.put(file_name)

def main():
    # get folder needed to copy
    old_folder = input("please input folder path : ")
    # new folder to store file
    try:
        new_folder = old_folder + "_copy"
        os.mkdir(new_folder)
    except:
        pass
    # get file list
    file_names = os.listdir(old_folder)
    # create process pool
    pool = multiprocessing.Pool(5)
    # create queue to store file_name having finished copying
    q = multiprocessing.Manager().Queue()
    # copy file
    for file_name in file_names:
        pool.apply_async(func=copy_file, args=(file_name, old_folder, new_folder,q))

    pool.close()
    # pool.join()
    all_file_num = len(file_names)
    ok_file_num = 0
    while True:
        file_name = q.get()
        ok_file_num += 1
        if all_file_num == ok_file_num:
            print("\rfinishing percentage : %.2f %%" % (ok_file_num * 100 / all_file_num), end="")
            break


if __name__ == '__main__':
    main()