import re
from typing import List, Tuple, Optional

import gdb


class TlExpectedPrinter(gdb.printing.PrettyPrinter):

    def __init__(self, tl_expected_instance):
        self.tl_expected_instance = tl_expected_instance
        super().__init__("tl::expected")

    def get_contained_value(self) -> str:
        """
        Gibt Wert des tl::expecteds als String.
        Wenn expected, gibt den Erfolg-Wert, sonst den Fehler-Wert.
        """
        has_value = self.tl_expected_instance["m_has_val"]
        if has_value:
            value = self.tl_expected_instance['m_val']
        else:
            value = self.tl_expected_instance["m_unexpect"]["m_val"]
        return value

    def get_content_name(self) -> str:
        """
        Name für das Feld, welches den Inhalt des tl::expected beschreibt.
        """
        return "value" if self.has_value() else "error"

    def has_value(self) -> bool:
        """
        Gibt an, ob tl::expected im Fehler- oder im Erfolgszustand ist.
        :return: True wenn Erfolgszustand, sonst False.
        """
        return self.tl_expected_instance['m_has_val']

    def has_value_name(self) -> str:
        """
        Name für das Feld, welches den Zustand des tl::expected beschreibt (Erfolg/Fehler).
        """
        return "has_value"

    def to_string(self) -> str:
        """
        GDB nutzt diese Methode um die String-Repräsentation des Typs anzuzeigen (bei Aufruf von print in gdb-Konsole).
        Der Rückgabewert dieser Funktion wird vor den Werten von Children angezeigt.
        Wird in CLion nicht im Debugger angezeigt.
        """
        return self.tl_expected_instance.type.name

    def children(self) -> List[Tuple[str, str]]:
        """
        Jedes Element der Liste wird in CLion als eine Zeile im Debugger angezeigt.
        Für jedes Tupel gilt: Erster Eintrag ist der Name des Elements, der zweite Eintrag der Wert.
        """
        return [(self.has_value_name(), self.has_value()), (self.get_content_name(), self.get_contained_value())]


def register_tl_expected_printer(value: gdb.Value) -> Optional[TlExpectedPrinter]:
    """
    Registriert Printer für tl::expected bei gdb.
    :param value:
    :return:
    """
    if value.type.name is None:
        return None
    regex = re.compile("tl::expected<.*, .*>")
    if regex.match(value.type.name):
        return TlExpectedPrinter(value)
    return None
