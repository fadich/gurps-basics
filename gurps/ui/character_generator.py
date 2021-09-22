#!/usr/bin/env python3

import sys
import argparse

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import tkinter.filedialog as filedialog
import tkinter.messagebox  as messagebox

from typing import Optional, Union

import pyperclip

from gurps.character import Character
from gurps.generation import CharacterGenerator


class CharacterList:

    def __init__(self):
        self.generations = []
        self.pointer = 0

    def generate(self):
        char = self._create_unique_character()
        self.generations.append((char.name, str(char)))

        self.pointer = len(self.generations) - 1

    def get_current_character(self) -> Optional[str]:
        if self.generations:
            return self.generations[self.pointer]

        return None

    def delete(self):
        del self.generations[self.pointer]
        if len(self.generations) <= 1:
            self.pointer = 0
        else:
            if self.pointer > 0:
                self.pointer -= 1
            else:
                self.pointer += 1

    def clear(self):
        self.pointer = 0
        self.generations.clear()

    def _create_unique_character(self) -> Character:
        new_char = CharacterGenerator().generate()
        for generation in self.generations:
            if generation[0] == new_char.name:
                return self._create_unique_character()

        return new_char


class Application:
    DEFAULT_PANDX = 10
    DEFAULT_PANDY = 5

    DEFAULT_FILE_TYPES = [
        ('GURPS character generator', '.gctxt'),
        ('GURPS character generator', '.txt'),
    ]

    CHARACTER_LIST_SEPARATOR = '\n' * 2 + '=' * 32 + '\n' * 2
    SINGLE_CHARACTER_SEPARATOR = ' ===> '

    def __init__(self, working_file: Optional[str] = None):
        self.working_file = working_file
        self.saved = False

        self.root = tk.Tk()
        self.main_menu = tk.Menu()
        self.file_menu = tk.Menu(tearoff=0)
        self.help_menu = tk.Menu(tearoff=0)

        self.file_menu.add_command(
            label='Новый',
            command=self.new
        )
        self.file_menu.add_command(
            label='Открыть',
            command=self.open
        )
        self.file_menu.add_command(
            label='Сохранить',
            command=self.save
        )
        self.file_menu.add_command(
            label='Сохранить как',
            command=self.save_as
        )

        self.help_menu.add_command(
            label='О программе',
            command=self.about
        )

        self.main_menu.add_cascade(
            label='Файл',
            menu=self.file_menu
        )
        self.main_menu.add_cascade(
            label='Справка',
            menu=self.help_menu
        )

        self.root.config(menu=self.main_menu)
        self.root.geometry('940x620')
        self.root.minsize(900, 600)
        # self.root.resizable(width=False, height=False)
        self.root.option_add('*Font', 'aerial 12')
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

        self._update_window_title()

        self.character_list = CharacterList()

        self.prev_btn = tk.Button(
            text='<< Назад',
            command=self.previous
        )
        self.next_btn = tk.Button(
            text='Вперед >>',
            command=self.next
        )
        self.generate_btn = tk.Button(
            text='Генерировать',
            command=self.generate
        )

        self.char_text = scrolledtext.ScrolledText(
            width=96,
            height=27,
            wrap='word',
        )

        self.delete_btn = tk.Button(
            text='Удалить',
            command=self.delete
        )
        self.copy_btn = tk.Button(
            text='Копировать',
            command=self.copy
        )

        self.prev_btn.grid(
            row=0,
            column=0,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY
        )
        self.generate_btn.grid(
            row=0,
            column=1,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY
        )
        self.next_btn.grid(
            row=0,
            column=2,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY
        )

        self.char_text.grid(
            row=1,
            column=0,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY,
            columnspan=3
        )

        self.delete_btn.grid(
            row=2,
            column=0,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY,
        )
        self.copy_btn.grid(
            row=2,
            column=2,
            padx=self.DEFAULT_PANDX,
            pady=self.DEFAULT_PANDY,
        )

    @property
    def current_character(self) -> str:
        char = self.character_list.get_current_character()
        if char:
            return char[1]

        return ''

    def start(self):
        if self.working_file:
            self._load_from_file(self.working_file)
        else:
            self.generate()

        self.root.mainloop()

    def generate(self):
        self.character_list.generate()
        self._update_current_character()
        self.saved = False
        self._update_window_title()

    def previous(self):
        self.character_list.pointer -= 1
        self._update_current_character()

    def next(self):
        self.character_list.pointer += 1
        self._update_current_character()

    def delete(self):
        char_name = self.character_list.get_current_character()[0]
        answer = messagebox.askyesno(
            title='Удалить персонажа',
            message=(
                f'Удалить персонажа "{char_name}"?'
            )
        )

        if not answer:
            return

        self.character_list.delete()
        self._update_current_character()
        self.saved = False
        self._update_window_title()

    def copy(self):
        pyperclip.copy(self.current_character)

    def open(self):
        if self.character_list.generations and not self.saved:
            answer = messagebox.askyesno(
                title='Открыть проект',
                message=(
                    'Вы уверены, что хотите открыть новый список генераций?\n'
                    'Все несохраненные изменения будут очищены.'
                )
            )

            if not answer:
                return

        ofile = filedialog.askopenfile(filetypes=self.DEFAULT_FILE_TYPES)
        if not ofile:
            return

        self._load_from_file(ofile.name)

    def new(self, skip_confirm: bool = False):
        if self.character_list.generations \
                and not self.saved \
                and not skip_confirm:
            answer = messagebox.askyesno(
                title='Создать новый проект',
                message=(
                    'Вы уверены, что хотите создать новый список генераций?\n'
                    'Все несохраненные изменения будут очищены.'
                )
            )

            if not answer:
                return

        self.character_list.clear()

        self._update_current_character()
        self.saved = True
        self._update_working_file(filename=None)

    def save(self):
        if not self.working_file:
            self.save_as()
            return

        with open(self.working_file, 'w') as file:
            file.write(
                self.CHARACTER_LIST_SEPARATOR.join(
                    map(
                        lambda gen: (
                            f'{gen[0]}'
                            f'{self.SINGLE_CHARACTER_SEPARATOR}'
                            f'{gen[1]}'
                        ),
                        self.character_list.generations
                    )
                )
            )

        self.saved = True
        self._update_window_title()

    def save_as(self):
        filename = filedialog.asksaveasfilename(
            filetypes=self.DEFAULT_FILE_TYPES
        )
        if not filename:
            return

        if not filename.endswith('.gctxt') or not filename.endswith('.txt'):
            filename = f'{filename}.gctxt'

        self._update_working_file(filename=filename)
        self.save()

    def on_close(self):
        if self.character_list.generations and not self.saved:
            answer = messagebox.askyesno(
                title='Закрыть проект',
                message=(
                    'Вы уверены, что хотите загрыть текущий список генераций?'
                    '\nВсе несохраненные изменения будут очищены.'
                )
            )

            if not answer:
                return

        self.root.destroy()

    def about(self):
        messagebox.showinfo(
            title='О программе',
            message=(
                'Версия сборки: 1.1.0\n\n'
                'Жалобы и предложения по улучшению: '
                'https://github.com/fadich/gurps-basics/issues'
            )
        )

    def _update_buttons_state(self):
        if self.character_list.pointer <= 0:
            self.prev_btn['state'] = tk.DISABLED
        else:
            self.prev_btn['state'] = tk.ACTIVE

        generations_count = len(self.character_list.generations)

        if self.character_list.pointer + 1 >= generations_count:
            self.next_btn['state'] = tk.DISABLED
        else:
            self.next_btn['state'] = tk.ACTIVE

        if len(self.character_list.generations) + 1 == \
                len(CharacterGenerator.NAMES):
            self.generate_btn['state'] = tk.DISABLED

        if self.current_character:
            self.copy_btn['state'] = tk.ACTIVE
            self.delete_btn['state'] = tk.ACTIVE
        else:
            self.copy_btn['state'] = tk.DISABLED
            self.delete_btn['state'] = tk.DISABLED

    def _update_current_character(self):
        self.char_text.delete('1.0', tk.END)
        self.char_text.insert(tk.END, self.current_character)

        self._update_buttons_state()

    def _update_working_file(self, filename: Union[str, None]):
        self.working_file = filename
        self._update_window_title()

    def _update_window_title(self):
        if self.working_file is not None:
            # filename = os.path.basename(self.working_file)
            title = f'Generations - {self.working_file}'
        else:
            title = 'New Generations'

        if not self.saved:
            title = f'* {title}'

        self.root.title(title)

    def _load_from_file(self, filename: str):
        with open(filename) as file:
            content = file.read()

        try:
            generations = content.split(self.CHARACTER_LIST_SEPARATOR)

            if self.SINGLE_CHARACTER_SEPARATOR not in generations[0]:
                raise SyntaxError('Invalid file structure')

            generations = [
                g.split(self.SINGLE_CHARACTER_SEPARATOR) for g in generations
            ]
        except Exception as e:
            messagebox.showerror(
                title='Reading error',
                message=f'Error on reading file: {e}'
            )

            return

        self.new(skip_confirm=True)

        self._update_working_file(filename)
        self.character_list.generations = generations

        self._update_current_character()


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('working_file', metavar='N', nargs='?', type=str,
                        help='path to .gctxt file to be opened')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help='set debug log level')
    args = parser.parse_args()

    app = Application(
        working_file=args.working_file
    )
    app.start()

    return 0


if __name__ == '__main__':
    sys.exit(main())
