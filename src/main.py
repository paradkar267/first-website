import os
from typing import Callable, Iterable, Iterator, List, Optional, Any


def map_entries(transform: Callable[[str], str]) -> Callable[[Iterable[str]], Iterable[str]]:
    def _inner(entries: Iterable[str]) -> Iterator[str]:
        for entry in entries:
            yield transform(entry)
    return _inner


def filter_entries(predicate: Callable[[str], bool]) -> Callable[[Iterable[str]], Iterable[str]]:
    def _inner(entries: Iterable[str]) -> Iterator[str]:
        for entry in entries:
            if predicate(entry):
                yield entry
    return _inner


def sort_entries(key: Optional[Callable[[str], Any]] = None, reverse: bool = False) -> Callable[[Iterable[str]], List[str]]:
    def _inner(entries: Iterable[str]) -> List[str]:
        return sorted(entries, key=key, reverse=reverse)
    return _inner


def pipe(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    for fn in funcs:
        value = fn(value)
    return value


def list_entries(
    directory: str,
    transform: Optional[Callable[[Iterable[str]], Iterable[str]]] = None,
    list_dir: Callable[[str], Iterable[str]] = os.listdir,
) -> List[str]:
    entries = list_dir(directory)
    if transform is not None:
        entries = transform(entries)
    return list(entries)


def list_files(directory: str) -> List[str]:
    return list_entries(directory)


def list_files_with_extension(directory: str, extension: str) -> List[str]:
    return list_entries(directory, transform=filter_entries(lambda name: name.endswith(extension)))


def list_files_sorted(directory: str, reverse: bool = False) -> List[str]:
    return list_entries(directory, transform=sort_entries(reverse=reverse))
