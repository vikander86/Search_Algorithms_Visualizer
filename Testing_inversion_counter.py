import itertools

def inversion_counters(array):
    number_of_inversion = 0
    length = len(array)
    number_of_inversion = sum(1 for i in range(length) for j in range(i+1, length)
                                  if 0 not in (array[i],array[j])
                                  and array[i] > array[j])
    if number_of_inversion % 2 == 0:
        return True            

# array = [1,2,5,4,8,7,6,0,3]

# test = inversion_counters(array)
# print(test)

count=0
test = list(itertools.permutations([0,1,2,3,4,5,6,7,8]))
count = sum(1 for i in test if inversion_counters(i))
print(test[0])
# for i in test:
#     if inversion_counters(i):
#         count +=1
print(count)
print(len(test))