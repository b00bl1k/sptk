import gettext
gettext.install("sptk")

from sptk import app

app = app.SptkApplication(0)
app.MainLoop()
