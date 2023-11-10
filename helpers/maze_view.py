class MazeView:

    def __init__(self, name, maze,
                 offset_x=1, offset_y=1):
        self.name = name
        self.maze = maze
        # foreground buffer is a list of dicts
        # {"x": int, "y": int, "icon": str}
        self.fg_buffer = []
        self.offset_x = offset_x
        self.offset_y = offset_y

    def draw_ascii_art(self) -> str:
        """ creates a terminal friendly ascii-art string
            from the current buffer
        """
        artsy_string = f"{self.name}"

        for line in self.frame_buffer():
            artsy_string += "\n" + "".join(line)

        return artsy_string

    def frame_buffer(self) -> list:
        """ combines bg and foreground into a frame
        """
        frame = self.maze.ascii_art_buffer()
        for entry in self.fg_buffer:
            try:
                x = entry["x"] + self.offset_x
                y = entry["y"] + self.offset_y
                icon = entry["icon"]
                icon = icon[:3]
            except ValueError:
                # we just don't print bad entries
                pass
            else:
                # note: coordinates inverted
                # because the frame buffer is a list of lines
                # we pick the line [y] first, and column [x] second
                frame[y][x] = icon

        return frame

    def add_fg_widget(self, widget: list[dict]):
        """ adds a list of pixels to the foreground buffer """
        for pix in widget:
            self.add_fg_pixel(pix)

    def add_fg_pixel(self, fg_pixel: dict):
        """ adds a pixel to the foreground buffer """
        if not isinstance(fg_pixel, dict):
            raise ValueError("Bad pixel. Expected: "
                             "{\"x\": int, \"y\": int, \"icon\": str}")
        self.fg_buffer.append(fg_pixel)

    def clear_fg(self):
        """ clears the fg buffer """
        self.fg_buffer = []
