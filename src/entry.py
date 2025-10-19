from workers import WorkerEntrypoint
from router import Router

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        router = Router(self.env)
        return await router.handle(request, None)
    
    async def on_fetch(self, request):
        router = Router(self.env)
        return await router.handle(request, None)
    
