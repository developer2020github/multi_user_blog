"""Module contains common hashing-relqted functions to be used for
either cookies or password handling
"""
import random
import string
import hashlib
import hmac

# Used as divider between portions
# of strings that are parsed into several
# variables
DIVIDER = "|"

# Constant to be used in cookies hashing
SECRET = 'imsosecret'


def make_salt():
    """
    creates a random string of 5 characters
    :return:
    """
    return ''.join(random.choice(string.ascii_letters) for n in range(5))


def make_pw_hash(name, password, salt=""):
    """
    Creates password hash in format
    (hash of name + password + salt)+ divider + salt
    Uses sha256 for hashing.
    :param name: username string
    :param password: password string
    :param salt: salt. if is not passed - will be created
    :return: string = (hash of name + password + salt)+ divider + salt
    """
    if salt == "":
        salt = make_salt()
    hash_value = hashlib.sha256(name+password+salt).hexdigest()
    return (str(hash_value)) + DIVIDER + salt


def valid_pw(name, password, pw_hash):
    """
    Validates password based on provided user name, password and hash value
    :param name: user name string
    :param password: password string
    :param pw_hash: password hash value
    ( password hash value is  hash(name + pws + salt) + divider + salt)
    :return: True if password is valid, False otherwise
    """
    salt = pw_hash.split(DIVIDER)[1]
    if pw_hash == make_pw_hash(name, password, salt):
        return True

    return False


# Following functions are to be used for cookie hashing

def hash_str(input_string, secret_value=SECRET):
    """
    Returns hmac hash of input string plus secret value
    :param input_string: input string
    :param secret_value: secret string to be added to s
                         Default value is module-level
                         constant SECRET
    :return: hmac hash of string plus secret value
    """
    return hmac.new(secret_value, input_string).hexdigest()


def make_secure_val(input_string, divider=DIVIDER):
    """
    Makes a string of input string + divider  + hmac hash
                of input string + secret word (see function hash_str for details)
    :param input_string: input string
    :param divider: divider symbol. Default value
                    is module-level constant DIVIDER
    :return: string as per function description
    """
    return input_string + divider + hash_str(input_string)


def check_secure_val(string_and_hash, divider=DIVIDER):
    """
    Validates hash of the input string
    :param string_and_hash: input = string + divider + hash of that string
    :param divider: divider to split on. Default value is module level constant DIVIDER
    :return:  if hash is valid return string , and None otherwise
    """
    val = string_and_hash.split(divider)[0]
    if string_and_hash == make_secure_val(val):
        return val
    return None


def make_secure_cookie(input_string):
    """
    A wrapper function around make_secure_value
    :param input_string: input string
    :return: sring of input string + divider  + hmac hash
             of input string + secret word (see function hash_str for details)
    """
    return make_secure_val(input_string)


def is_cookie_secure(cookie):
    """
    A srapper function around check_secure_val
    :param cookie:
    :return:  if hash is valid return string , and None otherwise
    """
    return check_secure_val(cookie)


def get_secure_cookie_value(request_object, cookie_name):
    """
    Checks if object has a specific cookie and if that cookie contains
     a combination of string and value hash of that string
    :param request_object: object to get cookie from
    :param cookie_name: name of the cookie to check
    :return: string value of the cookie if object has it and
            it and its hash is valid. None otherwise.
    """
    cookie = request_object.request.cookies.get(cookie_name)
    if cookie is None:
        return None
    secure_cookie_value = is_cookie_secure(cookie)
    return secure_cookie_value


def check_user_name_cookie(request_object, redirect_to_in_case_of_error,
                           username_cookie_name="user_id"):
    """
    A wrapper around get_secure_cookie_value function to be applied to check
    user name cookie. If check does not pass, redirects to another page
    :param request_object: object to reauest cookie from
    :param redirect_to_in_case_of_error: page to redirect if user name cookie is invalid
    :param username_cookie_name: name of username cookie (defaulted to "user_id")
    :return: user name if cookie is present and has valid hash, None otherwise
    """
    user_name = get_secure_cookie_value(request_object, username_cookie_name)
    if user_name is None:
        request_object.redirect(redirect_to_in_case_of_error)

    return user_name
