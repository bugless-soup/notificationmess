import sys

import notificationmess


gettrace = getattr(sys, 'gettrace', None)
notificationmess.start(gettrace is not None and gettrace())
