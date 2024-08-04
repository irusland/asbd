from api.deps import DepsContainer
from api.server import Server

app = DepsContainer().resolve(Server)
