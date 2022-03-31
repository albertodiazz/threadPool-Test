import websockets 


async def sendMessage(msg):
    '''
        [args : str]: [Puede ser cualquier cosa solo es el pretexto 
                       para activar la funcion handler]
    '''
    # Estoy seguro que esto se puede mejorar y asi poder activar el handler
    # de forma directa sin necesidad de hacer esto.
    # Se me ocurre probar con Queue
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send(msg)
        await websocket.recv()
