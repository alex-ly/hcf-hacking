import os

css = """
#ipython_notebook img {
    display: none;
}

#ipython_notebook {
}
#ipython_notebook a:before {
    content: "CSCI2000U %s";
    font-family: Helvetica;
    font-weight: bold;
    color: #888;
}
"""

user = os.environ.get('JUPYTERHUB_USER', '')
home = os.environ.get('HOME')
custom = os.path.join(home, ".jupyter", "custom")

try:
    os.makedirs(custom)
    with open(os.path.join(custom, "custom.css"), "w") as f:
        f.write(css % ("@" + user))
except:
    pass

