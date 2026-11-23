# PyBookmarker

A small bookmark manager in Python: a client that talks to a local bookmark server over HTTP, and a Tkinter desktop GUI.

> Course assignment — ICS 32 (Programming with Software Libraries), UC Irvine, 2025. The bookmark server and protocol module were provided by the course.

## Parts

| Folder | What it is |
|---|---|
| `a4_part1/` | **HTTP client.** Encodes add/delete/list requests in the course's bookmark protocol as JSON and sends them with `urllib` to the provided local server (`bookmark_server.py`), with error handling for network failures |
| `a4_part2/` | **OOP exercise.** A virtual dog-adoption and feeding simulation built on an abstract `Dog` base class with breed-specific subclasses |
| `a4_part3/` | **Tkinter GUI.** A desktop app with a tree view of saved URLs, a text box for new ones, Add/Delete buttons wired through callbacks, and an *Open…* menu to load a bookmark file |

## Running

```bash
# Part 1: start the server, then the client
cd a4_part1 && python bookmark_server.py     # in one terminal
cd a4_part1 && python a4_p1.py               # in another

# Part 3: GUI
cd a4_part3 && python a4_p3.py
```
