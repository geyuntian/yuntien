from yuntien.authext.models.user import get_current_user
from yuntien.authext.models.ra import RAEntMixin

#define roles
ROLE_ADMIN          = 'a'
ROLE_OWNER          = 'o'
ROLE_USER           = 'u'
ROLE_GUEST          = 'g'

#define operations
OPERATION_QUERY     = 'query'
OPERATION_ADD       = 'add'
OPERATION_DISPLAY   = 'display'
OPERATION_EDIT      = 'edit'
OPERATION_DELETE    = 'delete'
OPERATION_POST      = 'post'

AUTH = {}

AUTH[ROLE_ADMIN] = {
OPERATION_QUERY     : True,
OPERATION_ADD       : True,                         
OPERATION_DISPLAY   : True,
OPERATION_EDIT      : True,                         
OPERATION_DELETE    : True,
OPERATION_POST      : True,
}

AUTH[ROLE_OWNER] = {
OPERATION_QUERY     : True,
OPERATION_ADD       : True,                         
OPERATION_DISPLAY   : True,
OPERATION_EDIT      : True,                         
OPERATION_DELETE    : True,                         
OPERATION_POST      : True,
}

AUTH[ROLE_USER] = {
OPERATION_QUERY     : True,
OPERATION_ADD       : True,                         
OPERATION_DISPLAY   : True,
OPERATION_EDIT      : False,                         
OPERATION_DELETE    : False,                         
OPERATION_POST      : True,
}

AUTH[ROLE_GUEST] = {
OPERATION_QUERY     : True,
OPERATION_ADD       : False,                         
OPERATION_DISPLAY   : True,
OPERATION_EDIT      : False,                         
OPERATION_DELETE    : False,                         
OPERATION_POST      : False,
}

class Auth(object):
    check_parent = False
    
    @classmethod
    def get_auth_def(cls):
        return AUTH
    
    @classmethod
    def get_role(cls, obj, user):
        return _get_role(obj, user)
    
    @classmethod
    def get_auth(cls, obj=None, user=None):
        if not user:
            user = get_current_user()
        
        role = cls.get_role(obj, user)
        if role == ROLE_ADMIN:
            return cls.get_auth_def()[role]
      
        current_cls = cls
        while obj is not None and current_cls.check_parent == True:
            obj = obj.get_auth_parent()
            if obj:
                current_cls = obj.get_auth_class()
                role_tmp = current_cls.get_role(obj, user)
                if current_cls._compare_role(role_tmp, role):
                    role = role_tmp
      
        return cls.get_auth_def()[role]
    
    @classmethod
    def check_auth(cls, obj, operation, user=None):
        role = cls.get_role(obj, user)
        if role == ROLE_ADMIN:
            return True
        
        if cls.get_auth_def()[role][operation] == True:
            return True
      
        current_cls = cls
        while obj is not None and current_cls.check_parent == True:
            obj = obj.get_auth_parent()
            if obj:
                current_cls = obj.get_auth_class()
                role = current_cls.get_role(obj, user)
                
                if cls.get_auth_def()[role][operation] == True:
                    return True
      
        return False

    @classmethod
    def _compare_role(cls, role1, role2):
        return _comp_role(role1, role2)
    
class AuthWithRA(Auth):
    @classmethod
    def get_role(cls, obj, user):
        if not user.is_authenticated():
            return ROLE_GUEST
        
        if user.is_superuser:
            return ROLE_ADMIN
      
        if obj is not None and isinstance(obj, RAEntMixin):
            role = obj.get_role(user)
            if role:
                return role
      
        return ROLE_GUEST

class AuthCheckParent(Auth):
    check_parent = True
    
class AuthCheckParentWithRA(AuthWithRA):
    check_parent = True
    
class AuthEntMixin(object):
    @classmethod
    def get_auth_class(cls):
        return Auth
    
    def get_auth(self, user=None):
        return self.get_auth_class().get_auth(self, user)
    
    @property
    def auth(self):
        return self.get_auth(get_current_user())
        
    def check_auth(self, operation, user=None):
        return self.get_auth_class().check_auth(self, operation, user)
    
    def get_owner(self):
        return None

    def get_owner_id(self):
        return None
    
    def get_auth_parent(self):
        return None

def _get_role(obj, user):
    if not user.is_authenticated():
        return ROLE_GUEST
    
    if user.is_superuser:
        return ROLE_ADMIN
  
    if obj is not None:
        owner_id = obj.get_owner_id()
        if owner_id is None:
            owner_id = obj.get_owner().id
        if user.id == owner_id:
            return ROLE_OWNER
    return ROLE_USER

def _comp_role(role1, role2):
    rating = {
        ROLE_ADMIN    : 9,
        ROLE_OWNER    : 8,
        ROLE_USER     : 7,
        ROLE_GUEST    : 0,
    }

    return rating[role1] > rating[role2]
