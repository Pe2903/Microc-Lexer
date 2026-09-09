from __future__ import annotations

import enum
import string
from dataclasses import dataclass
from typing import Iterator


class TokenKind(enum.Enum):
    """Classe já implementada: nomes e números não devem ser alterados."""

    EOF = -1

    IDENTIFIER = 1
    INT_LITERAL = 2
    STRING_LITERAL = 3

    KW_INT = 10
    KW_BOOL = 11
    KW_VOID = 12
    KW_TRUE = 13
    KW_FALSE = 14
    KW_IF = 15
    KW_ELSE = 16
    KW_WHILE = 17
    KW_RETURN = 18
    KW_PRINT = 19

    PLUS = 20
    MINUS = 21
    STAR = 22
    SLASH = 23
    PERCENT = 24
    LESS = 25
    LESS_EQUAL = 26
    GREATER = 27
    GREATER_EQUAL = 28
    EQUAL_EQUAL = 29
    NOT_EQUAL = 30
    LOGICAL_AND = 31
    LOGICAL_OR = 32
    LOGICAL_NOT = 33
    ASSIGN = 34

    LEFT_PAREN = 40
    RIGHT_PAREN = 41
    LEFT_BRACE = 42
    RIGHT_BRACE = 43
    COMMA = 44
    SEMICOLON = 45


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    lexeme: str
    value: int | str | bool | None
    line: int
    column: int

    def __str__(self) -> str:
        return (
            f"<{self.kind.value}, {self.kind.name}, {self.lexeme!r}, "
            f"{self.value!r}, {self.line}, {self.column}>"
        )


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"erro léxico em {self.line}:{self.column}: {self.message}"


PALAVRAS_RESERVADAS: dict[str, TokenKind] = {
    "int": TokenKind.KW_INT,
    "bool": TokenKind.KW_BOOL,
    "void": TokenKind.KW_VOID,
    "true": TokenKind.KW_TRUE,
    "false": TokenKind.KW_FALSE,
    "if": TokenKind.KW_IF,
    "else": TokenKind.KW_ELSE,
    "while": TokenKind.KW_WHILE,
    "return": TokenKind.KW_RETURN,
    "print": TokenKind.KW_PRINT,
}

INICIO_IDENTIFICADOR = frozenset(string.ascii_letters + "_")
CORPO_IDENTIFICADOR = frozenset(string.ascii_letters + string.digits + "_")
ESPACOS = frozenset(" \t\r\n")


class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def _fim(self) -> bool:
        return self.pos >= len(self.source)

    def _olhar(self, adiante: int = 0) -> str:
        indice = self.pos + adiante
        if indice >= len(self.source):
            return ""
        return self.source[indice]

    def _avancar(self) -> str:
        caractere = self.source[self.pos]
        self.pos += 1
        if caractere == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return caractere

    def _descartar_espacos(self) -> None:
        while self._olhar() in ESPACOS:
            self._avancar()

    def _identificador_ou_palavra_reservada(self, linha: int, coluna: int) -> Token:
        inicio = self.pos
        while self._olhar() in CORPO_IDENTIFICADOR:
            self._avancar()
        lexema = self.source[inicio:self.pos]

        reservada = PALAVRAS_RESERVADAS.get(lexema)
        if reservada is None:
            return Token(TokenKind.IDENTIFIER, lexema, lexema, linha, coluna)
        if reservada is TokenKind.KW_TRUE:
            return Token(reservada, lexema, True, linha, coluna)
        if reservada is TokenKind.KW_FALSE:
            return Token(reservada, lexema, False, linha, coluna)
        return Token(reservada, lexema, None, linha, coluna)

    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        while True:
            self._descartar_espacos()

            if self._fim():
                yield Token(TokenKind.EOF, "", None, self.line, self.column)
                return

            linha, coluna = self.line, self.column

            if self._olhar() in INICIO_IDENTIFICADOR:
                yield self._identificador_ou_palavra_reservada(linha, coluna)
                continue

            caractere = self._avancar()
            raise LexerError(f"caractere inesperado {caractere!r}", linha, coluna)

    def scan(self) -> list[Token]:
        return list(self.tokens())
