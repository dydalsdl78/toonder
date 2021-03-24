from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import uuid

# 신규 유저 만드는 함수 하나와
# superuser 만드는 함수 하나를 만들어야 한다.

class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("이메일이 있어야 합니다.")

        if not username:
            raise ValueError("유저네임이 있어야 합니다.")

        #normalize는 대문자를 전부 소문자화 해준다. 
        user = self.model(
            email=self.normalize_email(email),
            # 이건 로그인용이 아니니까 normalize안해줘도 된다. 
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            # 이건 로그인용이 아니니까 normalize안해줘도 된다. 
            username=username,
            password=password
        )
        # superuser이기 때문에 아래 세가지가 True이다. 
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




# profile image를 갖고오기 위한 함수
def get_profile_image_filepath(self, filename):
    print(self.user_id)

    return f'profile_images/{self.user_id}/{"profile_image.png"}'


def get_default_profile_image():
    return "/default_profile.png"




class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=254, unique=True)
    username = models.CharField(unique=True, max_length=50)
    date_joined = models.DateTimeField(verbose_name = 'date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    # 아래 네가지는 AbstractBaseUser에 포함되어있기 때문에 반드시 정의해줘야 한다. is_active 랑 is_staff는 별로 쓸일이 없을 수 있따.
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # 이미지 필드는 pillow 패키지가 필요하다 pip install pillow했으며 freeze 하겠습니다. 
    profile_image = models.ImageField(upload_to=get_profile_image_filepath, max_length=255, blank=True, default=get_default_profile_image)
    
    #매니저랑 연결해주자
    objects = MyUserManager()

    # 로그인할때 쓸 거
    USERNAME_FIELD = 'email'
    # 로그인용이 email이고 required에 username이 추가되었으므로 두가지가 다 있어야지 회원가입이 가능하다. 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/{self.pk}/'):]

    # AbstractBaseUser에 있는 권한 관련 def이다.
    # permission 있니? 라고하면 is_admin으로 대답한다
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # 이것도 정의해줘야되서 하는데 크게 상관없다. 
    def has_module_perms(self, app_label):
        return True
    
    
