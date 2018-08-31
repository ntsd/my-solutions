
import os
import pickle    
import codecs
import io
import base64

class X:
    def out(self):
        print('xx')
# this just reference
obj = X()

pickled = codecs.encode(pickle.dumps(obj), "base64").decode()

print(pickled)

unpickled = pickle.loads(codecs.decode(pickled.encode(), "base64"))

unpickled.out()

# this full
with open("obj.pickle", 'wb') as obj_file:
    pickle.dump(obj, obj_file)

"""8003 635f 5f6d 6169 6e5f 5f0a 580a 7100
2981 7101 2e"""

with open('obj.pickle', 'rb') as obj_f:
    bytes_ = obj_f.read()
##    print(bytes_)
    print(len(bytes_))
    print(len(codecs.decode(bytes_, 'base64')))
    print(len(base64.urlsafe_b64decode(bytes_)),type(base64.urlsafe_b64decode(bytes_)))
    with open('obj.txt', 'w') as f:
        f.write(str(bytes_))
data = pickle.load(io.BytesIO(b'\x80\x03c__main__\nX\nq\x00)\x81q\x01.'))
data.out()
##with open('model.txt', 'rb') as f:
##    bytes_ = f.read()
##    data = pickle.load(io.BytesIO(base64.urlsafe_b64encode(bytes_)))
##    data.out()
