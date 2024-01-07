#!/usr/bin/env python
"""
Password Generator
Generates a password with high entropy and copies the result to clipboard.

Copyright (C) 2024  worstprgr <adam@seishin.io> GPG Key: key.seishin.io

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import string
import random
import argparse
import subprocess
import platform


class Clipboard:
    def copy_to_clipboard(self, text: str) -> None:
        current_platform: str = platform.system()

        if current_platform == 'Linux':
            self.__cp_linux(text)
        elif current_platform == 'Windows':
            self.__cp_windows(text)
        elif current_platform == 'Darwin':
            self.__cp_macos(text)
        else:
            raise NotImplemented('Unknown Platform/OS')

    @staticmethod
    def __cp_windows(text: str):
        try:
            subprocess.run('clip', universal_newlines=True, input=text, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except Exception as e:
            print(e)

    @staticmethod
    def __cp_macos(text: str):
        try:
            subprocess.run('pbcopy', universal_newlines=True, input=text, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except Exception as e:
            print(e)

    def __cp_linux(self, text: str) -> None:
        clipboard_engine: str = ''

        if self.__check_linux_clip_managers('xclip'):
            clipboard_engine = 'xclip -selection clipboard'
        elif self.__check_linux_clip_managers('xsel'):
            clipboard_engine = 'xsel --clipboard --input'

        if clipboard_engine:
            try:
                subprocess.run(clipboard_engine, universal_newlines=True, input=text, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            except Exception as e:
                print(e)
        else:
            raise RuntimeError('No known clipboard engine found')

    @staticmethod
    def __check_linux_clip_managers(clip_manager: str) -> bool:
        try:
            result = subprocess.run(['which', clip_manager], stdout=subprocess.PIPE, text=True)
            return bool(result.stdout.strip())
        except Exception as e:
            print(e)
            return False


class ArgParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('length', type=int, help='How long the password should be')
        parser.add_argument('-n', '--nocp', action='store_true', help='If provided, this program would not store the '
                                                                      'output in the OS clipboard.')

        args = parser.parse_args()
        self.pass_length: int = args.length
        self.nocp: bool = args.nocp


class PassGen(ArgParser, Clipboard):
    def __init__(self):
        ArgParser.__init__(self)
        Clipboard.__init__(self)
        self.passes: int = 512
        self.letters: str = string.ascii_letters
        self.digits: str = string.digits
        self.other: str = '!#$%&()*+-=?@_'
        self.chars: str = self.letters + self.digits + self.other

    def main(self):
        program_name: str = 'Password Generator'
        print('-' * 7, program_name, '-' * 7)

        result = self.rnd_chars(self.prep_chars(), self.pass_length)

        if not self.nocp:
            print('Info: Copied to clipboard')
            self.copy_to_clipboard(result)
        else:
            print('Info: Copy to clipboard disabled')

        print(result)
        print('-'*(16+len(program_name)))

    def prep_chars(self) -> str:
        new_random: list[str]
        chars: list[str] = list(self.chars)

        for x in range(self.passes):
            random.shuffle(chars)

        return ''.join(chars)

    @staticmethod
    def rnd_chars(given_chars: str, pw_length: int) -> str:
        return ''.join(random.choices(given_chars, k=pw_length))


if __name__ == '__main__':
    PassGen().main()
