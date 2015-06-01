from iflux.core import IfluxHandler


class IndexHandler(IfluxHandler):

    def get(self):
        self.render(
            'index.html',
            colony_name=self.component.colony,
            web_name=self.component.web['name']
        )
