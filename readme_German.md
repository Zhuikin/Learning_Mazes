# 10.11.2023

# Pfadsuchen im Labyrint
Eine Schnittstelle für Agentenbasierte Pfadsuche. 
Es werden die nötigen Funktionen bereitgestellt um den Agenten in einer 
(Gitter-basierten) Umgebung zu bewegen. 
Die details der Umgebung werden verschleiert.

Es werden keine "exotischen" Zusatzmodule benötigt.
(Ausser für die Curses Demo).

## Geeignete Alogrithmen
Man könnte hier drauf gängine Pfadsuche Algorithmen ausführen.
Rekursive Erforschung, Tiefensuche, Breitensuche, A*

## Frozen Lake
Ist eine spezielle Variante, die insbesondere als Beispiel für 
Machine Learning geeignet ist.
Hierbei hat die Umgebung - zusätzlich zu den üblichen Wänden -
"Löcher im Eis" in die der Agent hinein fallen könnte. Dies führt

## Q-Learning
Ein Reinforcment Learning (Bestärkendes Lernen) Algorithmus, kann
für die Frozen Lake Umgebung verwendet werden.

# Kurzanleitung

## maze_agent_access.py
Der vorgesehene Umgang ist, eine Instanz der Klasse MazeAgentAccess 
zu erstellen und deren Methoden als Interface für den Agenten zu nutzen. 

Beispiel für eine Instanz:
bob = MazeAgentAccess(name="Bob", maze_foldername="Lab_4x4")

maze_foldername ist der Name des Ordners mit den Daten für die Maze.

### Diese Properties geben auskunft über grundlegende eigenschaften der 
Umgebung

states -> int @property
actions -> int @property
action_space -> list of function pointers @property

### Die Properties ermöglichen es dem Agenten, seinen Status abzufragen
Der Agent muss selbst dafür Sorge tragen, wo relevant, seinen Status zu 
prüfen und darauf zu reagieren.

is_at_start -> bool @property
is_at_goal -> bool @property
is_in_hole -> bool @property
can_go_left -> bool @property
can_go_right -> bool @property
can_go_up -> bool @property
can_go_down -> bool @property

### Aktionsmethoden. Geben True, wenn die Aktion ausgeführt wurde.

step_left() -> bool
step_right() -> bool
step_up() -> bool
step_down() -> bool
reset_to_start() -> bool

### Hilfsmethoden um valide Aktionen abzufragen und auszuführen.
Alle können jederzeite versucht werden. Der Agent wird daran gehindert, 
illegale Aktionen auszuführen.
Der Rückgabewert gibt Auskunft darüber, ob die Aktion ausgeführt wurde.

get_valid_moves() -> list of function pointers


### Hilfsmethoden zum Darstellen der Umgebung.
Diese sind eher für den Nutzer und weniger für den Agenten gedacht.  

get_maze_view_buffer() -> str
print_maze() 

## mazes Unterordner
Hier werden standardmässig Umgebungen als Unterordner abgelegt und 
geladen.
Einige "maps" sind mitgeliefert.

## maze_editor.py
Eine mini-App zum Erstellen und bearbeiten von Mazes.
(Die Mazes werden als map.JSON Dateien im dazugehörigen Ordnern gespeichert).
Die JSON Dateien könnten auch händisch bearbeitet werden.

## maze_demo_simple und maze_demo_backtrack_pathfinder
Kleine Demos, die den Umgang mit der Agentenklasse zeigen.

## maze_demo_curses.py
Eine interaktive Demo (wo der Nutzer den Agenten vertritt).
Diese erfordert das package windows-curses (pip install windows-curses)
und kann nur in einem Terminal. Power-shell oder Terminal in PyCharm.
(Aicht aber das normale "run".) 
