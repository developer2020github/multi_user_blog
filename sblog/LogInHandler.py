from Handler import Handler
'''
storing passwords:
table of user->hash(pw +salt), salt values, where salt is some random characters

look for function make_salt in homewrok
    def make_salt():
    ###Your code here
    return ''.join(random.choice(string.ascii_letters) for n in range(5))

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash(name, pw):
    ###Your code here
    salt = make_salt()
    h=hashlib.sha256(name+pw+salt).hexdigest()
    return "%s,%s" % (h, salt)

=================================================
vaidating salts

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# Implement the function valid_pw() that returns True if a user's password
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt=""):
    if salt=="":
        salt = make_salt()

    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    ###Your code here
    salt = h.split(",")[1]
    if h ==make_pw_hash(name, pw, salt):
        return True

    return False

h = make_pw_hash('spez', 'hunter2')
print valid_pw('spez', 'hunter2', h)

try using bcrypt
===================
'''

class LogInHandler(Handler):

    def get(self):
        self.render("login.html")


    def post(self):
        username=self.request.get("username")
        password = self.request.get("password")

        self.redirect("/welcome")