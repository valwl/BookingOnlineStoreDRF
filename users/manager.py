from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    @classmethod
    def phone_normalise(cls, phone_number: str, ):
        if phone_number == '':
            return None
        else:
            digits = ''.join(filter(str.isdigit, phone_number))
            if len(digits) == 11:
                formatted_number = f'+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}'
            elif len(digits) == 10:
                formatted_number = f'+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}'
            else:
                return None
            return formatted_number

    def create_user(self, email=None, phone_number=None, password=None, **kwargs):
        if not email and not phone_number:
            raise ValueError('email or phone number must be sade')
        email = self.normalize_email(email) if email else None
        phone_number = self.phone_normalise(phone_number) if phone_number else None

        kwargs.setdefault('is_active', True)
        user = self.model(email=email, phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self.create_user(email, phone_number, password, **kwargs)