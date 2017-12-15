import numpy as np

file_name = 'test_file'

''' Read csv type file in input
    Check that the input file has an appropriate format for a detection file'''

def read_file(file_name):
    d = []
    todiscard = []
    f = open(file_name)
    D = map(lambda x: x.split(" "),f.readlines())
    D = map(lambda x: map(lambda y: float(y),x),D)

    ncol = len(D[0])
    result_array = np.zeros((len(D), ncol))

    for i in range(len(D)):
        result_array[i,:] = D[i]
        if (result_array[i,0], result_array[i,1]) not in d:
            d.append((result_array[i,0],result_array[i,1])) # adding tuple (time,Id), ensuring that it is unique in the file
        else:
            todiscard.append(i)
            print ('wrong format for the input file,'+ 
                            'there should not be several occurences'+ 
                            ' of the same tuple (Time,ID) '+
                'discarding incriminated input')
    result_array = np.delete(result_array, [todiscard], 0)
    return result_array


if __name__ == '__main__':
    import sys
    obs_file = str(sys.argv[1])
    print obs_file
    obs = read_file(obs_file)
