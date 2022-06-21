import os

def my_rename(path):
    print(path)
    sub = os.listdir(path)
    print(sub)

    for s in sub:
        ns = str(s)
        if ns[0] == ' ':
            ns = ns[1:]
        ns = ns.replace(' ', '_')
        if s != ns:
            os.rename(path+s, path+ns)
            ns = s
        if os.path.isdir(path+ns):
            my_rename(path+ns+'/')

def main():
    path = "C:/Users/lenovo-admin/Desktop/220218_background/"

    my_list = os.listdir(path)
    print(my_list)

    my_rename(path)


#os.rename('a.txt', 'b.kml')

if __name__ == "__main__":
    main()
