import asyncio

import tornado.web

from .cli import add_command

# hosts JS that logs and displays current data
# should be able to recover the data, from the data json until delted


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


async def launch(port):
    app = make_app()
    app.listen(port)
    await asyncio.Event().wait()


def main(args):
    asyncio.run(launch(args.port))


def parser_build(parser):
    parser.add_argument(
        "-p", "--port",
        default=8888, type=int,
        help="port to serve website on",
    )

    return parser


add_command(
    name='website',
    function=main,
    parser_build=parser_build,
    command_help='Launch website UI',
)
