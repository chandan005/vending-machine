class UserNotFoundException(Exception):
    def __init__(self, message='USER NOT FOUND.'):
        # Call the base class constructor with the parameters it needs
        super(UserNotFoundException, self).__init__(message)

class UserExistsException(Exception):
    def __init__(self, message='USER ALREADY EXISTS.'):
        # Call the base class constructor with the parameters it needs
        super(UserExistsException, self).__init__(message)

class UserNotBuyerException(Exception):
    def __init__(self, message='USER NOT BUYER.'):
        # Call the base class constructor with the parameters it needs
        super(UserNotBuyerException, self).__init__(message)
        
class UserInSufficientDepositException(Exception):
    def __init__(self, message='INSUFFICIENT DEPOSIT AMOUNT AVAILABLE FOR USER.'):
        # Call the base class constructor with the parameters it needs
        super(UserInSufficientDepositException, self).__init__(message)
        
class SellerDoesNotExistException(Exception):
    def __init__(self, message='SELLER DOES NOT EXIST.'):
        # Call the base class constructor with the parameters it needs
        super(SellerDoesNotExistException, self).__init__(message)
        
class ProductNotFoundException(Exception):
    def __init__(self, message='PRODUCT NOT FOUND.'):
        # Call the base class constructor with the parameters it needs
        super(ProductNotFoundException, self).__init__(message)

class ProductDoesNotBelongToSellerException(Exception):
    def __init__(self, message='PRODUCT DOES NOT BELONG TO SELLER.'):
        # Call the base class constructor with the parameters it needs
        super(ProductDoesNotBelongToSellerException, self).__init__(message)
        
class ProductStockUnavailableException(Exception):
    def __init__(self, message='PRODUCT STOCK NOT AVAILABLE'):
        # Call the base class constructor with the parameters it needs
        super(ProductStockUnavailableException, self).__init__(message)
        
class DepositExistsBeforeDeletionException(Exception):
    def __init__(self, message='DEPOSIT EXISTS FOR USER'):
        # Call the base class constructor with the parameters it needs
        super(DepositExistsBeforeDeletionException, self).__init__(message)
        
class ProductExistsForSellerBeforeDeletionException(Exception):
    def __init__(self, message='PRODUCT EXISTS FOR SELLER'):
        # Call the base class constructor with the parameters it needs
        super(ProductExistsForSellerBeforeDeletionException, self).__init__(message)

class DepositNotAllowedException(Exception):
    def __init__(self, message='DEPOSIT NOT ALLOWED. ALLOWED VALUES ARE: [5, 10, 20, 50 ,100]'):
        # Call the base class constructor with the parameters it needs
        super(DepositNotAllowedException, self).__init__(message)

class DatabaseException(Exception):
    def __init__(self, message='ERROR INSERTING/UPDATING DATA.'):
        # Call the base class constructor with the parameters it needs
        super(DatabaseException, self).__init__(message)

class InvalidObjectIdException(Exception):
    def __init__(self, message='INVALID OBJECTID.'):
        # Call the base class constructor with the parameters it needs
        super(InvalidObjectIdException, self).__init__(message)