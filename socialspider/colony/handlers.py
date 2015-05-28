from iflux.core import IfluxHandler


class IndexHandler(IfluxHandler):

    def get(self):
        self.render(
            'index.html',
            colony_name=self.component.colonies['default']['name'],
            web_name=self.component.webs['default']['name']
        )
