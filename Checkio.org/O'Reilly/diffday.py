def leapyr(n):
    if n % 400 == 0:
        return True
    if n % 100 == 0:
        return False
    if n % 4 == 0:
        return True
    else:
        return False
        
def days_diff(date1, date2):
    """
        Find absolute diff in days between dates
    """
    date = sorted(list([date1, date2])) #sort before date first
    y1 = date[0][0]
    m1 = date[0][1]
    d1 = date[0][2]
    y2 = date[1][0]
    m2 = date[1][1]
    d2 = date[1][2]
    year = 0
    month = 0
    day = 0
    dayofmonth = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    dayofmonth_leapyear = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    #count day of year+1 to year-1
    year2 = 0
    start = y1+1
    end = y2-1
    while start<=end:
        if leapyr(start):
            break
            year2 += 366  
        else:
            year2 += 365
        start += 1
    while start<=end:
        if leapyr(end):
            year2 += 366
            break
        else:
            year2 += 365
        end -= 1
    
##    for i in range(y1+1, y2):
##        if leapyr(i):
##            year += 366
##        else:
##            year += 365

    cost = 365.2424939951962
    
    
##    try:
##        cost = (year-year2)/(end-start)
##    except:
##        cost = 0
##    print(start, end, year2+round((end-start)*cost),"||",y1+1,y2-1, year,"cost:",(year-year2)/(end-start))

    year = year2+round((end-start)*cost)
    if year < 0:
        year = 0
    if start-end == 1:
        year = 365
    
    #check y1 and y2 is leapyear
    if leapyr(y1):
##        print("y1 leapyear")
        dayofmonth_y1 = dayofmonth_leapyear
    else:
##        print("y1 not leapyear")
        dayofmonth_y1 = dayofmonth
    if leapyr(y2):
##        print("y2 leapyear")
        dayofmonth_y2 = dayofmonth_leapyear
    else:
##        print("y2 not leapyear")
        dayofmonth_y2 = dayofmonth
    #check year1 == year2 for count day form month
    if(y1 == y2):
        range_month = range(m1+1, m2)
        for i in range_month:
            month += dayofmonth_y1[i]
    else:
        range_month_y1 = range(m1+1, 12+1)
        for i in range_month_y1:
            month += dayofmonth_y1[i]
##            print(i, dayofmonth_y1[i])
        range_month_y2 = range(1, m2)
        for i in range_month_y2:
            month += dayofmonth_y2[i]
##            print(i, dayofmonth_y2[i])
    
    if(y1 == y2 and m1 == m2):
        day = d2-d1
    else:
        day += (dayofmonth_y1[m1]-d1)+d2
##    print(year, month, day, year + month + day)
    return year + month + day
        
if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert days_diff((1982, 4, 19), (1982, 4, 22)) == 3
    assert days_diff((2014, 1, 1), (2014, 8, 27)) == 238
    assert days_diff((2014, 8, 27), (2014, 1, 1)) == 238
    assert days_diff((1,1,1), (9999,12,31))== 3652058
    assert days_diff((2012,2,29), (2014,2,28))== 730
    assert days_diff((1970,1,1), (2000,1,1)) == 10957
    assert days_diff((4139,10,30), (4923,12,23)) == 286404
