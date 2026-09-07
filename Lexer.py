from __future__ import annotations
 
import enum
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
 
 
class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""
 
    def __init__(self, source: str):
        self.source = source
        # Cursor sobre o texto. pos é a posição absoluta (0, 1, 2, ...);
        # line e column são a mesma posição em coordenadas humanas, que
        # começam em 1 e são o que o Token guarda.
        self.pos = 0
        self.line = 1
        self.column = 1
 
    # -- operações básicas sobre o cursor ---------------------------------
 
    def _fim(self) -> bool:
        """O cursor já passou do último caractere?"""
        return self.pos >= len(self.source)
 
    def _olhar(self, adiante: int = 0) -> str:
        """Devolve o caractere à frente SEM consumi-lo.
 
        Devolve string vazia depois do fim do texto, para que quem chama
        possa comparar sem precisar checar o limite antes.
        """
        indice = self.pos + adiante
        if indice >= len(self.source):
            return ""
        return self.source[indice]
 
    def _avancar(self) -> str:
        """Consome um caractere e anda um passo, mantendo linha e coluna.
 
        Este é o único método que altera a posição. Concentrar isso aqui
        é o que garante que as coordenadas fiquem certas em todo o resto
        do lexer.
        """
        caractere = self.source[self.pos]
        self.pos += 1
        if caractere == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return caractere
 
    # -- laço principal ---------------------------------------------------
 
    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        while True:
            if self._fim():
                # EOF tem lexema vazio, valor None e fica na posição
                # imediatamente posterior ao último caractere consumido.
                yield Token(TokenKind.EOF, "", None, self.line, self.column)
                return
 
            # Ainda não há nenhuma categoria de token implementada, então
            # qualquer caractere é desconhecido neste ponto. As próximas
            # etapas vão inserir os reconhecedores acima desta linha.
            linha, coluna = self.line, self.column
            caractere = self._avancar()
            raise LexerError(
                f"caractere inesperado {caractere!r}", linha, coluna
            )
 
    def scan(self) -> list[Token]:
        return list(self.tokens())
 
