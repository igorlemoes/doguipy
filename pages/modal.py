from nicegui import ui


class Modal(ui.dialog):
    def __init__(self, text) -> None:
        super().__init__()
        with self, ui.card().classes('flex w-96 h-96'):
            with ui.row().classes('w-full flex justify-center'):
                ui.label(text).classes('text-2xl').style('color:gray')
            self.imagem_col = ui.column(wrap=True).classes('w-full flex mt-16 justify-center content-center')
            self.imagem_col.clear()
            self.spinner()

    def spinner(self):
        self.imagem_col.clear()
        with self.imagem_col:
                ui.spinner(size='10em')