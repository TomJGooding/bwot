from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.geometry import clamp
from textual.reactive import var
from textual.validation import Integer
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

            yield Input(
                f"{self.a}",
                id="input-a",
                type="integer",
                validators=Integer(0, 255),
                compact=True,
            )
            for _ in range(3):
                yield Label(f"{self.a:08b}", classes="binary-a")

            yield Input(
                f"{self.b}",
                id="input-b",
                type="integer",
                validators=Integer(0, 255),
                compact=True,
            )
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

    @on(Input.Blurred)
    @on(Input.Submitted)
    def on_input_blurred_or_submitted(
        self, event: Input.Blurred | Input.Submitted
    ) -> None:
        input = event.input
        validation_result = event.validation_result
        assert validation_result is not None
        if not validation_result.is_valid:
            failure = validation_result.failures[0]
            # If the value is not a number, set the input to zero.
            if isinstance(failure, Integer.NotANumber):
                input.value = str(0)
            # If the value is not in range, set the input to the clamped value.
            elif isinstance(failure, Integer.NotInRange):
                clamped_value = clamp(int(event.value), 0, 255)
                input.value = str(clamped_value)

        if input.id == "input-a":
            self.a = int(input.value)
        elif input.id == "input-b":
            self.b = int(input.value)


if __name__ == "__main__":
    app = BwotApp()
    app.run()
