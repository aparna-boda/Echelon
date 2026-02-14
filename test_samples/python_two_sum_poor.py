# Two Sum - Bad Implementation

def twosum(nums,target):
    # nested loops - very slow
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i!=j:
                if nums[i]+nums[j]==target:
                    return [i,j]
    return None

# test
nums=[2,7,11,15]
target=9
print(twosum(nums,target))

nums2=[3,2,4]
target2=6
print(twosum(nums2,target2))

# another test
a=[3,3]
b=6
result=twosum(a,b)
print(result)
