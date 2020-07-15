import os

def FindFile(filename, ext_swap=None, if_none_create=False):
    if ext_swap is not None:
        if "." in ext_swap:
            FindFile(filename.replace(filename.split('.')[-1], ext_swap))
        else:
            FindFile(filename.replace('.'+filename.split('.')[-1], ext_swap))
    else:
        for root, dirs, files in os.walk('/'+os.path.abspath(os.getcwd()).split('/')[1]):
            for file in files:
                if file == filename:
                    return os.path.join(root, file)
        if if_none_create:
            if (filename.split('.')[-1] == 'h5') and (ext_swap.split('.')[-1] == 'fil'):
                os.system('h52fil '+filename)
                return FindFile(filename)
            elif (filename.split('.')[-1] == 'fil') and (ext_swap.split('.')[-1] == 'h5'):
                os.system('fil2h5 '+filename)
                return FindFile(filename)
            else:
                print('%s does not exist' % (filename))
        raise FileNotFoundError


