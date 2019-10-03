def sorted_intersect(list1, list2):
    """Intersects two (ascending) sorted lists and returns the sorted result
    
    Parameters
    ----------
    list1: List[Comparable]
    list2: List[Comparable]
        Sorted lists to be intersected
        
    Returns
    -------
    List[Comparable]
        Sorted intersection        
    """
    ### Begin your code
    cur2 = 0
    ret = []
    for ele in list1:
        while cur2<len(list2) and list2[cur2]<ele:
            cur2+=1
        if cur2>=len(list2):
            break
        # assert cur2 < len(list2) and list2[cur2] >= ele
        if ele == list2[cur2]:
            ret.append(ele)
            while cur2 < len(list2) and ret[-1] == list2[cur2]:
                cur2+=1
    return ret
    ### End your code