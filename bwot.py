from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.reactive import var
from textual.widgets import Input, Label


class BwotApp(App):
    CSS = """
    #bwot-grid {
        layout: grid;
        height: auto;
        width: auto;
        grid-size: 4;
        grid-columns: 10;

        .heading {
            text-style: bold;
        }

        .result {
            text-style: bold;
        }
    }
    """

    ENABLE_COMMAND_PALETTE = False

    a = var(58, init=False)
    b = var(41, init=False)

    def compose(self) -> ComposeResult:
        with Grid(id="bwot-grid"):
            columns = ["", "AND", "OR", "XOR"]
            for col in columns:
                yield Label(col, classes="heading")

            yield Input(f"{self.a}", id="input-a", type="integer", compact=True)
            for _ in range(3):
                yield Label(f"{self.a:08b}", classes="binary-a")

            yield Input(f"{self.b}", id="input-b", type="integer", compact=True)
            for _ in range(3):
                yield Label(f"{self.b:08b}", classes="binary-b")

            yield Label("Result", classes="result")
            yield Label(f"{self.a & self.b:08b}", id="result-and", classes="result")
            yield Label(f"{self.a | self.b:08b}", id="result-or", classes="result")
            yield Label(f"{self.a ^ self.b:08b}", id="result-xor", classes="result")

    def watch_a(self) -> None:
        for label in self.query(".binary-a").results(Label):
            label.update(f"{self.a:08b}")
        self.update_results()

    def watch_b(self) -> None:
        for label in self.query(".binary-b").results(Label):
            label.update(f"{self.b:08b}")
        self.update_results()

    def update_results(self) -> None:
        self.query_one("#result-and", Label).update(f"{self.a & self.b:08b}")
        self.query_one("#result-or", Label).update(f"{self.a | self.b:08b}")
        self.query_one("#result-xor", Label).update(f"{self.a ^ self.b:08b}")

    @on(Input.Submitted, "#input-a")
    @on(Input.Blurred, "#input-a")
    def on_input_a_submitted(self, event: Input.Submitted) -> None:
        self.a = int(event.value)

    @on(Input.Submitted, "#input-b")
    @on(Input.Blurred, "#input-b")
    def on_input_b_submitted(self, event: Input.Submitted) -> None:
        self.b = int(event.value)


if __name__ == "__main__":
    app = BwotApp()
    app.run()
