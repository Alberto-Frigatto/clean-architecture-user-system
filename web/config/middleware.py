import json
import time
from collections.abc import AsyncGenerator, Callable
from typing import Any

from fastapi import FastAPI, Request, Response, UploadFile
from starlette.concurrency import iterate_in_threadpool

from web.utils.logger import HttpLogger


def add_middlewares(app: FastAPI, *, test: bool) -> None:
    if test:

        @app.middleware('http')
        async def http_log_middleware(
            request: Request, call_next: Callable[[Any], Any]
        ) -> Response:
            body: dict[str, Any] | None = None

            try:
                body = json.loads(await request.body())
            except json.decoder.JSONDecodeError:
                pass

            form: list[tuple[str, UploadFile | str]] = (
                await request.form()
            ).multi_items()  # type: ignore

            start_time: float = time.perf_counter()
            response: Response = await call_next(request)
            process_time: float = time.perf_counter() - start_time

            response_body: dict[str, str | Any] | None = None

            try:
                response_body_data: list[bytes] = [
                    section async for section in response.body_iterator  # type: ignore
                ]
                response.body_iterator: AsyncGenerator = iterate_in_threadpool(  # type: ignore
                    iter(response_body_data)
                )
                response_body = json.loads(b"".join(response_body_data))
            except json.decoder.JSONDecodeError:
                pass

            HttpLogger(
                request_headers=dict(request.headers),
                response_headers=dict(response.headers),
                method=request.method,
                path=request.url.path,
                execution_time=process_time,
                status_code=str(response.status_code),
                json_body=body,
                form_body=form,
                response=response_body,
            ).log()

            return response
