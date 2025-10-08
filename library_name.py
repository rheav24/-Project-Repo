#Vinindi
def calcualte_remain_date(due_date, borrowed_date):
    """Calculating the reamin dates to return the materails.
    Args:
    import date for this task
    due_date is the date when the book should be returned
    borrowed_date is the date when the meterials were borrowed
    Returns
    This will return how many days reamin for return if the cutomer wants to avoid the fine
    Raises:
    TypeError: if due_date and borrowed_date is not in the date type

    Example:
    from datetime import date
    calcualte_remain_date(10,08,2025, 10,14,2025)
    6
    """
    if not isinstance(due_date, date) or not isinstance(borrowed_date, date): #isinstance use for the check the input or something in the right type or not
         raise: TypeError("The time format is not in the right format")
    remain_days = (due_date - borrowed_date).days #.days is for get the exact days as numbers
    return remain_days
#########################################################
def calculate_due_date(borrowed_date):
    """Calcualte how many days should be given as a loan.
    Args:
    import date for this task
    borrowed_date is the date when the meterials were borrowed
    Returns
    This will return how many days can given to the customer for keeping the book
    Raises:
    TypeError: borrowed_date is not in the date type

    Example:
    from datetime import date  #Used datetime becuase for importing datetime module that can help us to work with proper dates and time
    calculate_duedate(date(10,10,2025))
    datetime.date(10,24,2025)   
    
    """
    if not isinstance(borrowed_date, date): #isinstance use for the check the input or something in the right type or not
         raise: TypeError("The time format is not in the right format")
    due_date = borrowed_date + timedelta(days= 14) #timedelta is for the time difference like add 14 days for caulating due date
    return due_date
    
    

################################################################
def calcualte_overdue_days(due_date, returned_date):#can change as 
    """Calculating the overdue days for the book.
    Args:
    import date for this task
    due_date is the date when the book should be returned
    returned_date is the date when the custoemr retunred the book

    
    Returns
    Program returns the number of due dates

    Raises
    TypeError: if due_date and returned_date is not in the date type

    Example:
    import date
    calcualte_overdue_days((10,09,2025), (10,10,2025))
    1
    calcualte_overdue_days((10,09,2025), (10,01,2025))
    0
    """
    if not isinstance(due_date, date) or not isinstance(returned_date, date): #isinstance use for the check the input or something in the right type or not
         raise: TypeError("The time format is not in the right format")
    overdue_days = (returned_date - due_date).days
    return max(overdue_days, 0) #if 0 then return the zero avoiding  the negative 

##############################################################################################################################################################33
def search_author(keyword, catalog): #can change as search by category
    """ Searching the author by name and match the name.
    Args:
    keyword is a string which can use as names for search
    catalog is a list that conatians the detials of authors names

    Return:
    if the author name found in the catalog as found
    if the name was not in the list return "No author found for your search" as the name not found.
    Raises:
    Catalog must be a list

     Example:
       catalog = ["J.K. Rowling", "Rick Riordan", "Dan Brown"]
       search_author("J.K. Rowling", catalog)
        "J.K. Rowling"
       search_author("Stephen King", catalog)
        'Author not found'
    """
    if not isinstance(catalog,list):
        raise TypeError("Catalog should be a list")
    for author in catalog:
        if keyword.lower() == author.lower():
            return author
    return "Author not found" # return as not found 
####################################################################################3    
def calculate_overdue_fine(overdue_days): #can change as 
    """ Calcualte overdue fines 
    Args:
    overdue_days as an int - days like how many days that customer was late to returned the book
    Return:
    The fine amount in total
    Raises:
    Days should be count as integers
    Example:
    calcualate_overdue_fine(2, 0):
    0
    calcualate_overdue_fine(4, 5):
    16
    """
    if not isinstance(overdue_days, int): #checking the input as an integer
        raise TypeError("Days cannot be float")
    if overdue_days <= 2:
        fine = 0 * overdue_days
    elif 3 <overdue_days <= 5:
        fine = 5 * overdue_days
    elif 6 <overdue_days <= 10:
        fine  = 8 *overdue_days
    elif overdue_days >=11:
        fine = 10 * overdue_days

    return fine
        
    
