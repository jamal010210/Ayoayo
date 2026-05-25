class HistoryController:
    """
    Controls the history screen:
    - input handling
    - loading player history
    - UI state (active/results/errors)
    """

    def __init__(self, renderer, persistence):
        """Initializes the history controller with renderer and persistence layer."""
        self.renderer = renderer
        self.persistence = persistence

        self.active = False
        self.results = None
        self.error = None

    def open(self):
        """Opens the history screen and resets UI state."""
        self.active = True
        self.results = None
        self.error = None

        self.renderer.history_player_text = ""
        self.renderer.history_input_active = False
        self.renderer.history_suggestions = []

    def close(self):
        """Closes the history screen."""
        self.active = False

    def handle_click(self, pos):
        """Handles mouse clicks on the history screen."""
        # return button
        if self.renderer.get_return_to_menu_button_collision(pos):
            self.close()
            return

        # suggestion click
        clicked = self.renderer.get_history_suggestion_at_position(pos)

        if clicked:
            self._load_player(clicked[1])
            return

        # input focus
        self.renderer.handle_history_input_click(pos)

    def handle_key(self, event):
        """Handles keyboard input for history search."""
        if self.renderer.handle_history_input_key(event):
            name = self.renderer.get_history_input_value()
            self._load_player(name)

        self.renderer.history_suggestions = (
            self.persistence.get_player_suggestions(
                self.renderer.get_history_input_value()
            )
        )

    def _load_player(self, name: str):
        """Loads match history for a given player name."""
        if not name:
            self.results = []
            self.error = "Enter a player name."
            return

        player = self.persistence.get_player_by_name(name)

        if not player:
            self.results = []
            self.error = f"No exact player found for '{name}'."
            return

        self.results = self.persistence.get_player_history(player[0])
        self.error = None

    def render(self):
        """Renders the history screen."""
        self.renderer.draw_history_screen(self.results, self.error)
