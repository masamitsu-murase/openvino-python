import os
import shutil
import sys

if os.path.exists("src"):
    shutil.rmtree("src")

src_dir = "src_python%d.%d" % (sys.version_info.major, sys.version_info.minor)
shutil.copytree(src_dir, "src")
