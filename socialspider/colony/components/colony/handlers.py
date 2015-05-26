from iflux.core import IfluxHandler


class IndexHandler(IfluxHandler):

    def get(self):
        self.render('index.html')


