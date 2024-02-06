
def inversion_counter(array):
    number_of_inversion = 0
    for i in range(len(array)):
        index = i + 1
        for j in range(index,len(array)):
            print(array[i], array[j])
            if array[i] == array[j] or array[j] == 0 or array[i] == 0:
                continue
            elif array[i] > array[j]:
                number_of_inversion += 1
                
    return number_of_inversion

array = [1,2,5,4,8,7,6,0,3]

test = inversion_counter(array)
print(test)