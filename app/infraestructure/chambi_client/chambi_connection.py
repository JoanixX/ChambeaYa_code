import os
import httpx

CHAMBI_RAG_URL = os.getenv("CHAMBI_RAG_URL")

async def consultar_chambi(historial: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CHAMBI_RAG_URL}/preguntar",
            json={"historial": historial},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()