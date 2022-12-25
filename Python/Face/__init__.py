__add__ = ["Emotion",
           "Eye_blink",
           "Face_detection"]

from . import Emotion
from . import Eye_blink
from . import Face_detection
import Option

mask_file_patha = ""
embedding_list_No = []
file_list = []
count = 0
embedding_list = []
#------------------------
down = 0.35
up = 0.05
embedding_list_Ma = []
fail_count = 0                 