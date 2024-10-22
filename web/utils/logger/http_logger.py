import json
from datetime import datetime, timezone
from typing import Any

from fastapi import UploadFile
from rich.console import Console


class HttpLogger:
    _status_categories: dict[str, dict[str, str]] = {
        '1': {'title': 'Success', 'color': 'green'},
        '2': {'title': 'Success', 'color': 'green'},
        '3': {'title': 'Warning', 'color': 'yellow'},
        '4': {'title': 'Error', 'color': 'red'},
        '5': {'title': 'Error', 'color': 'red'},
    }

    def __init__(
        self,
        *,
        request_headers: dict[str, str],
        response_headers: dict[str, str],
        method: str,
        path: str,
        execution_time: float,
        status_code: str,
        form_body: list[tuple[str, UploadFile | str]],
        json_body: dict[str, Any] | None = None,
        response: dict[str, Any] | None = None,
    ) -> None:
        self._request_headers: dict[str, str] = dict(sorted(request_headers.items()))
        self._response_headers: dict[str, str] = dict(sorted(response_headers.items()))
        self._method: str = method
        self._path: str = path
        self._execution_time: float = execution_time
        self._status_code: str = status_code
        self._json_body: dict[str, Any] | None = json_body
        self._form_body: list[tuple[str, UploadFile | str]] = form_body
        self._response: dict[str, Any] | None = response

    def log(self) -> None:
        category: dict[str, str] = self._status_categories[self._status_code[0]]
        self._write_log(title=category['title'], color=category['color'])

    def _write_log(self, *, title: str, color: str) -> None:
        console: Console = Console(color_system='truecolor')

        now: datetime = datetime.now(timezone.utc)
        timestamp: str = now.strftime("%d/%m/%Y - %H:%M:%S.%f")[:-3]

        basic_info: dict[str, str] = {
            'Status code': self._status_code,
            'Timestamp': f'{timestamp} UTC',
            'Method': self._method,
            'Path': self._path,
            'Execution time': f'{self._execution_time:.4f} s',
        }

        console.print()
        self._print_log_title(
            console,
            color=color,
            title=title,
            method=basic_info["Method"],
            path=basic_info["Path"],
            status_code=basic_info["Status code"],
            execution_time=basic_info["Execution time"],
        )

        self._print_dict(console, title='Basic Info', data=basic_info)
        self._print_dict(
            console,
            title='Request Headers',
            data=self._request_headers,
            upper_keys=True,
        )
        self._print_dict(
            console,
            title='Response Headers',
            data=self._response_headers,
            upper_keys=True,
        )

        if len(self._form_body):
            self._print_form_data(console, title='Body', data=self._form_body)
        else:
            self._print_json(console, title='Body', data=self._json_body)

        self._print_json(console, title='Response', data=self._response)

        console.print()

    def _print_log_title(self, console: Console, *, color: str, **data: str) -> None:
        console.rule(
            (
                f'[bold {color}] {data["title"]} | '
                f'{data["method"]} '
                f'{data["path"]} '
                f'{data["status_code"]} | '
                f'{data["execution_time"]}[/]'
            ),
            style=f'{color}',
        )

    def _print_dict(
        self,
        console: Console,
        *,
        title: str,
        data: dict[str, str],
        upper_keys: bool = False,
    ) -> None:
        console.print(f'\n[bold green]{title}[/]')

        for key, value in data.items():
            console.print(f'[white]{key.upper() if upper_keys else key}: {value}[/]')

    def _print_json(
        self,
        console: Console,
        *,
        title: str,
        data: dict[str, Any] | None,
    ) -> None:
        if data:
            console.print(f'\n[bold green]{title}[/]')
            console.print_json(json.dumps(data, indent=4, ensure_ascii=False))

    def _print_form_data(
        self,
        console: Console,
        *,
        title: str,
        data: list[tuple[str, UploadFile | str]],
    ) -> None:
        console.print(f'\n[bold green]{title}[/]')

        for key, value in data:
            console.print(f'[bold plum2]{key}[/][white] = [/][green]"{value}"[/]')
